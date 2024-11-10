# -*- coding: utf-8 -*-
"""volume discretization structure class
"""
import warnings
import copy

import torch

from torchgdm.constants import DTYPE_FLOAT, DTYPE_COMPLEX, COLORS_DEFAULT
from torchgdm.tools.misc import get_default_device
from torchgdm.struct.base_classes import StructBase
from torchgdm.tools.geometry import get_step_from_geometry
from torchgdm.tools.geometry import sample_random_spherical
from torchgdm.tools.geometry import rotation_x, rotation_y, rotation_z
from torchgdm.tools.misc import ptp
from torchgdm.linearsystem import _reduce_dimensions


# --- base class volume discretized structure container - 3D
class StructDiscretized3D(StructBase):
    """base class volume discretized structure

    Defines the basic volume discretization, its polarizabilities and self-terms
    """

    __name__ = "3D volume discretized structure class"

    def __init__(
        self,
        positions: torch.Tensor,
        materials,
        step=None,
        mesh_normalization_factor: float = 1,
        radiative_correction: bool = False,
        device: torch.device = None,
        **kwargs,
    ):
        """3D discretized structure

        Args:
            positions (torch.Tensor): meshpoint positions (3D, but all y values must be zero)
            materials (material class, or list of them): material of structure. If list, define the material of each meshpoint.
            step (float, optional): nominal stepsize. If not provided, infer automatically from geometry. Defaults to None.
            mesh_normalization_factor (float, optional): mesh normalization. Needs to be adapted for non-cubic meshes. Defaults to 1 (cubic).
            radiative_correction (bool, optional): Add radiative correction term for each meshcell. Defaults to False.
            device (torch.device, optional): Defaults to "cpu" (can be changed by :func:`torchgdm.use_cuda`).

        Raises:
            ValueError: Invalid material config
        """
        super().__init__(
            radiative_correction=radiative_correction, device=device, **kwargs
        )
        self.mesh = "3D"
        self.n_dim = 3

        self.positions = torch.as_tensor(
            positions, dtype=DTYPE_FLOAT, device=self.device
        )
        self.r0 = self.get_center_of_mass()  # center of gravity

        if step is None:
            step_scalar = get_step_from_geometry(self.positions)
        else:
            step_scalar = step
        # step for every meshcell, for consistency with other struct classes
        self.step = step_scalar * torch.ones(
            len(self.positions), dtype=DTYPE_FLOAT, device=self.device
        )

        self.mesh_normalization_factor = torch.as_tensor(
            mesh_normalization_factor, dtype=DTYPE_FLOAT, device=self.device
        )
        if mesh_normalization_factor == 1:
            self.mesh = "cubic"
        else:
            self.mesh = "hexagonal"

        # material of each meshpoint
        if hasattr(materials, "__iter__"):
            if len(materials) != len(self.positions):
                raise ValueError(
                    "Either a global material needs to be given or "
                    + "each meshpoint needs a defined material. "
                    + "But meshpoint list and materials list are of different lengths."
                )
            self.materials = materials
        else:
            self.materials = [materials for i in self.positions]

        self.zeros = torch.zeros(
            (len(self.positions), 3, 3), dtype=DTYPE_COMPLEX, device=self.device
        )

        # discretized, made from natural material: only electric response
        self.evaluation_terms = ["E"]  # possible terms 'E' and 'H'

    def __repr__(self, verbose=False):
        """description about structure"""
        out_str = ""
        out_str += "------ discretized 3D nano-object -------"
        out_str += "\n" + " mesh type:              {}".format(self.mesh)
        out_str += "\n" + " nr. of meshpoints:      {}".format(len(self.positions))
        out_str += "\n" + " nominal stepsizes (nm): {}".format(
            [float(f) for f in torch.unique(self.step)]
        )
        out_str += "\n" + " materials:              {}".format(
            [m.__name__ for m in set(self.materials)]
        )
        bnds = ptp(self.positions, dim=0)
        out_str += "\n" + " size & position:"
        out_str += "\n" + "     X-extension    :    {:.1f} (nm)".format(bnds[0])
        out_str += "\n" + "     Y-extension    :    {:.1f} (nm)".format(bnds[1])
        out_str += "\n" + "     Z-extension    :    {:.1f} (nm)".format(bnds[2])
        out_str += "\n" + "     center of mass :    ({:.1f}, {:.1f}, {:.1f})".format(
            *self.r0
        )

        return out_str

    def set_device(self, device):
        """move all tensors of the class to device"""
        super().set_device(device)

        self.zeros = self.zeros.to(device)
        self.step = self.step.to(device)
        self.r0 = self.r0.to(device)

        self.mesh_normalization_factor = self.mesh_normalization_factor.to(device)

        for mat in self.materials:
            mat.set_device(device)

    # --- self-terms
    def get_selfterm_pE(self, wavelength: float, environment) -> torch.Tensor:
        """return list of 'EE' self-term tensors (3x3) at each meshpoint

        Args:
            wavelength (float): in nm
            environment (environment class): 3D environement class

        Returns:
            torch.Tensor: pE self term tensor
        """
        eps_env = environment.get_environment_permittivity_scalar(
            wavelength, r_probe=self.positions
        )

        norm_nonrad = (
            (-4 * torch.pi)
            * self.mesh_normalization_factor
            / (3 * self.step**3 * eps_env)
        )

        if self.radiative_correction:
            k0 = 2 * torch.pi / wavelength
            norm_rad = (
                self.mesh_normalization_factor
                * (1j * k0**3 * (2 / 3))
                * torch.ones(
                    len(self.positions), dtype=DTYPE_COMPLEX, device=self.device
                )
            )
            cnorm = norm_nonrad + norm_rad
        else:
            cnorm = norm_nonrad

        self_terms_pE = torch.zeros(
            (len(self.positions), 3, 3), dtype=DTYPE_COMPLEX, device=self.device
        )
        self_terms_pE[:, 0, 0] = cnorm
        self_terms_pE[:, 1, 1] = cnorm
        self_terms_pE[:, 2, 2] = cnorm

        return self_terms_pE

    def get_selfterm_mE(self, wavelength: float, environment) -> torch.Tensor:
        return self.zeros

    def get_selfterm_pH(self, wavelength: float, environment) -> torch.Tensor:
        return self.zeros

    def get_selfterm_mH(self, wavelength: float, environment) -> torch.Tensor:
        return self.zeros

    # --- polarizabilities
    def get_polarizability_pE(self, wavelength: float, environment) -> torch.Tensor:
        """return list of EE polarizability tensors (3x3) at each meshpoint

        Args:
            wavelength (float): in nm
            environment (environment class): 3D environement class

        Returns:
            torch.Tensor: pE polarizability tensor
        """
        eps_env = environment.get_environment_permittivity_scalar(
            wavelength, r_probe=self.positions
        )
        eps_env_tensor = torch.zeros(
            (len(self.positions), 3, 3), dtype=DTYPE_COMPLEX, device=self.device
        )
        eps_env_tensor[:, 0, 0] = eps_env
        eps_env_tensor[:, 1, 1] = eps_env
        eps_env_tensor[:, 2, 2] = eps_env

        eps_geo = torch.zeros(
            (len(self.positions), 3, 3), dtype=DTYPE_COMPLEX, device=self.device
        )
        for i, mat in enumerate(self.materials):
            eps_geo[i] = mat.get_epsilon(wavelength)

        vcell_norm = self.step**3 / self.mesh_normalization_factor

        ## --- isotropic polarizability
        alpha_pE = (
            (eps_geo - eps_env_tensor)
            * vcell_norm.unsqueeze(1).unsqueeze(1)
            / (4.0 * torch.pi)
        )

        # with reaction term:
        # k0 = 2 * torch.pi / wavelength
        # alpha_pE = alpha_pE / (1 - (1j * k0**3 * (2 / 3)) * alpha_pE)

        return alpha_pE

    def get_polarizability_mE(self, wavelength: float, environment) -> torch.Tensor:
        return self.zeros

    def get_polarizability_pH(self, wavelength: float, environment) -> torch.Tensor:
        return self.zeros

    def get_polarizability_mH(self, wavelength: float, environment) -> torch.Tensor:
        return self.zeros

    # --- eff. polarizability model extraction wrapper
    def convert_to_effective_polarizability_pair(
        self,
        environment,
        wavelengths: torch.Tensor,
        test_accuracy: bool = False,
        only_pE_mH: bool = True,
        batch_size=16,
        **kwargs,
    ):
        """convert the structure to an effective point polarizability structure model

        The model consists of a pair of electric and magnetic dipole.

        kwargs are passed to :func:`extract_effective_polarizability`

        Args:
            environment (environment class): 3D environement class
            wavelengths (torch.Tensor): list of wavelengths to extract the model at. in nm
            test_accuracy (bool, optional): Whether to test accuracy in a scattering simulation. Defaults to False.
            only_pE_mH (bool, optional): whether to extract only a p/m model (True) or a full (6x6) polarizability (False). Defaults to True.

        Returns:
            :class:`torchgdm.pola.point.StructEffPola3D`: Effective dipole-pair model
        """
        from torchgdm.struct import StructEffPola3D

        wavelengths = torch.as_tensor(
            wavelengths, dtype=DTYPE_FLOAT, device=self.device
        )

        alpha = extract_eff_pola_via_mp_decomposition(
            struct=self,
            environment=environment,
            wavelengths=wavelengths,
            only_pE_mH=only_pE_mH,
            batch_size=batch_size,
            **kwargs,
        )

        struct_aeff = StructEffPola3D(
            positions=torch.stack([self.r0]),
            alpha_dicts=[alpha],
            environment=environment,
            device=self.device,
        )

        # perform a test in an actual scattering simulation
        if test_accuracy:
            test_effective_polarizability_accuracy(struct_aeff, self)

        return struct_aeff

    # --- plotting
    def plot(
        self,
        projection="auto",
        scale=1.0,
        color="auto",
        show_grid=True,
        legend=True,
        set_ax_aspect=True,
        alpha=1.0,
        reset_color_cycle=True,
        **kwargs,
    ):
        """plot the structure (2D)

        Args:
            projection (str, optional): Cartesian projection. Default: "XY" or plane in which all dipoles lie. Defaults to "auto".
            scale (float, optional): scaling factor of the grid cells, if shown. Defaults to 1.0.
            color (str, optional): plot color. Defaults to "auto".
            show_grid (bool, optional): whether to show mesh grid (if available in structure). Defaults to True.
            legend (bool, optional): show legend. Defaults to True.
            set_ax_aspect (bool, optional): automatically set aspect ratio to equal. Defaults to True.
            alpha (int, optional): optional transparency. Defaults to 1.
            reset_color_cycle (bool, optional): reset color cycle after finishing the plot. Defaults to True.

        Returns:
            matplotlib axes
        """
        from torchgdm.visu import visu2d

        im = visu2d.geo2d._plot_structure_discretized(
            self,
            projection=projection,
            scale=scale,
            color=color,
            show_grid=show_grid,
            legend=legend,
            set_ax_aspect=set_ax_aspect,
            alpha=alpha,
            reset_color_cycle=reset_color_cycle,
            **kwargs,
        )
        return im

    def plot_contour(
        self,
        projection="auto",
        color="auto",
        set_ax_aspect=True,
        alpha=1.0,
        alpha_value=None,
        reset_color_cycle=True,
        **kwargs,
    ):
        """plot the contour around the structure (2D)

        Args:
            projection (str, optional): which cartesian plane to project onto. Defaults to "auto".
            color (str, optional): optional matplotlib compatible color. Defaults to "auto".
            set_ax_aspect (bool, optional): If True, will set aspect of plot to equal. Defaults to True.
            alpha (float, optional): matplotlib transparency value. Defaults to 1.0.
            alpha_value (float, optional): alphashape value. If `None`, try to automatically optimize for best enclosing of structure. Defaults to None.
            reset_color_cycle (bool, optional): reset color cycle after finishing the plot. Defaults to True.

        Returns:
            matplotlib line: matplotlib's `scatter` output
        """
        from torchgdm.visu import visu2d

        im = visu2d.geo2d.contour(
            self,
            projection=projection,
            color=color,
            set_ax_aspect=set_ax_aspect,
            alpha=alpha,
            alpha_value=alpha_value,
            reset_color_cycle=reset_color_cycle,
            **kwargs,
        )
        return im

    def plot3d(self, **kwargs):
        """plot the structure (3D)"""
        from torchgdm.visu import visu3d

        return visu3d.geo3d._plot_structure_discretized(self, **kwargs)

    # --- geometry operations
    def rotate(self, alpha, center=torch.as_tensor([0.0, 0.0, 0.0]), axis="z"):
        """rotate the structure

        Args:
            alpha (float): rotation angle (in rad)
            center (torch.Tensor, optional): center of rotation axis. Defaults to torch.as_tensor([0.0, 0.0, 0.0]).
            axis (str, optional): rotation axis, one of ['x', 'y', 'z']. Defaults to 'z'.

        Raises:
            ValueError: unknown rotation axis

        Returns:
            :class:`StructDiscretized3D`: copy of structure with rotated geometry
        """
        _struct_rotated = self.copy()
        center = center.to(dtype=DTYPE_FLOAT, device=self.device)

        if axis.lower() == "x":
            rot = rotation_x(alpha, device=self.device)
        elif axis.lower() == "y":
            rot = rotation_y(alpha, device=self.device)
        elif axis.lower() == "z":
            rot = rotation_z(alpha, device=self.device)
        else:
            raise ValueError("Unknown rotation axis ''.".format(axis))

        if len(_struct_rotated.positions) > 1:
            _struct_rotated.positions = torch.matmul(
                _struct_rotated.positions - (center + self.r0), rot
            ) + (center + self.r0)
        else:
            warnings.warn("Single meshpoint found, ignore rotation.")

        return _struct_rotated


