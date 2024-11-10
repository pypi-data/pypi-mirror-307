# -*- coding: utf-8 -*-
"""point polarizability structure class for torchgdm
"""
import warnings
import copy

import torch

from torchgdm.constants import DTYPE_FLOAT, DTYPE_COMPLEX
from torchgdm.tools.misc import get_default_device
from torchgdm.struct.base_classes import StructBase
from torchgdm.struct.point import StructEffPola3D
from torchgdm.tools import interp
from torchgdm.tools.geometry import rotation_x, rotation_y, rotation_z
from torchgdm.tools.geometry import test_structure_distances
from torchgdm.tools.geometry import get_enclosing_sphere_radius
from torchgdm.tools.misc import ptp


# --- base class volume discretized structure container - 3D
class StructEffPola2D(StructEffPola3D):
    """class for 2D line polarizability structure"""

    __name__ = "effective line polarizability (2D) structure class"

    def __init__(
        self,
        positions: torch.Tensor,
        alpha_dicts: list,
        device: torch.device = None,
        environment=None,
        shift_z_to_r0: bool = True,
    ):
        """2D line polarizability class

        The main information is provided in the `alpha_dicts`, which is a list of dicts with the full effective polarizability definitions. Each dict defines one structure and must contain following:
            - 'wavelengths': wavelengths at which the polarizabilities are calculated
            - at least one of: ['alpha_pE', 'alpha_mH', 'alpha_mE', 'alpha_pH']:
                polarizability tensors of shape [len(wavelengths), 3, 3]
            optional keys:
            - 'full_geometry': the original volume discretization of the represented geometry
            - 'r0': the origin of the effective polarizabilities with respect to optional 'full_geometry'
            - 'enclosing_radius': enclosing radius of original structure

        Args:
            positions (torch.Tensor): polarizability positions (3D, but all y values must be zero)
            alpha_dicts (list): list of polarizability model dictionaries
            device (torch.device, optional): Defaults to "cpu".
            environment (_type_, optional): 3D environment class. Defaults to None.
            shift_z_to_r0 (bool, optional): If True, if a position z-value is zero, each polarizability model's z position will be shifted to the height of the effective dipole development center. Defaults to True.

        Raises:
            ValueError: _description_
        """
        if device is None:
            self.device = get_default_device()
        else:
            self.device = device

        # expand positions, put single scatterer in list
        _positions = torch.as_tensor(positions, dtype=DTYPE_FLOAT, device=self.device)
        if len(_positions.shape) == 1:
            assert len(_positions) == 3
            _positions = _positions.unsqueeze(0)

        if torch.count_nonzero(_positions[..., 1]) > 0:
            warnings.warn("2D structure. Remove all positions with y!=0.")
            _positions = _positions[_positions[..., 1] != 0]
            if len(_positions) == 0:
                raise ValueError("No mesh positions at y=0. Please check geometry.")

        super().__init__(
            positions=positions,
            alpha_dicts=alpha_dicts,
            environment=environment,
            shift_z_to_r0=shift_z_to_r0,
            device=device,
        )
        self.n_dim = 2

    def __repr__(self, verbose=False):
        """description about structure"""
        out_str = ""
        out_str += (
            "------ 2D effective ED / MD line-dipole polarizabilities object -------"
        )
        out_str += "\n" + " nr. of dipole-pairs:    {}".format(
            len(self.get_all_positions())
        )
        out_str += "\n" + " nominal enclosing circle diameters (nm): {}".format(
            [round(float(f), 1) for f in torch.unique(self.step)]
        )
        if len(self.full_geometries) > 0:
            pos = torch.cat(self.full_geometries)
            out_str += "\n" + " original 2D geometry: "
            out_str += "\n" + "  - replacing nr. of meshpoints: {}".format(len(pos))
            bnds = ptp(pos, dim=0)
            out_str += "\n" + "  - size & position:"
            out_str += "\n" + "        X-extension    :    {:.1f} (nm)".format(bnds[0])
            out_str += "\n" + "        Z-extension    :    {:.1f} (nm)".format(bnds[2])
            out_str += "\n" + "  - center of mass :    ({:.1f}, {:.1f}, {:.1f})".format(
                *[float(f) for f in self.get_center_of_mass()]
            )

        return out_str

    # --- plotting
    def plot(
        self,
        scale=1.0,
        color="auto",
        linestyle_circle=(0, (2, 2)),
        color_circle="auto",
        color_circle_fill=None,
        alpha=1,
        show_grid=True,
        color_grid="auto",
        alpha_grid=0.25,
        legend=True,
        set_ax_aspect=True,
        reset_color_cycle=True,
        **kwargs
    ):
        """plot the structure of the effective line-polarizability (2D)

        Args:
            scale (float, optional): scaling factor of the grid cells, if shown. Defaults to 1.0.
            color (str, optional): plot color. Defaults to "auto".
            linestyle_circle (tuple, optional): optional line style for enclosing circle. Defaults to (0, (2, 2)).
            color_circle (str, optional): optional alternative color for enclosing circle. Defaults to "auto".
            color_circle_fill (_type_, optional): optional alternative fill color for enclosing circle. Defaults to None.
            alpha (int, optional): optional transparency. Defaults to 1.
            show_grid (bool, optional): whether to show mesh grid (if available in structure). Defaults to True.
            color_grid (str, optional): optional alternative color for the mesh grid. Defaults to "auto".
            alpha_grid (float, optional): optional alternative transparency for the mesh grid. Defaults to 0.25.
            legend (bool, optional): show legend. Defaults to True.
            set_ax_aspect (bool, optional): automatically set aspect ratio to equal. Defaults to True.
            reset_color_cycle (bool, optional): reset color cycle after finishing the plot. Defaults to True.

        Returns:
            matplotlib axes
        """
        from torchgdm.visu import visu2d

        kwargs["projection"] = "xz"
        im = visu2d.geo2d._plot_structure_eff_pola(
            self,
            scale=scale,
            color=color,
            linestyle_circle=linestyle_circle,
            color_circle=color_circle,
            color_circle_fill=color_circle_fill,
            alpha=alpha,
            show_grid=show_grid,
            color_grid=color_grid,
            alpha_grid=alpha_grid,
            legend=legend,
            set_ax_aspect=set_ax_aspect,
            reset_color_cycle=reset_color_cycle,
            **kwargs
        )
        return im

    def plot_contour(
        self,
        color="auto",
        set_ax_aspect=True,
        alpha=1.0,
        alpha_value=None,
        reset_color_cycle=True,
        **kwargs
    ):
        """plot the contour of the underlying 2D-mesh (2D)

        Args:
            color (str, optional): optional matplotlib compatible color. Defaults to "auto".
            set_ax_aspect (bool, optional): If True, will set aspect of plot to equal. Defaults to True.
            alpha (float, optional): matplotlib transparency value. Defaults to 1.0.
            alpha_value (float, optional): alphashape value. If `None`, try to automatically optimize for best enclosing of structure. Defaults to None.
            reset_color_cycle (bool, optional): reset color cycle after finishing the plot. Defaults to True.

        Returns:
            matplotlib line: matplotlib's `scatter` output
        """
        from torchgdm.visu import visu2d

        kwargs["projection"] = "xz"
        im = visu2d.geo2d.contour(
            self,
            color=color,
            set_ax_aspect=set_ax_aspect,
            alpha=alpha,
            alpha_value=alpha_value,
            reset_color_cycle=reset_color_cycle,
            **kwargs
        )
        return im

    def plot3d(self, **kwargs):
        """plot the point polarizability structure (3D)"""
        from torchgdm.visu import visu3d
        
        warnings.warn(
            "Visualizing a 2D model in 3D will show only meshpoints in the 'XZ' plane. The 3D plot shows a circumscribing sphere but is in fact a circumscribing cylinder."
        )

        return visu3d.geo3d._plot_structure_eff_3dpola(self, **kwargs)

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
        if axis.lower() != "y":
            raise ValueError(
                "Only rotation axis 'y' supported in 2D (infinite axis).".format(axis)
            )

        _struct_rotated = super().rotate(alpha=alpha, center=center, axis=axis)

        return _struct_rotated
