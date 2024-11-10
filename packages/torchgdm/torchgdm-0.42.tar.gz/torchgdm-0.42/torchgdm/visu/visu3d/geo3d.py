# encoding=utf-8
"""
3D visualization tools for geometries
"""
# %%
import copy
import warnings
import itertools

import torch

from torchgdm.constants import COLORS_DEFAULT
from torchgdm.tools.misc import to_np
from torchgdm import tools


# global color handling
COLOR_ITERATOR = itertools.cycle(COLORS_DEFAULT)
LEGEND_ENTRIES_LOOKUP = dict()


# reset color iterator and materials lookup
def _reset_color_iterator():
    global COLOR_ITERATOR, LEGEND_ENTRIES_LOOKUP
    COLOR_ITERATOR = itertools.cycle(COLORS_DEFAULT)
    LEGEND_ENTRIES_LOOKUP = dict()


def _return_next_color():
    return next(COLOR_ITERATOR)


_reset_color_iterator()


def _generate_legend(pl):
    global LEGEND_ENTRIES_LOOKUP

    if len(LEGEND_ENTRIES_LOOKUP) != 0:
        labels = LEGEND_ENTRIES_LOOKUP.keys()
    else:
        labels = []

    pv_labels = []
    for i_s, label in enumerate(labels):
        legend_dict = LEGEND_ENTRIES_LOOKUP[label]
        pv_labels.append([label, legend_dict["fc"]])

    pl.add_legend(labels=pv_labels, bcolor="w", face=None)

    return pl.legend


def _plot_structure_discretized(
    struct,
    scale=1.0,
    color="auto",
    show_grid=True,
    legend=True,
    alpha=1.0,
    show="auto",
    pl=None,
    reset_color_cycle=True,
    **kwargs,
):
    import numpy as np
    import pyvista as pv

    if "projection" in kwargs:
        kwargs.pop("projection")

    global COLOR_ITERATOR, LEGEND_ENTRIES_LOOKUP

    if reset_color_cycle:
        _reset_color_iterator()

    # get mesh positions and step sizes, cut in multi-materials
    pos = to_np(struct.positions)
    step = to_np(struct.step)

    if type(show) == str:
        if show.lower() == "auto" and pl is None:
            show = True
        else:
            False

    if pl is None:
        pl = pv.Plotter()

    if color == "auto":
        # colors = COLORS_DEFAULT
        diff_mat_names = [s.__name__ for s in struct.materials]
        mat_names = np.array(diff_mat_names)

        different_materials = np.unique(mat_names)

        mat_pos_subset_idx = []
        for pos_single_mat in different_materials:
            mat_pos_subset_idx.append(
                np.arange(len(mat_names))[mat_names == pos_single_mat]
            )
    else:
        different_materials = ["struct. id:{}".format(struct.id)]
        mat_pos_subset_idx = [np.arange(len(pos))]  # all pos
        # colors = [color]

    # the actual plot
    mesh_list = []
    for i_s, pos_idx in enumerate(mat_pos_subset_idx):
        pos_mat = pos[pos_idx]
        steplist_mat = step[pos_idx]

        pts = pv.PolyData(pos_mat)
        pts["steps"] = steplist_mat
        pts.set_active_scalars("steps")

        mesh_list.append(
            pts.glyph(geom=pv.Cube(), scale="steps", factor=scale, orient=False)
        )

    for i_s, mesh in enumerate(mesh_list):
        # chose color
        if color == "auto":
            # if material already used, re-use its color. otherwise use next color
            if different_materials[i_s] in LEGEND_ENTRIES_LOOKUP:
                _col = LEGEND_ENTRIES_LOOKUP[different_materials[i_s]]["color"]
            else:
                _col = next(COLOR_ITERATOR)
        elif type(color) in [list, tuple]:
            _col = color[i_s]
        else:
            _col = color

        # add legend entry:
        LEGEND_ENTRIES_LOOKUP[different_materials[i_s]] = dict(
            color=_col,
            fc=_col,
            ec=_col,
            marker="s",
            markersize=10,
        )

        label = different_materials[i_s]
        pl.add_mesh(
            mesh,
            color=_col,
            show_edges=show_grid,
            edge_color="black",
            line_width=0.5,
            opacity=alpha,
            edge_opacity=alpha,
            label=label,
        )

    if legend:
        _generate_legend(pl)

    if show:
        pl.show()

    return mesh_list