class StructDiscretizedCubic3D(StructDiscretized3D):
    """class for cubic volume discretized structure

    Defines the cubic volume discretization, polarizabilities and self-terms
    """

    __name__ = "3D cubic discretized structure class"

    def __init__(
        self,
        discretization_config,
        step,
        materials,
        device: torch.device = None,
        **kwargs,
    ):
        """3D structure, discretized on a cubic lattice

        Args:
            discretization_config (tuple): tuple of discretization condition function, and discretizer walk limits (as provided by the geometries generators)
            step (float, optional): nominal stepsize. If not provided, infer automatically from geometry. Defaults to None.
            materials (material class, or list of them): material of structure. If list, define the material of each meshpoint.
            device (torch.device, optional): Defaults to "cpu" (can be changed by :func:`torchgdm.use_cuda`).

        Raises:
            ValueError: Invalid material config
        """
        from torchgdm.struct.volume import discretizer_cubic

        positions = discretizer_cubic(*discretization_config, step=step)

        super().__init__(positions, materials, step=step, device=device, **kwargs)

        self.mesh = "cubic"
        self.mesh_normalization_factor = torch.tensor(
            1.0, dtype=DTYPE_FLOAT, device=self.device
        )


class StructDiscretizedHexagonal3D(StructDiscretized3D):
    """class for hexagonal compact volume discretized structure

    Defines the hexagonal compact volume discretization, polarizabilities and self-terms
    """

    __name__ = "3D hexagonal compact discretized structure class"

    def __init__(
        self,
        discretization_config,
        step,
        materials,
        device: torch.device = None,
        **kwargs,
    ):
        """3D structure, discretized on a hexagonal compact lattice

        Args:
            discretization_config (tuple): tuple of discretization condition function, and discretizer walk limits (as provided by the geometries generators)
            step (float, optional): nominal stepsize. If not provided, infer automatically from geometry. Defaults to None.
            materials (material class, or list of them): material of structure. If list, define the material of each meshpoint.
            device (torch.device, optional): Defaults to "cpu" (can be changed by :func:`torchgdm.use_cuda`).

        Raises:
            ValueError: Invalid material config
        """
        from torchgdm.struct.volume import discretizer_hexagonalcompact

        positions = discretizer_hexagonalcompact(*discretization_config, step=step)

        super().__init__(positions, materials, step=step, device=device, **kwargs)

        self.mesh = "hexagonal"
        self.mesh_normalization_factor = torch.sqrt(
            torch.as_tensor(2.0, dtype=DTYPE_FLOAT, device=self.device)
        )


