# -*- coding: utf-8 -*-
"""volume discretization structure class
"""
import warnings

import torch

from torchgdm.constants import (
    DTYPE_FLOAT,
    DTYPE_COMPLEX,
    COLORS_DEFAULT,
)
from torchgdm.tools.misc import get_default_device
from torchgdm.struct.base_classes import StructBase
from torchgdm.tools.geometry import get_step_from_geometry
from torchgdm.tools.geometry import sample_random_circular
from torchgdm.tools.geometry import rotation_y
from torchgdm.tools.misc import ptp


class StructDiscretized2D(StructBase):
    """base class 2D surface discretized structure with infinite axis

    Defines the 2D surface discretization, its polarizabilities and self-terms
    """

    __name__ = "2D discretized structure"

    def __init__(
        self,
        positions: torch.Tensor,
        materials,
        step=None,
        device: torch.device = None,
        **kwargs
    ):
        """2D discretized structure

        Args:
            positions (torch.Tensor): meshpoint positions (3D, but all y values must be zero)
            materials (material class, or list of them): material of structure. If list, define the material of each meshpoint.
            step (float, optional): nominal stepsize. If not provided, infer automatically from geometry. Defaults to None.
            device (torch.device, optional): Defaults to "cpu" (can be changed by :func:`torchgdm.use_cuda`).

        Raises:
            ValueError: No mesh points at y=0, Invalid material config
        """
        super().__init__(device=device, **kwargs)
        self.mesh = "2D"
        self.n_dim = 2

        self.positions = torch.as_tensor(
            positions, dtype=DTYPE_FLOAT, device=self.device
        )
        if torch.count_nonzero(self.positions[..., 1]) > 0:
            warnings.warn("2D structure. Remove all positions with y!=0.")
            self.positions = self.positions[self.positions[..., 1] != 0]
            if len(self.positions) == 0:
                raise ValueError("No mesh positions at y=0. Please check geometry.")

        self.r0 = self.get_center_of_mass()  # center of gravity

        if step is None:
            step_scalar = get_step_from_geometry(self.positions)
        else:
            step_scalar = step

        # step for every meshcell, for consistency with other struct classes
        self.step = step_scalar * torch.ones(
            len(self.positions), dtype=DTYPE_FLOAT, device=self.device
        )

        self.radiative_correction = False  # not implemented
        self.mesh_normalization_factor = torch.as_tensor(
            1, dtype=DTYPE_FLOAT, device=self.device
        )  # square mesh

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
        out_str += "------ discretized 2D nano-object -------"
        out_str += "\n" + " mesh type:              {}".format(self.mesh)
        out_str += "\n" + " nr. of meshpoints:      {}".format(len(self.positions))
        out_str += "\n" + " nominal stepsizes (nm): {}".format(
            [float(f) for f in torch.unique(self.step)]
        )
        out_str += "\n" + " material:               {}".format(
            [m.__name__ for m in set(self.materials)]
        )
        bnds = ptp(self.positions, dim=0)
        out_str += "\n" + " size & position (Y-axis is infinite):"
        out_str += "\n" + "     X-extension          :   {:.1f} (nm)".format(bnds[0])
        out_str += "\n" + "     Z-extension          :   {:.1f} (nm)".format(bnds[2])
        out_str += "\n" + "     center of mass (x,z) : ({:.1f}, {:.1f})".format(
            self.r0[0], self.r0[2]
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
            environment (environment class): 2D environement class

        Returns:
            torch.Tensor: pE self term tensor
        """
        eps_env = environment.get_environment_permittivity_scalar(
            wavelength, r_probe=self.positions
        )
        # cast env permittivity to real, because hankel only support real args
        eps_env = torch.as_tensor(eps_env, dtype=DTYPE_COMPLEX, device=self.device).real

        k0 = 2 * torch.pi / wavelength
        k02 = k0**2

        if self.mesh_normalization_factor == 0:
            norm_xz = 0
            norm_y = 0
        else:
            from torchgdm.tools.special import H1n

            S = self.step**2
            k0_y = environment.get_k0_y(wavelength)

            kr2 = torch.as_tensor(
                eps_env * k02 - k0_y**2, dtype=DTYPE_FLOAT, device=self.device
            )
            kr = torch.sqrt(kr2)

            h11 = H1n(1, kr * self.step / torch.pi**0.5)
            norm01 = self.step / torch.pi**0.5 * h11 / kr + 2j / (torch.pi * kr**2)

            norm_xz_nonrad = -1 * self.mesh_normalization_factor / (2.0 * S * eps_env)
            norm_xz_rad = 1j * torch.pi * (2 * k02 - kr2 / eps_env) * norm01 / (4 * S)

            norm_y_nonrad = 0
            norm_y_rad = 1j * torch.pi * (k02 - k0_y**2 / eps_env) * norm01 / (2 * S)

            norm_xz = 4.0 * torch.pi * (norm_xz_nonrad + norm_xz_rad)
            norm_y = 4.0 * torch.pi * (norm_y_nonrad + norm_y_rad)

        self_terms_pE = torch.zeros(
            (len(self.positions), 3, 3), dtype=DTYPE_COMPLEX, device=self.device
        )
        self_terms_pE[:, 0, 0] = norm_xz
        self_terms_pE[:, 1, 1] = norm_y
        self_terms_pE[:, 2, 2] = norm_xz

        return self_terms_pE

    # --- polarizabilities
    def get_polarizability_pE(self, wavelength: float, environment) -> torch.Tensor:
        """return list of EE polarizability tensors (3x3) at each meshpoint

        Args:
            wavelength (float): in nm
            environment (environment class): 2D environement class

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

        S_cell_norm = self.step**2 / float(self.mesh_normalization_factor)

        # --- polarizability
        alpha_pE = (
            (eps_geo - eps_env_tensor)
            * S_cell_norm.unsqueeze(1).unsqueeze(1)
            / (4.0 * torch.pi)
        )

        return alpha_pE

    def convert_to_effective_polarizability_pair(
        self, environment, wavelengths, test_accuracy=False, **kwargs
    ):
        from torchgdm.struct import StructEffPola2D
        from torchgdm.struct.volume.pola import test_effective_polarizability_accuracy
        warnings.warn("2D effective polarizabilities only implemented for illumination incidence in XZ plane!")
        
        alpha = extract_eff_pola_via_propagation(
            struct=self, environment=environment, wavelengths=wavelengths, **kwargs
        )
        struct_aeff = StructEffPola2D(
            positions=torch.stack([self.r0]),
            alpha_dicts=[alpha],
            environment=environment,
            device=self.device,
        )

        if test_accuracy:
            test_effective_polarizability_accuracy(struct_aeff, self, test_yz_incidence=False)

        return struct_aeff

    # --- plotting
    def plot(self, **kwargs):
        """plot the structure in XZ plane (2D)"""
        from torchgdm.visu import visu2d

        kwargs["projection"] = "xz"
        im = visu2d.geo2d._plot_structure_discretized(self, **kwargs)
        return im

    def plot_contour(self, **kwargs):
        """plot the structure contour in XZ plane (2D)"""
        from torchgdm.visu import visu2d

        kwargs["projection"] = "xz"
        im = visu2d.geo2d._plot_contour_discretized(self, **kwargs)
        return im

    def plot3d(self, **kwargs):
        """plot the structure in 3D"""
        from torchgdm.visu import visu3d

        warnings.warn(
            "Visualizing a 2D model in 3D will show only meshpoints in the 'XZ' plane."
        )

        return visu3d.geo3d._plot_structure_discretized(self, **kwargs)

    # --- geometry operations
    def rotate(
        self,
        alpha: float,
        center: torch.Tensor = torch.as_tensor([0.0, 0.0, 0.0]),
        axis: str = "y",
    ):
        """rotate the structure

        Args:
            alpha (float): rotation angle (in rad)
            center (torch.Tensor, optional): center of rotation axis. Defaults to torch.as_tensor([0.0, 0.0, 0.0]).
            axis (str, optional): rotation axis. Defaults to "y".

        Raises:
            ValueError: only "y" axis supported in 2D

        Returns:
            :class:`StructDiscretized2D`: copy of structure with rotated geometry
        """
        _struct_rotated = self.copy()
        center = center.to(dtype=DTYPE_FLOAT, device=self.device)

        if axis.lower() == "y":
            rot = rotation_y(alpha, device=self.device)
        else:
            raise ValueError(
                "Only rotation axis 'y' supported in 2D (infinite axis).".format(axis)
            )

        if len(_struct_rotated.positions) > 1:
            _struct_rotated.positions = torch.matmul(
                _struct_rotated.positions - (center + self.r0), rot
            ) + (center + self.r0)
        else:
            warnings.warn("Single meshpoint found, ignore rotation.")

        return _struct_rotated


class StructDiscretizedSquare2D(StructDiscretized2D):
    """class for square surface discretized, infinitely long 2D structure

    Defines the square surface discretization, polarizabilities and self-terms
    """

    __name__ = "2D square lattice discretized structure class"

    def __init__(
        self,
        discretization_config,
        step,
        materials,
        device: torch.device = None,
        **kwargs
    ):
        """2D structure, discretized on a square lattice

        Infinite axis along Y

        Args:
            discretization_config (tuple): tuple of discretization condition function, and discretizer walk limits (as provided by the geometries generators)
            step (float, optional): nominal stepsize. If not provided, infer automatically from geometry. Defaults to None.
            materials (material class, or list of them): material of structure. If list, define the material of each meshpoint.
            device (torch.device, optional): Defaults to "cpu" (can be changed by :func:`torchgdm.use_cuda`).

        Raises:
            ValueError: No mesh points at y=0, Invalid material config
        """
        from torchgdm.struct.surface_2d import discretizer_square

        positions = discretizer_square(*discretization_config, step=step)

        super().__init__(positions, materials, step=step, device=device, **kwargs)

        self.mesh = "square (2D)"
        self.mesh_normalization_factor = torch.tensor(
            1.0, dtype=DTYPE_FLOAT, device=self.device
        )


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
    from torchgdm.env.freespace_2d.inc_fields import ElectricLineDipole, PlaneWave
    from torchgdm.simulation import Simulation
    from torchgdm.postproc.fields import nf
    from torchgdm.tools.geometry import get_enclosing_sphere_radius
    from torchgdm.tools.misc import tqdm
    from torchgdm.struct.volume.pola import _test_residual_effective_polarizability

    if verbose:
        import time
    _struct = struct.copy()

    if device is None:
        device = _struct.device
    else:
        struct.set_device(device)
    
    # convert single wavelength to list
    wavelengths = torch.as_tensor(
        wavelengths, dtype=DTYPE_FLOAT, device=device
    )
    wavelengths = torch.atleast_1d(wavelengths)

    # use first order multipole moments (propto local field)
    step_max = torch.max(struct.step)
    enclosing_radius = get_enclosing_sphere_radius(_struct.positions)
    illumination_radius = enclosing_radius + distance_dipoles
    probe_radius = enclosing_radius + distance_probe * step_max
    r0 = struct.get_center_of_mass()

    # setup perpendicular plane waves illuminations
    if n_dipoles is None:
        angles = torch.linspace(-torch.pi, torch.pi*0.9, 14)
        pw_conf_list = [[1.0, 0.0, angle, "xz"] for angle in angles]
        pw_conf_list += [[0.0, 1.0, angle, "xz"] for angle in angles]
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
        rnd_pos_dp = sample_random_circular(n_dipoles) * illumination_radius
        e_inc_extract = [
            ElectricLineDipole(
                r_source=r_dp,
                p_source=torch.rand(3, device=device) * illumination_radius,
                device=device,
            )
            for r_dp in rnd_pos_dp
        ]

    # setup field probe positions on enclosing sphere
    r_probe = sample_random_circular(n_probe) * probe_radius

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
            e0 = e_inc.get_efield(r0.unsqueeze(0), wl, _sim.environment)
            e0_eval[i_field] = e0
            h0 = e_inc.get_hfield(r0.unsqueeze(0), wl, _sim.environment)
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
        # alpha_pE=alpha_6x6[:, :3, :3],
        # alpha_mH=alpha_6x6[:, 3:, 3:],
        wavelengths=wavelengths,
        enclosing_radius=enclosing_radius,
        k0_spectrum=2 * torch.pi / wavelengths,
    )
    # if not only_pE_mH:
    #     dict_pola_pseudo["alpha_mE"] = alpha_6x6[:, 3:, :3]
    #     dict_pola_pseudo["alpha_pH"] = alpha_6x6[:, :3, 3:]

    return dict_pola_pseudo