def _plot_structure_eff_3dpola(
    struct,
    scale=1.0,
    center_marker_scale=10,
    color="auto",
    sphere_style="wireframe",
    color_sphere="auto",
    theta_resolution=20,
    phi_resolution=20,
    alpha=0.1,
    show_grid=True,
    color_grid="auto",
    alpha_grid=0.05,
    show="auto",
    pl=None,
    legend=False,
    reset_color_cycle=True,
    **kwargs,
):
    from torchgdm import tools
    import numpy as np
    import pyvista as pv

    if "projection" in kwargs:
        kwargs.pop("projection")

    global COLOR_ITERATOR, LEGEND_ENTRIES_LOOKUP

    if reset_color_cycle:
        _reset_color_iterator()

    if type(show) == str:
        if show.lower() == "auto" and pl is None:
            show = True
        else:
            show = False

    if pl is None:
        pl = pv.Plotter()

    # legend label based on structure ID
    legend_label = "eff.pola. (id: {})".format(struct.id)

    # automatic next color
    if color == "auto":
        if legend_label in LEGEND_ENTRIES_LOOKUP:
            _col = LEGEND_ENTRIES_LOOKUP[legend_label]["color"]
        else:
            _col = next(COLOR_ITERATOR)
    else:
        _col = color

    if color_grid == "auto":
        color_grid = _col
    if color_sphere == "auto":
        color_sphere = _col

    # add / update legend entry
    LEGEND_ENTRIES_LOOKUP[legend_label] = dict(
        color=_col,
        fc=color_sphere,
        ec=_col,
        marker="o",
        markersize=10,
    )

    # geometry data to numpy
    pos_a = to_np(struct.positions)
    enclosing_radius = to_np(struct.step) / 2.0

    # create the actual plot: iterate over polarizabilities
    mesh_sphere_list = []
    mesh_center_list = []
    mesh_fullgeo_list = []
    for i, pos in enumerate(pos_a):
        r = enclosing_radius[i]
        _geo = struct.full_geometries[i]
        pos_mesh = to_np(_geo)
        step_mesh = to_np(tools.geometry.get_step_from_geometry(_geo))

        # plot enclosing sphere
        enclose_sphere = pv.Sphere(
            r + step_mesh / 2.0,
            pos,
            theta_resolution=theta_resolution,
            phi_resolution=phi_resolution,
        )
        mesh_sphere_list.append(enclose_sphere)

        # center pos. "marker" sphere
        mesh_center_list.append(pv.Sphere(center_marker_scale, pos))

        # full geometry mesh
        pts = pv.PolyData(pos_mesh)
        pts["steps"] = np.ones(len(pos_mesh)) * step_mesh
        pts.set_active_scalars("steps")

        mesh_fullgeo_list.append(
            pts.glyph(geom=pv.Cube(), scale="steps", factor=scale, orient=False)
        )

    # plot enclosing sphere wireframe
    for i_s, mesh in enumerate(mesh_sphere_list):
        pl.add_mesh(
            mesh,
            color=color_sphere,
            show_edges=False,
            line_width=0.5,
            edge_opacity=alpha,
            opacity=alpha,
            style=sphere_style,
        )

    # plot dipole position
    for i_s, mesh in enumerate(mesh_center_list):
        pl.add_mesh(mesh, color=_col)

    # optionally plot the replaced full geometry mesh
    if show_grid:
        for i_s, mesh in enumerate(mesh_fullgeo_list):
            pl.add_mesh(
                mesh,
                color=color_grid,
                show_edges=True,
                edge_color="black",
                line_width=0.5,
                opacity=alpha_grid,
                edge_opacity=alpha_grid * 0.1,
            )

    # optional legend additions
    if legend:
        _generate_legend(pl)

    if show:
        pl.show()

    return mesh_sphere_list, mesh_center_list, mesh_fullgeo_list


def structure(
    struct,
    color="auto",
    scale=1,
    legend=True,
    reset_color_cycle=True,
    pl=None,
    show="auto",
    **kwargs,
):
    """plot structure in 3D

    plot the structure `struct` in 3D using `pyvista`.
    Either from a structure instance, or using a simulation as input.

    kwargs are passed to individual structure plotting and / or to pyvista

    Parameters
    ----------
    struct : simulation or structure
          either a simulation or a structure instance

    projection : str, default: 'auto'
        which 2D projection to plot: "auto", "XY", "YZ", "XZ"

    color : str or matplotlib color, default: "auto"
            Color of scatterplot. Either "auto", or matplotlib-compatible color.
            "auto": automatic color selection (multi-color for multiple materials).

    legend : bool, default: True
        whether to add a legend if multi-material structure (requires auto-color enabled)


    Returns
    -------
        lists of shown meshes that are returned by the 3D plotting functions

    """
    import pyvista as pv
    from torchgdm.simulation import SimulationBase, Simulation
    from torchgdm.struct.volume.pola import StructDiscretized3D
    from torchgdm.struct.volume.pola import StructDiscretizedCubic3D
    from torchgdm.struct.volume.pola import StructDiscretizedHexagonal3D
    from torchgdm.struct.point.pola import StructEffPola3D

    if reset_color_cycle:
        _reset_color_iterator()

    # got a structure instance:
    if (
        issubclass(type(struct), StructDiscretized3D)
        or issubclass(type(struct), StructDiscretizedCubic3D)
        or issubclass(type(struct), StructDiscretizedHexagonal3D)
    ):
        pl_res = _plot_structure_discretized(
            struct,
            color=color,
            scale=scale,
            show=show,
            pl=pl,
            **kwargs,
        )
    elif issubclass(type(struct), StructEffPola3D):
        pl_res = _plot_structure_eff_3dpola(
            struct,
            color=color,
            scale=scale,
            show=show,
            pl=pl,
            **kwargs,
        )
    elif issubclass(type(struct), Simulation) or issubclass(
        type(struct), SimulationBase
    ):
        # -- prep
        sim = struct

        if type(show) == str:
            if show.lower() == "auto" and pl is None:
                show = True
            else:
                show = False

        if pl is None:
            pl = pv.Plotter()

        # -- call all structure's plot functions
        pl_res = []  # collect results
        for i_s, _st in enumerate(sim.structures):
            pl_res.append(
                _st.plot3d(
                    color=color,
                    scale=scale,
                    pl=pl,
                    legend=False,
                    reset_color_cycle=False,
                    show=False,
                    **kwargs,
                )
            )

        # -- finalize: config global plot
        if legend:
            _generate_legend(pl)
        if show:
            pl.show()
    else:
        raise ValueError("Unknown structure input")

    if reset_color_cycle:
        _reset_color_iterator()

    return pl_res