def extract_eff_pola_via_mp_decomposition(
    struct,
    environment,
    wavelengths,
    long_wavelength_approx=False,
    n_dipoles=None,
    distance_dipoles=5000,
    verbose=True,
    only_pE_mH=True,
    progress_bar=True,
    device=None,
    batch_size=16,
    **kwargs,
):
    """Extract effective electric and magnetic dipole polarizability for volume discretized structure

    Extract the polarizability for the structure `struct` in a given `environement`
    at the specified `wavelengths`

    solve inverse problem of adjusting polarizability for different illuminations
    via pseudoinverse

    By default, use 14 plane waves (different incidence directions and polarizations).
    alternative: illumination with `n_dipoles` point-dipole sources if `n_dipoles` is an integer > 0.


    Args:
        struct (class:`StructDiscretized3D`): the discretized structure to extract the model for.
        environment (environment class): 3D environement class.
        wavelengths (torch.Tensor): list of wavelengths to extract the model at. in nm.
        long_wavelength_approx (bool, optional): If True, use long wavelength approximation for dupole extraction. Defaults to False.
        n_dipoles (int, optional): If given, use `n` dipole sources as illumination instead of plane waves. Defaults to None.
        distance_dipoles (int, optional): if using dipoles, specify their distance to the center of gravity. Defaults to 5000.
        verbose (bool, optional): whether to sprint progess info. Defaults to True.
        only_pE_mH (bool, optional): whether to extract only a p/m model (True) or a full (6x6) polarizability (False). Defaults to True.
        progress_bar (bool, optional): whether to show a progress bar. Defaults to True.
        device (str, optional). Defaults to None, in which case the structure's device is used.

    Returns:
        dict: contains all informations about the effective dipole polarizability model
    """
    from torchgdm.env.freespace_3d.inc_fields import ElectricDipole, PlaneWave
    from torchgdm.simulation import Simulation
    from torchgdm.postproc.multipole import decomposition_exact
    from torchgdm.tools.geometry import get_enclosing_sphere_radius
    from torchgdm.tools.misc import tqdm

    if verbose:
        import time
    _struct = struct.copy()

    if device is None:
        device = _struct.device
    else:
        struct.set_device(device)

    # convert single wavelength to list
    wavelengths = torch.as_tensor(wavelengths, dtype=DTYPE_FLOAT, device=device)
    wavelengths = torch.atleast_1d(wavelengths)

    # use first order multipole moments (propto local field)
    which_moment_p = "ed_1"
    which_moment_m = "md"
    enclosing_radius = get_enclosing_sphere_radius(_struct.positions)
    r_sphere = enclosing_radius + distance_dipoles
    r0 = struct.get_center_of_mass()

    # setup perpendicular plane waves illuminations
    if n_dipoles is None:
        pw_conf_list = [
            [0.0, 1.0, 0, "xz"],  # E-x, H-y, k-z
            [1.0, 0.0, 0, "xz"],  # E-y, H-x, k-z
            #
            [1.0, 0.0, torch.pi / 2.0, "xz"],  # E-x, H-z, k-y
            [0.0, 1.0, torch.pi / 2.0, "xz"],  # E-z, H-x, k-y
            #
            [1.0, 0.0, torch.pi / 2.0, "yz"],  # E-y, H-z, k-x
            [0.0, 1.0, torch.pi / 2.0, "yz"],  # E-z, H-y, k-x
            #
            [1.0, 0.0, -torch.pi / 2.0, "xz"],  # E-x, H-z, -k-y
            [0.0, 1.0, -torch.pi / 2.0, "xz"],  # E-z, H-x, -k-y
            #
            [1.0, 0.0, -torch.pi / 2.0, "yz"],  # E-y, H-z, -k-x
            [0.0, 1.0, -torch.pi / 2.0, "yz"],  # E-z, H-y, -k-x
            #
            [1.0, 0.0, torch.pi / 4.0, "xz"],  # oblique
            [0.0, 1.0, torch.pi / 4.0, "yz"],  # oblique
            #
            [0.0, 1.0, -torch.pi / 4.0, "xz"],  # oblique, opposite
            [1.0, 0.0, -torch.pi / 4.0, "yz"],  # oblique, opposite
        ]
        e_inc_list = [
            PlaneWave(e0s=a, e0p=b, inc_angle=c, inc_plane=d, device=device)
            for [a, b, c, d] in pw_conf_list
        ]
    # optional: multiple dipole illuminations
    else:
        if n_dipoles <= 0 or type(n_dipoles) != int:
            raise ValueError(
                "dipole illumination mode: `n_dipoles` needs to be a positive integer."
            )

        # setup dipoles of random position and random orientation
        rnd_pos = sample_random_spherical(n_dipoles) * r_sphere
        e_inc_list = [
            ElectricDipole(
                r_source=r_dp,
                p_source=torch.rand(3, device=device) * r_sphere,
                device=device,
            )
            for r_dp in rnd_pos
        ]

    # replace illumination
    _sim = Simulation(
        structures=[_struct],
        environment=environment,
        illumination_fields=e_inc_list,
        wavelengths=wavelengths,
        device=device,
    )

    if verbose:
        t0 = time.time()
        _pos_p, _pos_m = _sim._get_polarizable_positions_separate_p_m()
        n_dp = len(_pos_p) + len(_pos_m)
        n_wl = len(wavelengths)
        print("Running simulation ({} dipoles, {} wls)... ".format(n_dp, n_wl), end="")
    _sim.run(verbose=False, progress_bar=progress_bar, batch_size=batch_size)

    if verbose and not progress_bar:
        print("Done in {:.2f}s.".format(time.time() - t0))

    # solve the optimization problem
    alpha_6x6 = torch.zeros(
        (len(wavelengths), 6, 6), dtype=DTYPE_COMPLEX, device=device
    )
    if verbose:
        t0 = time.time()
        print("Running p/m optimization... ", end="")

    for i_wl in tqdm(range(len(wavelengths)), progress_bar, title=""):
        wl = wavelengths[i_wl]

        # multipole expansion for all illuminations
        mp_dict = decomposition_exact(
            _sim,
            wl,
            long_wavelength_approx=long_wavelength_approx,
        )
        p_eval = mp_dict[which_moment_p]
        m_eval = mp_dict[which_moment_m]

        # illuminating fields at expansion location
        e0_eval = torch.zeros((len(e_inc_list), 3), dtype=DTYPE_COMPLEX, device=device)
        h0_eval = torch.zeros((len(e_inc_list), 3), dtype=DTYPE_COMPLEX, device=device)
        for i_field, e_inc in enumerate(e_inc_list):
            e0 = e_inc.get_efield(r0.unsqueeze(0), wl, environment)
            e0_eval[i_field] = e0
            h0 = e_inc.get_hfield(r0.unsqueeze(0), wl, environment)
            eps_env = environment.get_environment_permittivity_scalar(wl, r0)
            h0_eval[i_field] = h0

        # --- full 6x6 polarizability
        if not only_pE_mH:
            # pseudo-inverse of all illuminations
            f0_eval = torch.cat([e0_eval, h0_eval], dim=1)
            pinv_f0 = torch.linalg.pinv(f0_eval)

            # optimum alphas to obtain dipole moments for each illumination
            pm_eval = torch.cat([p_eval, m_eval], dim=1)
            alpha_6x6_inv = torch.matmul(pinv_f0, pm_eval)
            alpha_6x6[i_wl] = alpha_6x6_inv

            # test residuals
            _test_residual_effective_polarizability(
                _struct,
                wl,
                environment,
                alpha_6x6_inv,
                f0_eval,
                pm_eval,
                text_which_dp="6x6 dipole",
            )

        # --- only pE and mH
        if only_pE_mH:
            # pseudo-inverse of all illuminations
            pinv_e0 = torch.linalg.pinv(e0_eval)
            pinv_h0 = torch.linalg.pinv(h0_eval)

            # optimum alphas to obtain dipole moments for each illumination
            alpha_pinv = torch.matmul(pinv_e0, p_eval)
            alpha_minv = torch.matmul(pinv_h0, m_eval)

            alpha_6x6[i_wl, :3, :3] = alpha_pinv
            alpha_6x6[i_wl, 3:, 3:] = alpha_minv

            # test residuals
            _test_residual_effective_polarizability(
                _struct,
                wl,
                environment,
                alpha_pinv,
                e0_eval,
                p_eval,
                text_which_dp="electric dipole",
            )
            _test_residual_effective_polarizability(
                _struct,
                wl,
                environment,
                alpha_minv,
                h0_eval,
                m_eval,
                text_which_dp="magnetic dipole",
            )

    if verbose:
        print("Done in {:.2f}s.".format(time.time() - t0))

    dict_pola_pseudo = dict(
        r0=r0,
        r0_MD=r0,
        r0_ED=r0,
        full_geometry=_struct.positions,
        alpha_6x6=alpha_6x6,
        wavelengths=wavelengths,
        enclosing_radius=enclosing_radius,
        k0_spectrum=2 * torch.pi / wavelengths,
    )
    return dict_pola_pseudo


def extract_eff_pola_via_propagation(
    struct,
    environment,
    wavelengths,
    n_probe=150,
    distance_probe=10.0,
    n_dipoles=None,
    distance_dipoles=5000,
    verbose=True,
    only_pE_mH=False,
    progress_bar=True,
    device=None,
):
    """Extract effective electric and magnetic dipole polarizability for volume discretized structure

    Extract the polarizability for the structure `struct` in a given `environement`
    at the specified `wavelengths`

    In this version, the effective dipole response for several illuminations is obtained
    via matching on a circumscribing sphere by solving of a first inverse problem via pseudoinverse.

    The second inverse problem of adjusting polarizability for different
    illuminations is also solved via pseudoinverse.

    By default, use 14 plane waves (different incidence directions and polarizations).
    alternative: illumination with `n_dipoles` point-dipole sources if `n_dipoles` is an integer > 0.


    Args:
        struct (class:`StructDiscretized3D`): the discretized structure to extract the model for.
        environment (environment class): 3D environement class.
        wavelengths (torch.Tensor): list of wavelengths to extract the model at. in nm.
        n_probe (int, optional): number of probe positions on enclosing sphere. Defaults to 100.
        distance_probe (float, optional): additional distance to enclosing sphere in units of discretization step. Defaults to 2.0.
        n_dipoles (int, optional): If given, use `n` dipole sources as illumination instead of plane waves. Defaults to None.
        distance_dipoles (int, optional): if using dipoles, specify their distance to the center of gravity. Defaults to 5000.
        verbose (bool, optional): whether to sprint progess info. Defaults to True.
        only_pE_mH (bool, optional): whether to extract only a p/m model (True) or a full (6x6) polarizability (False). Defaults to True.
        progress_bar (bool, optional): whether to show a progress bar. Defaults to True.
        device (str, optional). Defaults to None, in which case the structure's device is used.

    Returns:
        dict: contains all informations about the effective dipole polarizability model
    """
    from torchgdm.env.freespace_3d.inc_fields import ElectricDipole, PlaneWave
    from torchgdm.simulation import Simulation
    from torchgdm.postproc.fields import nf
    from torchgdm.tools.geometry import get_enclosing_sphere_radius
    from torchgdm.tools.misc import tqdm

    if verbose:
        import time
    _struct = struct.copy()

    if device is None:
        device = _struct.device
    else:
        struct.set_device(device)

    # convert single wavelength to list
    wavelengths = torch.as_tensor(wavelengths, dtype=DTYPE_FLOAT, device=device)
    wavelengths = torch.atleast_1d(wavelengths)

    # use first order multipole moments (propto local field)
    step_max = torch.max(struct.step)
    enclosing_radius = get_enclosing_sphere_radius(_struct.positions)
    illumination_radius = enclosing_radius + distance_dipoles
    probe_radius = enclosing_radius + distance_probe * step_max
    r0 = struct.get_center_of_mass()

    # setup perpendicular plane waves illuminations
    if n_dipoles is None:
        pw_conf_list = [
            [0.0, 1.0, 0, "xz"],  # E-x, H-y, k-z
            [1.0, 0.0, 0, "xz"],  # E-y, H-x, k-z
            #
            [1.0, 0.0, torch.pi / 2.0, "xz"],  # E-x, H-z, k-y
            [0.0, 1.0, torch.pi / 2.0, "xz"],  # E-z, H-x, k-y
            #
            [1.0, 0.0, torch.pi / 2.0, "yz"],  # E-y, H-z, k-x
            [0.0, 1.0, torch.pi / 2.0, "yz"],  # E-z, H-y, k-x
            #
            [1.0, 0.0, -torch.pi / 2.0, "xz"],  # E-x, H-z, -k-y
            [0.0, 1.0, -torch.pi / 2.0, "xz"],  # E-z, H-x, -k-y
            #
            [1.0, 0.0, -torch.pi / 2.0, "yz"],  # E-y, H-z, -k-x
            [0.0, 1.0, -torch.pi / 2.0, "yz"],  # E-z, H-y, -k-x
            #
            [1.0, 0.0, torch.pi / 4.0, "xz"],  # oblique
            [0.0, 1.0, torch.pi / 4.0, "yz"],  # oblique
            #
            [0.0, 1.0, -torch.pi / 4.0, "xz"],  # oblique, opposite
            [1.0, 0.0, -torch.pi / 4.0, "yz"],  # oblique, opposite
        ]
        e_inc_extract = [
            PlaneWave(e0s=a, e0p=b, inc_angle=c, inc_plane=d, device=device)
            for [a, b, c, d] in pw_conf_list
        ]
    # optional: multiple dipole illuminations
    else:
        if n_dipoles <= 0 or type(n_dipoles) != int:
            raise ValueError(
                "dipole illumination mode: `n_dipoles` needs to be a positive integer."
            )

        # setup dipoles of random position and random orientation
        rnd_pos_dp = sample_random_spherical(n_dipoles) * illumination_radius
        e_inc_extract = [
            ElectricDipole(
                r_source=r_dp,
                p_source=torch.rand(3, device=device) * illumination_radius,
                device=device,
            )
            for r_dp in rnd_pos_dp
        ]

    # setup field probe positions on enclosing sphere
    r_probe = sample_random_spherical(n_probe) * probe_radius

    # replace illumination
    _sim = Simulation(
        structures=[_struct],
        environment=environment,
        illumination_fields=e_inc_extract,
        wavelengths=wavelengths,
        device=device,
    )

    if verbose:
        t0 = time.time()
        _pos_p, _pos_m = _sim._get_polarizable_positions_separate_p_m()
        n_dp = len(_pos_p) + len(_pos_m)
        n_wl = len(wavelengths)
        print("Running simulation ({} dipoles, {} wls)... ".format(n_dp, n_wl), end="")
    _sim.run(verbose=False, progress_bar=progress_bar)

    if verbose and not progress_bar:
        print("Done in {:.2f}s.".format(time.time() - t0))

    # solve the optimization problem
    alpha_6x6 = torch.zeros(
        (len(wavelengths), 6, 6), dtype=DTYPE_COMPLEX, device=device
    )
    if verbose:
        t0 = time.time()
        print("Running p/m optimization... ", end="")

    for i_wl in tqdm(range(len(wavelengths)), progress_bar, title=""):
        wl = wavelengths[i_wl]

        # calculate fields on enclosing sphere for all illuminations
        # shape: (n_illumination, n_probe*6)
        nf_probe = nf(_sim, wl, r_probe=r_probe, progress_bar=False)
        e_eval = nf_probe["sca"].get_efield()
        h_eval = nf_probe["sca"].get_hfield()
        f_eval = torch.cat([e_eval, h_eval], dim=2)
        f_eval = f_eval.reshape(len(e_inc_extract), -1)

        # illuminating fields at expansion location
        # shape: (n_illumination, 6)
        e0_eval = torch.zeros(
            (len(e_inc_extract), 3), dtype=DTYPE_COMPLEX, device=device
        )
        h0_eval = torch.zeros(
            (len(e_inc_extract), 3), dtype=DTYPE_COMPLEX, device=device
        )
        for i_field, e_inc in enumerate(e_inc_extract):
            e0 = e_inc.get_efield(r0.unsqueeze(0), wl, environment)
            e0_eval[i_field] = e0
            h0 = e_inc.get_hfield(r0.unsqueeze(0), wl, environment)
            eps_env = environment.get_environment_permittivity_scalar(wl, r0)
            h0_eval[i_field] = h0
        f0_eval = torch.cat([e0_eval, h0_eval], dim=1)

        # --- full 6x6 polarizability
        if not only_pE_mH:
            # calculate Green's tensors between r0 and r_probe
            # shape: (n_probe*6, 6)
            G_6x6 = environment.get_G_6x6(r_probe=r_probe, r_source=r0, wavelength=wl)
            G_all = G_6x6.reshape(-1, 6)

            # inv. problem #1: probe fields + Green's tensors --> dipole moments
            Gi = torch.linalg.pinv(G_all)
            pm_eff = torch.matmul(Gi.unsqueeze(0), f_eval.unsqueeze(-1))[..., 0]

            # inv. problem #2: dipole moments + illumination --> effective pola
            pinv_f0 = torch.linalg.pinv(f0_eval)
            alpha_6x6_inv = torch.matmul(pinv_f0, pm_eff)

            # optimum alphas to obtain dipole moments for each illumination
            alpha_6x6[i_wl] = alpha_6x6_inv

            # test residuals
            _test_residual_effective_polarizability(
                _struct,
                wl,
                environment,
                alpha_6x6_inv,
                f0_eval,
                pm_eff,
                text_which_dp="6x6 dipole",
            )

        # --- only pE and mH
        if only_pE_mH:
            # calculate Green's tensors between r0 and r_probe
            # shape: (n_probe*6, 6)
            G_Ep = environment.get_G_Ep(r_probe=r_probe, r_source=r0, wavelength=wl)
            G_Hm = environment.get_G_Hm(r_probe=r_probe, r_source=r0, wavelength=wl)
            G_Ep_all = G_Ep.reshape(-1, 3)
            G_Hm_all = G_Hm.reshape(-1, 3)

            e_eval = e_eval.reshape(len(e_inc_extract), -1)
            h_eval = h_eval.reshape(len(e_inc_extract), -1)

            # inv. problem #1: probe fields + Green's tensors --> dipole moments
            G_Ep_i = torch.linalg.pinv(G_Ep_all)
            G_Hm_i = torch.linalg.pinv(G_Hm_all)
            p_eff = torch.matmul(G_Ep_i.unsqueeze(0), e_eval.unsqueeze(-1))[..., 0]
            m_eff = torch.matmul(G_Hm_i.unsqueeze(0), h_eval.unsqueeze(-1))[..., 0]

            # pseudo-inverse of all illuminations
            pinv_e0 = torch.linalg.pinv(e0_eval)
            pinv_h0 = torch.linalg.pinv(h0_eval)

            # optimum alphas to obtain dipole moments for each illumination
            alpha_pinv = torch.matmul(pinv_e0, p_eff)
            alpha_minv = torch.matmul(pinv_h0, m_eff)

            alpha_6x6[i_wl, :3, :3] = alpha_pinv
            alpha_6x6[i_wl, 3:, 3:] = alpha_minv

            # test residuals
            _test_residual_effective_polarizability(
                _struct,
                wl,
                environment,
                alpha_pinv,
                e0_eval,
                p_eff,
                text_which_dp="electric dipole",
            )
            _test_residual_effective_polarizability(
                _struct,
                wl,
                environment,
                alpha_minv,
                h0_eval,
                m_eff,
                text_which_dp="magnetic dipole",
            )

    if verbose:
        print("Done in {:.2f}s.".format(time.time() - t0))

    dict_pola_pseudo = dict(
        r0=r0,
        r0_MD=r0,
        r0_ED=r0,
        full_geometry=_struct.positions,
        alpha_6x6=alpha_6x6,
        wavelengths=wavelengths,
        enclosing_radius=enclosing_radius,
        k0_spectrum=2 * torch.pi / wavelengths,
    )

    return dict_pola_pseudo


def _test_residual_effective_polarizability(
    _struct,
    wavelength,
    environment,
    alpha_eff,
    f0,
    dp_moments,
    text_which_dp="",
    residual_warning_threshold=0.25,
):
    # --- test - calculate mean residuals for accuracy estimation
    epsilon_dpm = torch.abs(
        _struct.get_polarizability_6x6(wavelength=wavelength, environment=environment)
    ).max()  # add a single mesh-cell polarizability as epsilon to relative error test

    res_p = torch.abs(dp_moments - torch.matmul(alpha_eff, f0.T).T)
    norm_p = torch.linalg.norm(dp_moments, dim=-1).unsqueeze(1) + epsilon_dpm

    if torch.max(res_p / norm_p) > residual_warning_threshold:
        print(
            "Warning: wl={}nm - eff. {} pola. peak residual is exceeing the threshold! ({:.4f} > {:.2f})".format(
                wavelength,
                text_which_dp,
                torch.max(res_p / norm_p),
                residual_warning_threshold,
            )
        )


def test_effective_polarizability_accuracy(
    struct_alpha,
    struct_full,
    test_yz_incidence=True,
    environment=None,
    rtol=0.10,
    verbose=True,
    progress_bar=False,
    device=None,
):
    """test effective polarizability model in a scattering simulation

    Print some information about model accuracy

    Args:
        struct_alpha (torchgdm.struct.point.StructEffPola3D): effective polarizability structure
        struct_full (StructDiscretized3D): associated full discretization structure as reference
        test_yz_incidence (bool, optional): Whether to test also YZ incident plane. Defaults to True.
        environment (3D env. class, optional): Simulation environment. If None, use environment from effective dipole model structure. Defaults to None.
        rtol (float, optional): relative error threshold for raising warnings. Defaults to 0.10.
        verbose (bool, optional): Print detailed info. Defaults to True.
        progress_bar (bool, optional): Show progress bars. Defaults to False.
        device (str, optional): If None, use structure's device. Defaults to None.

    """
    from torchgdm.tools.batch import calc_spectrum
    from torchgdm.postproc import crosssect
    from torchgdm.env.freespace_3d.inc_fields import PlaneWave
    from torchgdm.simulation import Simulation
    from torchgdm.tools.misc import to_np

    if environment is None:
        if struct_alpha.environment is None:
            raise ValueError(
                "Structure does not contain environement definition, "
                + "and no environemnt has been specified. Please provide the environment."
            )
        environment = struct_alpha.environment

    if device is None:
        device = struct_alpha.device

    wavelengths = struct_alpha.wavelengths_data

    # test configs: plane wave, s/p-polarization, 0/90 deg incidence
    e_inc_list = [
        PlaneWave(e0p=1.0, e0s=0.0, inc_angle=0),
        PlaneWave(e0p=0.0, e0s=1.0, inc_angle=0),
        PlaneWave(e0p=1.0, e0s=0.0, inc_angle=torch.pi / 2),
        PlaneWave(e0p=0.0, e0s=1.0, inc_angle=torch.pi / 2),
    ]
    if test_yz_incidence:
        e_inc_list += [
            PlaneWave(e0p=1.0, e0s=0.0, inc_plane="yz", inc_angle=torch.pi / 2),
            PlaneWave(e0p=0.0, e0s=1.0, inc_plane="yz", inc_angle=torch.pi / 2),
        ]

    # setup a discretized and a effective dipole pair simulation
    sim_alpha = Simulation(
        structures=[struct_alpha],
        environment=environment,
        illumination_fields=e_inc_list,
        wavelengths=wavelengths,
        device=device,
    )
    sim_discr = Simulation(
        structures=[struct_full],
        environment=environment,
        illumination_fields=e_inc_list,
        wavelengths=wavelengths,
        device=device,
    )

    # run simulations and calc. cross section spectra
    if verbose:
        print("-" * 60)
        print("Testing effective polarizability vs. discretized simulation.")

    sim_alpha.run(verbose=False, progress_bar=progress_bar)
    cs_alpha = calc_spectrum(sim_alpha, crosssect.total, progress_bar=progress_bar)

    sim_discr.run(verbose=False, progress_bar=progress_bar)
    cs_discr = calc_spectrum(sim_discr, crosssect.total, progress_bar=progress_bar)

    # calculate errors
    for k in ["scs", "ecs"]:
        try:
            rel_diff = (cs_discr[k] - cs_alpha[k]) / ((cs_discr[k] + cs_alpha[k]))
            mean_rel_error = torch.mean(torch.abs(rel_diff))
            peak_rel_error = torch.max(torch.abs(rel_diff))
            if verbose:
                print("'{}':".format(k))
                print("    - mean rel. error: {:.3f}".format(to_np(mean_rel_error)))
                print("    - peak rel. error: {:.3f}".format(to_np(peak_rel_error)))
            if mean_rel_error > rtol:
                warnings.warn(
                    "'{}': Effective polarizability mean relative error larger than tolerance ({:.3f} > {:.3f})".format(
                        k, mean_rel_error, rtol
                    )
                )

            elif peak_rel_error > rtol:
                warnings.warn(
                    "'{}': Effective polarizability peak relative error larger than tolerance ({:.3f} > {:.3f})".format(
                        k, peak_rel_error, rtol
                    )
                )

        except TypeError:
            pass
    if verbose:
        print("-" * 60)


# %% --- test
if __name__ == "__main__":
    import torchgdm as tg

    device = "cpu"
    # device = "cuda"

    # --- setup test case simulation
    # - illumination field(s)
    wavelengths = torch.tensor([650.0])
    wavelengths = torch.linspace(500, 800, 21)

    # - environment
    eps_env = 1.0
    mat_env = tg.materials.MatConstant(eps_env)
    env = tg.env.freespace_3d.EnvHomogeneous3D(env_material=mat_env)

    # - dummy illumination field
    e_inc_dummy = tg.env.freespace_3d.PlaneWave(inc_angle=torch.pi / 4)

    # - first structure: volume discretization
    l = 8
    w = 4
    h = 4
    step = 20.0
    mat_struct = tg.materials.MatConstant(eps=10.0)
    mat_struct = tg.materials.MatDatabase("Ge")
    geometry = tg.struct.volume.discretizer_cubic(
        *tg.struct.volume.cuboid(l, w, h), step=step
    )
    # geometry = tg.struct.volume.discretizer_hexagonalcompact(
    #     *tg.struct.volume.split_ring(r_in=9, r_out=12, h=2, alpha_g=torch.pi/8), step=step
    # )

    struct_mesh = tg.struct.StructDiscretized3D(geometry, mat_struct)
    # struct_mesh2 = struct_mesh.rotate(torch.pi / 2)
    # struct_mesh = struct_mesh + (struct_mesh2 + [(w) / 2 * step, (l + w) / 2 * step, 0])
    struct_mesh.plot()

    struct_alpha_pE_mH = struct_mesh.convert_to_effective_polarizability_pair(
        env, wavelengths, only_pE_mH=True, test_accuracy=True
    )
    struct_alpha_6x6 = struct_mesh.convert_to_effective_polarizability_pair(
        env, wavelengths, only_pE_mH=False, test_accuracy=True
    )

    # - full simulation
    sim_full = tg.simulation.Simulation(
        structures=[struct_mesh],
        environment=env,
        illumination_fields=[e_inc_dummy],
        wavelengths=wavelengths,
        device=device,
    )

    alpha_pm_test = struct_alpha_pE_mH.get_polarizability_6x6(wavelengths[0], env)
    alpha_66_test = struct_alpha_6x6.get_polarizability_6x6(wavelengths[0], env)
    # %%
    import matplotlib.pyplot as plt

    plt.figure(figsize=(8, 8))
    plt.subplot(221)
    plt.imshow(alpha_pm_test[0].real)
    plt.colorbar()
    plt.subplot(222)
    plt.imshow(alpha_pm_test[0].imag)
    plt.colorbar()

    plt.subplot(223)
    plt.imshow(alpha_66_test[0].real)
    plt.colorbar()
    plt.subplot(224)
    plt.imshow(alpha_66_test[0].imag)
    plt.colorbar()
    plt.show()
    # %%
    sim_pEmH = tg.simulation.Simulation(
        structures=[struct_alpha_pE_mH],
        environment=env,
        illumination_fields=[e_inc_dummy],
        wavelengths=wavelengths,
        device=device,
    )
    sim_6x6 = tg.simulation.Simulation(
        structures=[struct_alpha_6x6],
        environment=env,
        illumination_fields=[e_inc_dummy],
        wavelengths=wavelengths,
        device=device,
    )
    sim_full.run()
    sim_pEmH.run()
    sim_6x6.run()

    cs_f = sim_full.get_spectra_scs()
    cs_pm = sim_pEmH.get_spectra_scs()
    cs_66 = sim_6x6.get_spectra_scs()
    plt.plot(wavelengths, cs_f["scs"], label="scs-full")
    plt.plot(wavelengths, cs_pm["scs"], label="scs-pm")
    plt.plot(wavelengths, cs_66["scs"], label="scs-6x6")
    plt.legend()
    plt.show()
# %%
# print(sim_full.get_spectra_scs())
# print(sim_pEmH.get_spectra_scs())
# print(sim_6x6.get_spectra_scs())

# %%
