# -*- coding: utf-8 -*-
"""
core simulation class
"""
# %%
import warnings
import time

import torch

from torchgdm.field import Field
from torchgdm.constants import DTYPE_FLOAT, DTYPE_COMPLEX
from torchgdm.tools.misc import tqdm, purge_mem, get_default_device
from torchgdm.tools.batch import get_e0, get_h0
from torchgdm.tools.geometry import test_structure_distances


# --- simulation base class
class SimulationBase:
    """torchgdm simulation container

    This class contains all elements describing a simulation:
     - the environment
     - the structure(s)
     - the illumination field(s)
     - the evaluation wavelength(s)

    It also acts as an interface to running and postprocessing
    of the simulation as well as for several visualization tools.
     - run the simulation
     - evaluate observables
     - evaluate spectra
     - evaluate a rasterscan

    It also contains methods for manipulations of the simulation and structures
     - add / remove a structure
     - split off a new simulation with a sub-structure
     - combine with structures and their fields from another simulation
     - copy (including optional shift of all structures)

    Furthermore it several contains private methods necessary for simulation setup and running
    """

    __name__ = "simulation base class"

    def __init__(
        self,
        structures: list,
        environment,
        illumination_fields: list,
        wavelengths: torch.Tensor,
        test_structure_collisions: bool = True,
        on_distance_violation: str = "error",
        device: torch.device = None,
    ):
        """base simulation constructor

        Args:
            structures (_type_): list of structures
            environment (_type_): environment class
            illumination_fields (_type_): list of illuminations
            wavelengths (torch.Tensor): evaluation wavelengths (in nm)
            test_structure_collisions (bool, optional): Check for overlapping / colliding structures. Can be slow in case of many structures. Defaults to True.
            on_distance_violation (str, optional): behavior on distance violation. can be "error", "warn" or None (do nothing). Defaults to "error".
            device (torch.device, optional): Defaults to "cpu" (can be changed by :func:`torchgdm.use_cuda`).
        """
        if device is None:
            self.device = get_default_device()
        else:
            self.device = device

        # structures, wavelengths, illuminations: if single element given, wrap into list
        if hasattr(structures, "__iter__"):
            self.structures = [
                _s for _s in structures if _s is not None
            ]  # ignore "None" entries
        else:
            self.structures = [structures]

        if hasattr(illumination_fields, "__iter__"):
            self.illumination_fields = illumination_fields
        else:
            self.illumination_fields = [illumination_fields]

        # convert single wavelength to list
        self.wavelengths = torch.as_tensor(
            wavelengths, dtype=DTYPE_FLOAT, device=self.device
        )
        self.wavelengths = torch.atleast_1d(self.wavelengths)

        self.environment = environment

        # test collisions:
        for _s1 in self.structures:
            for _s2 in self.structures:
                if _s1 != _s2:
                    N_dist1, N_dist2 = test_structure_distances(
                        _s1, _s2, on_distance_violation=on_distance_violation
                    )

        self.reset_fields()

        # test if all components are same dimension as environment
        self._test_dimensions_matching()

    def _test_dimensions_matching(self):
        self.n_dim = dim = self.environment.n_dim
        if dim == -1:
            raise ValueError(
                "The environemnt has undefined dimension (-1), please modify your environment class."
            )

        # test structures
        for _s in self.structures:
            if _s.n_dim == -1:
                raise ValueError(
                    "A structure has undefined dimension (-1), please modify your structure class. "
                    + f"The current environment is {dim}D."
                )
            if _s.n_dim != dim:
                raise ValueError(
                    "Structures with inconsistent dimensions found. "
                    + f"Environment is {dim}D, all structures must be {dim}D as well."
                )

        # test illumination fields
        for _f in self.illumination_fields:
            if _f.n_dim == -1:
                raise ValueError(
                    "An illumination field has undefined dimension (-1), please modify your field class. "
                    + f"The current environment is {dim}D."
                )
            if _f.n_dim != dim:
                raise ValueError(
                    "Illumination fields with inconsistent dimensions found. "
                    + f"Environment is {dim}D, all fields must be {dim}D as well."
                )

    def set_device(self, device):
        """move all tensors of the class to device"""
        self.device = device

        # iterate lists of torchgdm objects
        for i in range(len(self.structures)):
            self.structures[i].set_device(device=device)
        for i in range(len(self.illumination_fields)):
            self.illumination_fields[i].set_device(device=device)

        # stored fields
        for k in self.fields_inside:
            self.fields_inside[k].set_device(device=device)

        # further objects
        self.environment.set_device(device=device)
        self.wavelengths = self.wavelengths.to(device=device)

    # --- simulation manipulation
    def add_struct(self, struct, on_distance_violation="error"):
        """add a structure to the simulation

        reset possibly pre-calculated fields.
        **Caution:** Not compatible with autograd!

        Args:
            struct (StructBase): structure to add

        Returns:
            simulation including added structure
        """
        import copy

        _new_sim = copy.deepcopy(self)

        _new_sim.structures.append(struct)

        N_dist1, N_dist2 = test_structure_distances(
            self, struct, on_distance_violation=on_distance_violation
        )

        warnings.warn(
            "Resetting pre-calculated fields. This should be changed, e.g. add zero fields."
        )
        _new_sim.reset_fields()
        return _new_sim

    def delete_struct(self, index: int):
        """delete a structure from the simulation

        **Caution:** Not compatible with autograd!

        Args:
            index (int): index of structure to delete from sim

        Returns:
            simulation without deleted structure
        """
        _simlist = [self.split(i) for i in range(len(self.structures))]
        if index == 0:
            _s = _simlist.pop(0)

        _new_sim = _simlist.pop(0)
        for i, _s in enumerate(_simlist):
            if index != 0 and i == index:
                pass  # delete (don't add) this structure
            else:
                _new_sim.combine(_s)

        return _new_sim

    def split(self, structure_index: int):
        """split a structure into new simulation

        return a new simulation with identical config,
        containing only the splitted structure.
        If fields were calculated, they are kept for the splitted structure

        **Caution:** Not compatible with autograd!

        Args:
            index (int): index of structure to split from sim

        Returns:
            simulation containing splitted structure
        """
        import copy

        _new_sim = copy.deepcopy(self)

        # if calculated, extract fields inside splitted structure
        if len(_new_sim.fields_inside) > 0:
            _new_sim.fields_inside = _new_sim._get_insidefields_for_single_structure(
                structure_index=structure_index
            )

        # retain selected structure
        _new_sim.structures = [_new_sim.structures[structure_index]]

        return _new_sim

    def combine(self, other_sim, on_distance_violation="error"):
        """combine with other simulation

        Combining pre-calculated fields. Wavelengths and field configs must match!

        **Caution:** Not compatible with autograd!

        Args:
            other_sim (:class:`Simulation`): simulation to combine with

        Returns:
            :class:`Simulation`: combined simulation
        """
        import copy

        _new_sim = copy.deepcopy(self)

        assert len(_new_sim.fields_inside) == len(other_sim.fields_inside)
        assert _new_sim.wavelengths == other_sim.wavelengths
        assert len(_new_sim.illumination_fields) == len(other_sim.illumination_fields)
        assert _new_sim.environment.__name__ == other_sim.environment.__name__
        assert _new_sim.device == other_sim.device

        N_dist1, N_dist2 = test_structure_distances(
            self, other_sim, on_distance_violation=on_distance_violation
        )

        # if existing: combine inside fields
        if len(_new_sim.fields_inside) > 0:
            fields_inside_combined = dict()
            for wl in self.wavelengths:
                wl = float(wl)

                e_in_1 = _new_sim.fields_inside[wl].efield
                h_in_1 = _new_sim.fields_inside[wl].hfield
                e_in_2 = other_sim.fields_inside[wl].efield
                h_in_2 = other_sim.fields_inside[wl].hfield
                e_in = torch.cat([e_in_1, e_in_2], dim=1)
                h_in = torch.cat([h_in_1, h_in_2], dim=1)

                pos1 = _new_sim.get_all_positions()
                pos2 = other_sim.get_all_positions()
                pos = torch.cat([pos1, pos2], dim=0)

                _f = Field(pos, e_in, h_in)
                fields_inside_combined[float(wl)] = _f

            _new_sim.fields_inside = fields_inside_combined

        # combine structures
        _new_sim.structures += other_sim.structures  # add 2 lists

        return _new_sim

    def copy(self, positions=None):
        """(batch) copy simulation

        optionally, a simulations with multiple copies of its structures can be created, where each copy of structures is shifted to a new position.

        Args:
            positions (list, optional): list of new positions to create copies of the structures at. If None, create a single, identical copy. Defaults to None.

        Returns:
            :class:`Simulation`: new simulation
        """
        if positions is None:
            import copy

            return copy.deepcopy(self)
        else:
            # generate multiple copies, moved to `positions`
            positions = torch.as_tensor(
                positions, device=self.device, dtype=DTYPE_FLOAT
            )

            # single position: expand dim
            if len(positions.shape) == 1:
                positions = positions.unsqueeze(0)

            assert len(positions.shape) == 2
            assert positions.shape[1] == 3

            new_sim_list = []
            for _r in positions:
                _sim = self.copy()
                for i in range(len(_sim.structures)):
                    _sim.structures[i] = _sim.structures[i] + _r
                new_sim_list.append(_sim)

            new_sim = new_sim_list.pop(0)
            for _s in new_sim_list:
                new_sim = new_sim.combine(_s)

            return new_sim

    def __add__(self, other):
        if issubclass(type(other), type(self)):
            # add another simulation: try combining both.
            return self.combine(other)
        else:
            raise ValueError(
                "Unknown add type, only addition of other sim is supported."
            )

    # --- convenience plotting wrapper
    def plot_structure(self, **kwargs):
        from torchgdm.visu import visu2d

        visu2d.structure(self, **kwargs)

    def plot_contour(self, **kwargs):
        from torchgdm.visu import visu2d

        visu2d.contour(self, **kwargs)

    def plot_structure_3d(self, **kwargs):
        from torchgdm.visu import visu3d

        visu3d.structure(self, **kwargs)

    def plot_efield_vectors_inside(self, wavelength, illumination_index=0, **kwargs):
        from torchgdm.visu import visu2d

        visu2d.vectorfield_inside(
            self,
            wavelength=wavelength,
            illumination_index=illumination_index,
            whichfield="e",
            **kwargs,
        )

    def plot_hfield_vectors_inside(self, wavelength, illumination_index=0, **kwargs):
        from torchgdm.visu import visu2d

        visu2d.vectorfield_inside(
            self,
            wavelength=wavelength,
            illumination_index=illumination_index,
            whichfield="h",
            **kwargs,
        )

    def plot_efield_vectors_inside_3d(
        self, wavelength, illumination_index=0, scale=1, **kwargs
    ):
        from torchgdm.visu import visu3d

        visu3d.vectorfield_inside(
            self,
            wavelength=wavelength,
            illumination_index=illumination_index,
            whichfield="e",
            scale=25 * scale,
            **kwargs,
        )

    def plot_hfield_vectors_inside_3d(
        self, wavelength, illumination_index=0, scale=1, **kwargs
    ):
        from torchgdm.visu import visu3d

        visu3d.vectorfield_inside(
            self,
            wavelength=wavelength,
            illumination_index=illumination_index,
            whichfield="h",
            scale=25 * scale,
            **kwargs,
        )

    # --- functions combining properties from all structures
    def get_all_positions(self) -> torch.Tensor:
        """return a list of all positions with dipoles"""
        return torch.cat([struct.positions for struct in self.structures], dim=0)

    def get_source_validity_radius(self) -> torch.Tensor:
        """return a list of all effective step-radii / enclosing sphere radius"""
        all_pos_step = [_s.get_source_validity_radius() for _s in self.structures]
        return torch.cat(all_pos_step)

    def get_closest_wavelength(self, wavelength):
        """return closest wavelength match available in the simulation"""
        from torchgdm.tools.misc import get_closest_wavelength

        return get_closest_wavelength(self, wavelength)

    # --- internal API: helper for polarizable / non-polarizable dipole handling
    def _get_polarizable_positions_indices_separate_p_m(
        self, structure_index=-1
    ) -> tuple:
        """get lists with indices of polarizable positions, separate for p and m

        Args:
            structure_index (int, optional): Optionally select a specific sub-structure. if -1, return for all structures. Defaults to -1.

        Returns:
            tuple: (torch.Tensor, torch.Tensor). position indices at which polarizable p and m dipoles are located
        """
        # optional: consider only a specific structure
        if structure_index == -1:
            structures = self.structures
        else:
            structures = [self.structures[structure_index]]

        idx_p = [torch.tensor([], dtype=torch.int32, device=self.device)]
        idx_m = [torch.tensor([], dtype=torch.int32, device=self.device)]
        i_offset = 0
        for struct in structures:
            N_pos = len(struct.positions)

            _sT = struct.evaluation_terms
            if "E" in _sT:
                idx_p.append(
                    torch.arange(i_offset, i_offset + N_pos, device=self.device)
                )
            if "H" in _sT:
                idx_m.append(
                    torch.arange(i_offset, i_offset + N_pos, device=self.device)
                )

            i_offset += N_pos

        return torch.cat(idx_p, dim=0), torch.cat(idx_m, dim=0)

    def _get_nonpolarizable_positions_indices_separate_p_m(
        self, structure_index=-1
    ) -> tuple:
        """get lists with indices of non-polarizable positions (where *no* polarizabilites are located), separate for p and m

        Args:
            structure_index (int, optional): Optionally select a specific sub-structure. if -1, return for all structures. Defaults to -1.

        Returns:
            tuple: (torch.Tensor, torch.Tensor). non-polarizable position indices at which *no* p or *no* m dipoles are located
        """
        # optional: consider only a specific structure
        if structure_index == -1:
            structures = self.structures
        else:
            structures = [self.structures[structure_index]]

        idx_p = [torch.tensor([], dtype=torch.int32, device=self.device)]
        idx_m = [torch.tensor([], dtype=torch.int32, device=self.device)]
        i_offset = 0
        for struct in structures:
            N_pos = len(struct.positions)

            _sT = struct.evaluation_terms
            if "E" not in _sT:
                idx_p.append(
                    torch.arange(i_offset, i_offset + N_pos, device=self.device)
                )
            if "H" not in _sT:
                idx_m.append(
                    torch.arange(i_offset, i_offset + N_pos, device=self.device)
                )

            i_offset += N_pos

        return torch.cat(idx_p, dim=0), torch.cat(idx_m, dim=0)

    def _get_polarizable_positions_separate_p_m(self) -> tuple:
        """get lists with polarizable positions, separate for p and m

        Args:
            structure_index (int, optional): Optionally select a specific sub-structure. if -1, return for all structures. Defaults to -1.

        Returns:
            tuple: (torch.Tensor, torch.Tensor). positions at which polarizable p and m dipoles are located
        """
        idx_p, idx_m = self._get_polarizable_positions_indices_separate_p_m()
        dp_pos = self.get_all_positions()
        pos_p = torch.index_select(dp_pos, 0, idx_p)
        pos_m = torch.index_select(dp_pos, 0, idx_m)

        return pos_p, pos_m

    def _get_nonpolarizable_positions_separate_p_m(self) -> tuple:
        """get lists with non-polarizable positions (where *no* polarizabilites are located), separate for p and m

        Args:
            structure_index (int, optional): Optionally select a specific sub-structure. if -1, return for all structures. Defaults to -1.

        Returns:
            tuple: (torch.Tensor, torch.Tensor). non-polarizable positions at which *no* p or *no* m dipoles are located
        """
        idx_p, idx_m = self._get_nonpolarizable_positions_indices_separate_p_m()
        dp_pos = self.get_all_positions()
        pos_miss_p = torch.index_select(dp_pos, 0, idx_p)
        pos_miss_m = torch.index_select(dp_pos, 0, idx_m)

        return pos_miss_p, pos_miss_m

    def _get_polarizable_mask_full_fields(self) -> torch.Tensor:
        # loop through structures and create field-mask for polarizable positions
        mask_fields = []
        for struct in self.structures:
            Npos = len(struct.positions)

            _sT = struct.evaluation_terms
            _mask_e0h0 = torch.zeros(
                (len(self.illumination_fields), Npos, 6),
                dtype=torch.bool,
                device=self.device,
            )
            if "E" in _sT:
                _mask_e0h0[..., :3] = 1
            if "H" in _sT:
                _mask_e0h0[..., 3:] = 1
            mask_fields.append(_mask_e0h0)
        mask_fields = torch.cat(mask_fields, dim=1)

        return mask_fields

    # --- polarizabilities of all structure dipoles
    def _get_all_polarizabilitites_6x6(self, wavelength: float) -> torch.Tensor:
        pola_list = torch.cat(
            [
                struct.get_polarizability_6x6(wavelength, self.environment)
                for struct in self.structures
            ],
            dim=0,
        )
        return pola_list

    def _get_all_polarizabilitites_pEH_3x6(self, wavelength: float) -> torch.Tensor:
        pola_list = torch.cat(
            [
                struct.get_polarizability_pEH_3x6(wavelength, self.environment)
                for struct in self.structures
            ],
            dim=0,
        )
        return pola_list

    def _get_all_polarizabilitites_mEH_3x6(self, wavelength: float) -> torch.Tensor:
        pola_list = torch.cat(
            [
                struct.get_polarizability_mEH_3x6(wavelength, self.environment)
                for struct in self.structures
            ],
            dim=0,
        )
        return pola_list

    def _get_all_selfterms_6x6(self, wavelength: float) -> torch.Tensor:
        st_list = []
        for struct in self.structures:
            st_list.append(struct.get_selfterm_6x6(wavelength, self.environment))
        return torch.cat(st_list, dim=0)

    # --- illumination fields at all dipoles
    def _get_all_e0(self, wavelength: float) -> torch.Tensor:
        dp_pos = self.get_all_positions()
        e0 = get_e0(sim=self, wavelength=wavelength, r_probe=dp_pos)
        return e0

    def _get_all_h0(self, wavelength: float) -> torch.Tensor:
        dp_pos = self.get_all_positions()
        h0 = get_h0(sim=self, wavelength=wavelength, r_probe=dp_pos)
        return h0

    def _get_all_e0_h0(self, wavelength: float) -> torch.Tensor:
        e0 = self._get_all_e0(wavelength)
        h0 = self._get_all_h0(wavelength)
        e0h0 = torch.cat([e0, h0], dim=-1)
        return e0h0

    # --- fields per structure
    def _get_insidefields_for_single_structure(self, structure_index):
        # get indices of positions corresponding to selected structure
        n_pos = [len(_s.positions) for _s in self.structures]
        n_pos_cum = torch.cumsum(torch.as_tensor([0] + n_pos), 0)
        idx = [
            torch.arange(_nstart, _nstart + _n) for _nstart, _n in zip(n_pos_cum, n_pos)
        ][structure_index]
        idx = idx.to(device=self.device)

        # extract inside fields of selected structure
        fields_inside_struct = dict()
        for wl in self.wavelengths:
            wl = float(wl)

            e_in_mask = torch.index_select(self.fields_inside[wl].efield, 1, idx)
            h_in_mask = torch.index_select(self.fields_inside[wl].hfield, 1, idx)

            _f = Field(self.structures[structure_index].positions, e_in_mask, h_in_mask)
            fields_inside_struct[float(wl)] = _f

        return fields_inside_struct

    # --- fields and dipole moments at polarizable sources only
    def _get_polarizablefields_e0_h0(self, wavelength: float) -> torch.Tensor:
        # get full illumination E0, H0 fields (defined in parent class)
        e0_h0_all = self._get_all_e0_h0(wavelength=wavelength)

        mask_fields = self._get_polarizable_mask_full_fields()
        return e0_h0_all[mask_fields].reshape(len(self.illumination_fields), -1)

    def _get_polarizablefields_e(self, wavelength):
        wl_key = float(wavelength)
        idx_p, idx_m = self._get_polarizable_positions_indices_separate_p_m()
        e_in_mask = torch.index_select(self.fields_inside[wl_key].efield, 1, idx_p)
        return e_in_mask

    def _get_polarizablefields_h(self, wavelength):
        wl_key = float(wavelength)
        idx_p, idx_m = self._get_polarizable_positions_indices_separate_p_m()
        h_in_mask = torch.index_select(self.fields_inside[wl_key].hfield, 1, idx_m)
        return h_in_mask

    def _get_polarizable_dipole_moments_p(self, wavelength):
        wl_key = float(wavelength)
        idx_p, idx_m = self._get_polarizable_positions_indices_separate_p_m()

        e_in_mask = self._get_polarizablefields_e(wavelength)
        e_in_mask = torch.index_select(self.fields_inside[wl_key].efield, 1, idx_p)
        h_in_mask = torch.index_select(self.fields_inside[wl_key].hfield, 1, idx_p)
        e_h_in_mask = torch.cat([e_in_mask, h_in_mask], dim=-1)

        # calc. electric dipole moments due to E and H
        alpha_pEH = self._get_all_polarizabilitites_pEH_3x6(wavelength)
        alpha_pEH_mask = torch.index_select(alpha_pEH, 0, idx_p)
        p_in_mask = torch.matmul(alpha_pEH_mask, e_h_in_mask.unsqueeze(-1))

        return p_in_mask[..., 0]  # remove last dim from broadcast in matmul

    def _get_polarizable_dipole_moments_m(self, wavelength):
        wl_key = float(wavelength)
        idx_p, idx_m = self._get_polarizable_positions_indices_separate_p_m()

        e_in_mask = torch.index_select(self.fields_inside[wl_key].efield, 1, idx_m)
        h_in_mask = torch.index_select(self.fields_inside[wl_key].hfield, 1, idx_m)
        e_h_in_mask = torch.cat([e_in_mask, h_in_mask], dim=-1)

        # calc. magnetic dipole moments due to E and H
        alpha_mEH = self._get_all_polarizabilitites_mEH_3x6(wavelength)
        alpha_mEH_mask = torch.index_select(alpha_mEH, 0, idx_m)
        m_in_mask = torch.matmul(alpha_mEH_mask, e_h_in_mask.unsqueeze(-1))

        return m_in_mask[..., 0]  # remove last dim from broadcast in matmul


# --- simulation container class
class Simulation(SimulationBase):
    """torchgdm simulation container"""

    __name__ = "torchgdm simulation container"

    def __init__(
        self,
        structures: list,
        environment,
        illumination_fields: list,
        wavelengths: list,
        linearsystem="default",
        test_structure_collisions: bool = True,
        on_distance_violation: str = "error",
        device: torch.device = None,
    ):
        """simulation constructor

        Args:
            structures (list): list of structures
            environment (environmentBase): environment class
            illumination_fields (list): list of illuminations
            wavelengths (list): list of wavelengths to evaluate (nm)
            linearsystem (linearSystemBase): solver for the coupling system. Defaults to `LinearSystemFullMoreMemoryEfficient`
            test_structure_collisions (bool, optional): Check for overlapping / colliding structures. Can be slow in case of many structures. Defaults to True.
            on_distance_violation (str, optional): behavior on distance violation. can be "error", "warn" or None (do nothing). Defaults to "error".
            device (torch.device, optional): Defaults to 'cpu'.
        """
        super().__init__(
            structures=structures,
            environment=environment,
            illumination_fields=illumination_fields,
            wavelengths=wavelengths,
            device=device,
            test_structure_collisions=test_structure_collisions,
            on_distance_violation=on_distance_violation,
        )
        if type(linearsystem) == str:
            if linearsystem.lower() == "default":
                from torchgdm.linearsystem import LinearSystemFullMoreMemoryEfficient

                self.linearsystem = LinearSystemFullMoreMemoryEfficient(device=device)
            else:
                raise ValueError("Unknown linearsystem.")
        else:
            self.linearsystem = linearsystem

        # set the global device for the simulation
        self.set_device(self.device)

    def __repr__(self):
        out_str = ""
        out_str += "simulation on device '{}'...\n".format(self.device)

        out_str += " - {}\n".format(self.environment.__name__)

        out_str += " - {} structures\n".format(len(self.structures))

        _pos = self.get_all_positions()
        out_str += " - {} positions\n".format(len(_pos))

        _pos_p, _pos_m = self._get_polarizable_positions_separate_p_m()
        out_str += " - {} coupled dipoles\n".format(len(_pos_p) + len(_pos_m))
        out_str += "   (of which {} p, {} m)\n".format(len(_pos_p), len(_pos_m))

        out_str += " - {} wavelengths\n".format(len(self.wavelengths))

        out_str += " - {} illumination fields per wavelength".format(
            len(self.illumination_fields)
        )
        return out_str

    def set_device(self, device):
        super().set_device(device)
        self.linearsystem.set_device(device)

    def reset_fields(self):
        self.fields_inside = dict()

    def run(
        self,
        batch_size: int = 32,
        calc_missing: bool = False,
        verbose: int = 1,
        progress_bar=True,
    ):
        """run the simulation: evaluate all illuminations at all wavelengths

        results are the selfconsistent, full electric and magnetic fields
        at each meshpoint of all structures.

        this will populate `self.fields_inside` a dict with the wavelengths (in nm) as keys.
        Each element is a :class:`torchgdm.Field` instance, containing the `efield` and `hfield`.

        Args:
            batch_size (int, optional):    Nr of incident fields evaluated in parallel. Defaults to 32.
            calc_missing (bool, optional): calculate non-relevant internal fields, typically
                                           H-Field in discretized structures). Defaults to False.
            verbose (int, optional):       print status info. Defaults to 1.
        """
        t_start = time.time()
        if verbose:
            print("-" * 60)
            print(self)
            print("\nrun spectral simulation:")

        # loop over wavelengths
        for wl in tqdm(self.wavelengths, progress_bar, title=""):
            t_start_wl = time.time()
            if verbose and not progress_bar:
                print("wl={:.1f}nm: ".format(wl), end="")
            e_in, h_in = self.linearsystem.solve(
                sim=self,
                wavelength=wl,
                batch_size=batch_size,
                verbose=verbose,
            )

            _f = Field(self.get_all_positions(), e_in, h_in)
            self.fields_inside[float(wl)] = _f

            # pure electric / pure magnetic reponse: calc. missing fields via propagation
            if calc_missing:
                t_fillmiss0 = time.time()
                if verbose and not progress_bar:
                    print(" propa", end="")
                self._calculate_fields_at_nonpolarizable(wavelength=wl)
                t_fillmiss1 = time.time()
                if verbose and not progress_bar:
                    print(" {:.2f}s.".format(t_fillmiss1 - t_fillmiss0), end="")

            # cleanup
            purge_mem(dev=e_in.device)

            if verbose and not progress_bar:
                t_end = time.time()
                print(" tot {:.2f}s.".format(t_end - t_start_wl))

        if verbose:
            t_end = time.time()
            if not progress_bar:
                print()
            print("spectrum done in {:.2f}s".format(t_end - t_start))
            print("-" * 60 + "\n")

    # --- fields propagation
    def _calculate_fields_at_nonpolarizable(self, wavelength: float):
        """calculate internal fields for non-polarizable locations

        calculates the magnetic field at locations of purely electric-electric polarizabilties and
        the electric field at locations of purely magnetic-magnetic polarizabilties

        Args:
            wavelength (float): in nm
        """
        # - calculate missing fields at a wavelength via re-propagation
        from torchgdm.postproc.fields import _nearfield_e, _nearfield_h

        wl_key = float(wavelength)
        field_shape = self.fields_inside[wl_key].efield.shape

        mask = self._get_polarizable_mask_full_fields()
        mask_e, mask_h = torch.chunk(mask, 2, dim=2)

        (
            pos_e_miss,
            pos_h_miss,
        ) = self._get_nonpolarizable_positions_separate_p_m()

        if len(pos_e_miss) > 0:
            nf_e = _nearfield_e(
                sim=self,
                wavelength=wavelength,
                r_probe=pos_e_miss,
                source_distance_steps=0.1,  # exclude 'self-source' (divergence of G)
            )
            _e = nf_e["e_tot"]
            e_in = self.fields_inside[wl_key].efield.flatten()
            e_in[~mask_e.flatten()] = _e.flatten()
            e_in = e_in.reshape(field_shape)
            self.fields_inside[wl_key].set_efield(e_in)

        if len(pos_h_miss) > 0:
            nf_h = _nearfield_h(
                sim=self,
                wavelength=wavelength,
                r_probe=pos_h_miss,
                source_distance_steps=0.1,  # exclude 'self-source' (divergence of G)
            )
            _h = nf_h["h_tot"]
            h_in = self.fields_inside[wl_key].hfield.flatten()
            h_in[~mask_h.flatten()] = _h.flatten()
            h_in = h_in.reshape(field_shape)
            self.fields_inside[wl_key].set_hfield(h_in)

    # --- wrapper for post processing functions
    def get_geometric_crosssection(self, projection="xy"):
        """get ensemble geometric cross section of all structures in nm^2

        Args:
            projection (str, optional): cartesian projection of cross section. Defaults to "xy"

        Returns:
            float: geometric cross section in nm^2
        """
        import torchgdm as tg

        pos = self.get_all_positions()
        steps = torch.cat(
            [s.step / s.mesh_normalization_factor for s in self.structures]
        )
        return tg.tools.geometry._get_geo_cs_positions_steps(pos, steps, projection)

    # - fields
    def get_nearfield(
        self, wavelength, r_probe=None, illumination_index=None, **kwargs
    ):
        """calculate the nearfield (electric and magnetic) at positions `r_probe`

        kwargs (such as `batch_size`) are passed to :func:`torchgdm.postproc.fields.nf`.

        Args:
            sim (:class:`torchgdm.Simulation`): simulation instance
            wavelength (float): evaluation wavelength (in nm)
            r_probe (dict, optional): probe locations describing dict (gen. from `tools.geometry`).  Defaults to None, in which case all positions of the simulation structures are used
            illumination_index (int, optional): optional index of a specific illumination. If None, batch-evaluate all illuminations. Defaults to None.

        Returns:
            dict: results for total, scattered and incident fields (keys: "tot", "sca", "inc") in instances of :class:`torchgdm.Field`
        """
        import torchgdm as tg

        if r_probe is None:
            r_probe = self.get_all_positions()

        nf = tg.postproc.fields.nf(
            self,
            wavelength=wavelength,
            r_probe=r_probe,
            illumination_index=illumination_index,
            **kwargs,
        )

        return nf

    def get_nf(self, **kwargs):
        """alias for :meth:`Simulation.get_nearfield`"""
        return self.get_nearfield(**kwargs)

    def get_field_gradients(
        self,
        wavelength: float,
        r_probe: torch.Tensor = None,
        illumination_index: int = None,  # None: batch all illumination fields
        source_distance_steps: float = None,
        delta=0.1,
        whichfield="e_tot",
        **kwargs,
    ):
        """nearfield gradients inside or in proximity of a nanostructure

        Calculate field-gradients (positions defined by `r_probe`).
        pytorch AD is not efficient for gradients of functions R^n --> R^m, with $n \\sim m >> 1$.
        Therefore, here numerical derivatives are calculated via center differences.

        Based on the original implementation in pyGDM by C. Majorel.

        Warning: The current implementation is not memory efficient, since all fields are calculated, even though not required.

        Args:
            sim (:class:`torchgdm.Simulation`): simulation instance
            wavelength (float): in nm
            r_probe (torch.Tensor, optional): tuple (x,y,z) or list of 3-lists/-tuples to evaluate field gradients. Use all structure positions by default. Defaults to None.
            illumination_index (int, optional): optional index of a specific illumination. If None, batch-evaluate all illuminations. Defaults to None.
            delta (float, optional):  differential step for numerical center-derivative (in nanometers). Defaults to 0.1.
            whichfield (str, optional): fields to calculate the gradient for. One of ["e_sca","e_tot","e_inc", "h_sca","h_tot,"h_inc], . Defaults to "e_tot".

        Raises:
            ValueError: _description_

        Returns:
            3 lists of 3-tuples [dAx, dAy, dAz] (complex): dAj are the differential terms:
                - idx [0] = dE/dx = [dEx/dx, dEy/dx, dEz/dx]
                - idx [1] = dE/dy = [dEx/dy, dEy/dy, dEz/dy]
                - idx [2] = dE/dz = [dEx/dz, dEy/dz, dEz/dz]
        """
        import torchgdm as tg

        if r_probe is None:
            r_probe = self.get_all_positions()
        # field_gradient(sim, wavelength, r_probe, delta=delta, whichfield=field)
        fieldgrad = tg.postproc.fields.field_gradient(
            self,
            wavelength=wavelength,
            r_probe=r_probe,
            illumination_index=illumination_index,
            source_distance_steps=source_distance_steps,
            delta=delta,
            whichfield=whichfield,
            **kwargs,
        )

        return fieldgrad

    def get_nearfield_intensity_efield(
        self, wavelength, r_probe=None, illumination_index=None, **kwargs
    ):
        """calculate the electric field intensity in the nearfield at positions `r_probe`

        kwargs (such as `batch_size`) are passed to :func:`torchgdm.postproc.fields.nf`.

        Args:
            sim (:class:`torchgdm.Simulation`): simulation instance
            wavelength (float): evaluation wavelength (in nm)
            r_probe (dict, optional): probe locations describing dict (gen. from `tools.geometry`).  Defaults to None, in which case all positions of the simulation structures are used
            illumination_index (int, optional): optional index of a specific illumination. If None, batch-evaluate all illuminations. Defaults to None.

        Returns:
            dict: results for total, scattered and incident electric field intensity (keys: "tot", "sca", "inc")
        """
        nf = self.get_nearfield(
            wavelength=wavelength,
            r_probe=r_probe,
            illumination_index=illumination_index,
            **kwargs,
        )

        # add positions
        nf["r_probe"] = nf["tot"].get_positions()

        for which in ["tot", "sca", "inc"]:
            nf[which] = nf[which].get_efield_intensity()

        return nf

    def get_nearfield_intensity_hfield(
        self, wavelength, r_probe=None, illumination_index=None, **kwargs
    ):
        """calculate the magnetic field intensity in the nearfield at positions `r_probe`

        kwargs (such as `batch_size`) are passed to :func:`torchgdm.postproc.fields.nf`.

        Args:
            sim (:class:`torchgdm.Simulation`): simulation instance
            wavelength (float): evaluation wavelength (in nm)
            r_probe (dict, optional): probe locations describing dict (gen. from `tools.geometry`).  Defaults to None, in which case all positions of the simulation structures are used
            illumination_index (int, optional): optional index of a specific illumination. If None, batch-evaluate all illuminations. Defaults to None.

        Returns:
            dict: results for total, scattered and incident magnetic field intensity (keys: "tot", "sca", "inc")
        """
        nf = self.get_nearfield(
            wavelength=wavelength,
            r_probe=r_probe,
            illumination_index=illumination_index,
            **kwargs,
        )

        # add positions
        nf["r_probe"] = nf["tot"].get_positions()

        for which in ["tot", "sca", "inc"]:
            nf[which] = nf[which].get_hfield_intensity()

        return nf

    def get_chirality(
        self, wavelength, r_probe=None, illumination_index=None, **kwargs
    ):
        """calculate the nearfield chirality at positions `r_probe`

        kwargs (such as `batch_size`) are passed to :func:`torchgdm.postproc.fields.nf`.

        Args:
            sim (:class:`torchgdm.Simulation`): simulation instance
            wavelength (float): evaluation wavelength (in nm)
            r_probe (dict, optional): probe locations describing dict (gen. from `tools.geometry`).  Defaults to None, in which case all positions of the simulation structures are used
            illumination_index (int, optional): optional index of a specific illumination. If None, batch-evaluate all illuminations. Defaults to None.

        Returns:
            dict: results for total, scattered and incident magnetic field intensity (keys: "tot", "sca", "inc")
        """
        nf_C = self.get_nearfield(
            wavelength=wavelength,
            r_probe=r_probe,
            illumination_index=illumination_index,
            **kwargs,
        )

        # add positions
        nf_C["r_probe"] = nf_C["tot"].get_positions()

        # overwrite Field instances by the chirality
        for which in ["tot", "sca", "inc"]:
            nf_C[which] = nf_C[which].get_chirality()

        return nf_C

    def get_poynting(self, wavelength, r_probe=None, illumination_index=None, **kwargs):
        """calculate the Poynting vector at positions `r_probe`

        kwargs (such as `batch_size`) are passed to :func:`torchgdm.postproc.fields.nf`.

        Args:
            sim (:class:`torchgdm.Simulation`): simulation instance
            wavelength (float): evaluation wavelength (in nm)
            r_probe (dict, optional): probe locations describing dict (gen. from `tools.geometry`).  Defaults to None, in which case all positions of the simulation structures are used
            illumination_index (int, optional): optional index of a specific illumination. If None, batch-evaluate all illuminations. Defaults to None.

        Returns:
            dict: results for total, scattered and incident field's Poynting vector (keys: "tot", "sca", "inc")
        """
        nf_S = self.get_nearfield(
            wavelength=wavelength,
            r_probe=r_probe,
            illumination_index=illumination_index,
            **kwargs,
        )

        # add positions
        nf_S["r_probe"] = nf_S["tot"].get_positions()

        # overwrite Field instances by the Poynting vectors
        for which in ["tot", "sca", "inc"]:
            nf_S[which] = nf_S[which].get_poynting()

        return nf_S

    def get_energy_flux(
        self, wavelength, r_probe=None, illumination_index=None, **kwargs
    ):
        """calculate the energy flux (time averaged Poynting vector) at positions `r_probe`

        kwargs (such as `batch_size`) are passed to :func:`torchgdm.postproc.fields.nf`.

        Args:
            sim (:class:`torchgdm.Simulation`): simulation instance
            wavelength (float): evaluation wavelength (in nm)
            r_probe (dict, optional): probe locations describing dict (gen. from `tools.geometry`).  Defaults to None, in which case all positions of the simulation structures are used
            illumination_index (int, optional): optional index of a specific illumination. If None, batch-evaluate all illuminations. Defaults to None.

        Returns:
            dict: results for total, scattered and incident field's time averaged Poynting vector (keys: "tot", "sca", "inc")
        """
        nf_S = self.get_nearfield(
            wavelength=wavelength,
            r_probe=r_probe,
            illumination_index=illumination_index,
            **kwargs,
        )

        # add positions
        nf_S["r_probe"] = nf_S["tot"].get_positions()

        # overwrite Field instances by the time averaged Poynting vectors
        for which in ["tot", "sca", "inc"]:
            nf_S[which] = nf_S[which].get_energy_flux()

        return nf_S

    def get_green(
        self,
        r_probe: torch.Tensor,
        r_source: torch.Tensor,
        wavelength: float,
        use_sim_copy=True,
        progress_bar=True,
        verbose=0,
        **kwargs,
    ):
        """calculate the Green's tensor in presence of the structure(s)

        kwargs (such as `batch_size`) are passed to :func:`tg.postproc.green.G`.

        Args:
            sim (`torchgdm.Simulation`): simulation
            r_probe (torch.Tensor): probe position(s)
            r_source (torch.Tensor): source location(s)
            wavelength (float): in nm
            use_sim_copy (bool, optional): Use copy of simulation or use simulation in-place. May not work in some autograd scenario. Defaults to True.
            progress_bar (bool, optional): Show progress bar. Defaults to True.
            verbose (bool, optional): Print status of underlying simulation call. Defaults to False.

        Returns:
            dict: Green's tensors for all source/probe position combinations:
                - "G_6x6": full 6x6 tensor
                - "G_Ep": electric-electric 3x3 tensor
                - "G_Em": electric-magnetic 3x3 tensor
                - "G_Hp": magnetic-electric 3x3 tensor
                - "G_Hm": magnetic-magnetic 3x3 tensor
        """
        import torchgdm as tg

        if r_probe is None:
            r_probe = self.get_all_positions()

        G = tg.postproc.green.G(
            self,
            r_probe=r_probe,
            r_source=r_source,
            wavelength=wavelength,
            use_sim_copy=use_sim_copy,
            progress_bar=progress_bar,
            verbose=verbose,
            **kwargs,
        )

        return G

    def get_ldos(
        self,
        r_probe: torch.Tensor,
        wavelength: float,
        progress_bar=True,
        verbose=False,
        **kwargs,
    ):
        """calculate the LDOS close to the structure(s)

        kwargs (such as `batch_size`) are passed to :func:`torchgdm.postproc.fields.nf`.

        Args:
            sim (`torchgdm.Simulation`): simulation
            r_probe (torch.Tensor): probe position(s)
            wavelength (float): in nm
            progress_bar (bool, optional): Show progress bar. Defaults to True.
            verbose (bool, optional): Print status info. Defaults to False.


        Returns:
            dict: Green's tensors, partial and averaged LDOS all probe positions:
                - "G_ii": full 6x6 tensor
                - "ldos_partial": partial electric (first 3) and magnetic (last 3) LDOS. (Diagonal elements of Green's tensor)
                - "ldos_e": full electric LDOS
                - "ldos_m": full magnetic LDOS
        """
        import torchgdm as tg

        if r_probe is None:
            r_probe = self.get_all_positions()

        ldos = tg.postproc.green.ldos(
            self,
            r_probe=r_probe,
            wavelength=wavelength,
            progress_bar=progress_bar,
            verbose=verbose,
            **kwargs,
        )

        return ldos

    def get_farfield(self, wavelength, r_probe, illumination_index=None, **kwargs):
        """calculate the far-field (electric and magnetic) at positions `r_probe`

        kwargs (such as `batch_size`) are passed to :func:`torchgdm.postproc.fields.nf`.

        Args:
            sim (:class:`torchgdm.Simulation`): simulation instance
            wavelength (float): evaluation wavelength (in nm)
            r_probe (dict, optional): probe locations describing dict (gen. from `tools.geometry`). Defaults to None, in which case full hemisphere coordinates are used
            illumination_index (int, optional): optional index of a specific illumination. If None, batch-evaluate all illuminations. Defaults to None.

        Returns:
            dict: results for total, scattered and incident fields in instances of :class:`torchgdm.Field`
        """
        import torchgdm as tg

        ff = tg.postproc.fields.ff(
            self,
            wavelength=wavelength,
            r_probe=r_probe,
            illumination_index=illumination_index,
            **kwargs,
        )

        return ff

    # - rasterscan
    def get_rasterscan(self, func, wavelength, kw_r="r_focus", **kwargs):
        """Get rasterscan from a "scan-position" parameters `kw_r` and evaluation function `func`

        `kw_r` must be an attribute of the available illuminations, defining
        some position (3-tuple), this is used as the raster-scan position for each evaluation.

        kwargs are passed to `func`.

        Args:
            func (callable): postprocessing function, from :mod:`tg.postproc`
            wavelength (float): evaluation wavelength (in nm)
            kw_r (str): kwarg used for scan position of rasterscan

        Returns:
            dict: spectrum results
        """
        from torchgdm.tools.batch import calc_rasterscan

        rs_res = calc_rasterscan(self, func, wavelength=wavelength, kw_r="r_focus")
        return rs_res

    # - spectra
    def get_spectra(self, func, **kwargs):
        """Get spectra using all available wavelengths for evaluation function `func`

        kwargs are passed to `func`

        Args:
            func (callable): postprocessing function, from :mod:`tg.postproc`

        Returns:
            dict: spectrum results
        """
        from torchgdm.tools.batch import calc_spectrum

        nf_spec = calc_spectrum(self, func, **kwargs)
        return nf_spec

    def get_spectra_scs(self, **kwargs):
        """total scattering, absorption and extinction cross section spectra

        This function also returns extinction and absorption cross-sections, which are calculated as byproducts.

        kwargs (such as `batch_size`) are passed to :func:`torchgdm.postproc.crosssect.scs`.

        Args:
            sim (:class:`torchgdm.Simulation`): simulation instance
            illumination_index (int, optional): optional index of a specific illumination. If None, batch-evaluate all illuminations. Defaults to None.
            normalize_to_local_e0 (bool, optional): Whether to normalize to local illumination amplitude. Can be useful to get an approximate cross-section for non-plane wave illuminations. Defaults to False.
            radiative_correction (bool, optional): Whether to add radiative correction term. Defaults to True.

        Returns:
            dict: dictionaty containing the scattering, absorption and extinction cross section spectra
        """
        import torchgdm as tg

        scs_spec = tg.tools.batch.calc_spectrum(
            self, tg.postproc.crosssect.scs, **kwargs
        )
        return scs_spec

    def get_crosssections(self, **kwargs):
        """total scattering, absorption and extinction cross section spectra

        *Note:* this is an alias for :func:`Simulation.get_spectra_scs`.

        kwargs (such as `batch_size`) are passed to :func:`torchgdm.postproc.crosssect.scs`.

        Args:
            sim (:class:`torchgdm.Simulation`): simulation instance
            illumination_index (int, optional): optional index of a specific illumination. If None, batch-evaluate all illuminations. Defaults to None.
            normalize_to_local_e0 (bool, optional): Whether to normalize to local illumination amplitude. Can be useful to get an approximate cross-section for non-plane wave illuminations. Defaults to False.
            radiative_correction (bool, optional): Whether to add radiative correction term. Defaults to True.

        Returns:
            dict: dictionaty containing the scattering, absorption and extinction cross section spectra
        """
        return self.get_spectra_scs(**kwargs)

    def get_spectra_ecs(self, **kwargs):
        """total exctinction cross section spectra

        kwargs (such as `batch_size`) are passed to :func:`torchgdm.postproc.crosssect.ecs`.

        Args:
            sim (:class:`torchgdm.Simulation`): simulation instance
            illumination_index (int, optional): optional index of a specific illumination. If None, batch-evaluate all illuminations. Defaults to None.
            normalize_to_local_e0 (bool, optional): Whether to normalize to local illumination amplitude. Can be useful to get an approximate cross-section for non-plane wave illuminations. Defaults to False.

        Returns:
            dict: dictionaty containing the extinction cross section spectra
        """
        import torchgdm as tg

        ecs_spec = tg.tools.batch.calc_spectrum(
            self, tg.postproc.crosssect.ecs, **kwargs
        )
        return ecs_spec

    def get_spectra_acs(self, **kwargs):
        """total absorption cross section spectra

        kwargs (such as `batch_size`) are passed to :func:`torchgdm.postproc.crosssect.acs`.

        Args:
            sim (:class:`torchgdm.Simulation`): simulation instance
            illumination_index (int, optional): optional index of a specific illumination. If None, batch-evaluate all illuminations. Defaults to None.
            normalize_to_local_e0 (bool, optional): Whether to normalize to local illumination amplitude. Can be useful to get an approximate cross-section for non-plane wave illuminations. Defaults to False.

        Returns:
            dict: dictionaty containing the absorption cross section spectra
        """
        import torchgdm as tg

        ecs_spec = tg.tools.batch.calc_spectrum(
            self, tg.postproc.crosssect.ecs, **kwargs
        )
        return ecs_spec

    def get_spectra_nf(self, r_probe=None, **kwargs):
        """Get spectra of complex nearfields at all available wavelengths at positions `r_probe`

        kwargs (such as `batch_size`) are passed to :func:`torchgdm.postproc.fields.nf`.

        Args:
            r_probe (dict, optional): probe locations describing dict (gen. from `tools.geometry`). Defaults to None, in which case all positions of the simulation structures are used
            illumination_index (int, optional): optional index of a specific illumination. If None, batch-evaluate all illuminations. Defaults to None.

        Returns:
            dict: contains results for total, scattered and incident fields in instances of :class:`torchgdm.Field`
        """
        import torchgdm as tg

        if r_probe is None:
            r_probe = self.get_all_positions()

        nf_spec = tg.tools.batch.calc_spectrum(
            self, tg.postproc.fields.nf, r_probe=r_probe, **kwargs
        )
        return nf_spec

    def get_spectra_nf_intensity_e(self, r_probe=None, **kwargs):
        """Get spectrum of integrated electric nearfield intensities

        kwargs (such as `batch_size`) are passed to :func:`torchgdm.postproc.fields.nf`.

        Args:
            r_probe (dict, optional): probe locations describing dict (gen. from `tools.geometry`). Defaults to None, in which case all positions of the simulation structures are used
            illumination_index (int, optional): optional index of a specific illumination. If None, batch-evaluate all illuminations. Defaults to None.

        Returns:
            dict: contains results for total (key "tot"), scattered (key "sca") and incident (key "inc") electric field intensity
        """
        nf_spec = self.get_spectra_nf(r_probe=r_probe, **kwargs)

        for which in ["tot", "sca", "inc"]:
            nf_spec[which] = torch.stack(
                [f.get_integrated_efield_intensity() for f in nf_spec[which]]
            )

        return nf_spec

    def get_spectra_nf_intensity_h(self, r_probe=None, **kwargs):
        """Get spectrum of integrated magnetic nearfield intensities

        kwargs (such as `batch_size`) are passed to :func:`torchgdm.postproc.fields.nf`.

        Args:
            r_probe (dict, optional): probe locations describing dict (gen. from `tools.geometry`). Defaults to None, in which case all positions of the simulation structures are used
            illumination_index (int, optional): optional index of a specific illumination. If None, batch-evaluate all illuminations. Defaults to None.

        Returns:
            dict: contains results for total (key "tot"), scattered (key "sca") and incident (key "inc") magnetic field intensity
        """
        nf_spec = self.get_spectra_nf(r_probe=r_probe, **kwargs)

        for which in ["tot", "sca", "inc"]:
            nf_spec[which] = torch.stack(
                [f.get_integrated_hfield_intensity() for f in nf_spec[which]]
            )

        return nf_spec

    def get_spectra_nf_intensity_e_inside(self):
        """Get spectrum of integrated electric nearfield intensities inside structure"""
        import torchgdm as tg

        nf_int_e = tg.tools.batch.calc_spectrum(
            self, tg.postproc.fields.integrated_nf_intensity_e_inside
        )

        return nf_int_e

    def get_spectra_nf_intensity_h_inside(self):
        """Get spectrum of integrated magnetic nearfield intensities inside structure"""
        import torchgdm as tg

        nf_int_h = tg.tools.batch.calc_spectrum(
            self, tg.postproc.fields.integrated_nf_intensity_h_inside
        )

        return nf_int_h

    def get_spectra_ff(self, r_probe=None, **kwargs):
        """Get spectra of complex far-fields at all available wavelengths at positions `r_probe`

        kwargs (such as `batch_size`) are passed to :func:`torchgdm.postproc.fields.ff`.

        Args:
            sim (:class:`torchgdm.Simulation`): simulation instance
            r_probe (dict, optional): probe locations describing dict (gen. from `tools.geometry`). Defaults to None, in which case all positions of the simulation structures are used
            illumination_index (int, optional): optional index of a specific illumination. If None, batch-evaluate all illuminations. Defaults to None.

        Returns:
            dict: contains results for total, scattered and incident fields in instances of :class:`torchgdm.Field`
        """
        import torchgdm as tg

        ff_spec = tg.tools.batch.calc_spectrum(
            self, tg.postproc.fields.ff, r_probe=r_probe, **kwargs
        )
        return ff_spec

    def get_spectra_ff_intensity(self, r_probe=None, **kwargs):
        """Get spectrum of integrated far-field intensities

        kwargs (such as `batch_size`) are passed to :func:`torchgdm.postproc.fields.ff`.

        Args:
            sim (:class:`torchgdm.Simulation`): simulation instance
            r_probe (dict or list, optional): probe locations (gen. from `tools.geometry`). Defaults to None, in which case intergration goes over full hemisphere
            illumination_index (int, optional): optional index of a specific illumination. If None, batch-evaluate all illuminations. Defaults to None.

        Returns:
            dict: contains results for total (key "tot"), scattered (key "sca") and incident (key "inc") far-field intensity
        """
        ff_spec = self.get_spectra_ff(r_probe, **kwargs)

        for which in ["tot", "sca", "inc"]:
            ff_spec[which] = torch.stack(
                [f.get_integrated_efield_intensity() for f in ff_spec[which]]
            )

        return ff_spec

    def get_spectra_multipole(self, **kwargs):
        """Get spectrum of exact multipole decomposition

        This returns the spectra for the full multipole moments of dipole and quadrupole order.
        For more detailed documentation, see :func:`torchgdm.postproc.multipole.decomposition_exact`.
        kwargs (such as `batch_size`) are passed to :func:`torchgdm.postproc.multipole.decomposition_exact`.

        Args:
            sim (:class:`torchgdm.Simulation`): simulation instance
            illumination_index (int, optional): optional index of a specific illumination. If None, batch-evaluate all illuminations. Defaults to None.
            r0 (torch.Tensor, optional): [x,y,z] position of multipole decomposition development. Defaults to None, in which case the center of gravity is used.
            epsilon (float, optional): positions too close to r0 will moved away from r0 by epsilon (in units of step) to avoid numerical divergence of the Bessel terms. Defaults to 0.1.
            long_wavelength_approx (bool, optional): if True, use long wavelength approximation. Defaults to False.

        Returns:
            dict: each element contains the spectrum for one multipole moment. dipoles are rank-1 (3-vectors), quadrupoles are rank 2 (3x3 tensors):
                - 'ed_tot': electric dipole (full)
                - 'md': magnetic dipole
                - 'eq_tot': electric quadrupole (full)
                - 'mq': magnetic quadrupole
                - 'ed_1': electric dipole (first order)
                - 'ed_toroidal': toroidal dipole
                - 'eq1': electric quadrupole (first order)
                - 'eq_toroidal': toroidal quadrupole
        """
        import torchgdm as tg

        mpd_spec = tg.tools.batch.calc_spectrum(
            self, tg.postproc.multipole.decomposition_exact, **kwargs
        )
        return mpd_spec

    def get_spectra_multipole_scs(self, **kwargs):
        """spectra of multipole decomposition of extinction cross section

        Returns the exact multipole decomposition of the extinction cross section spectra: electric and magnetic dipole and quadrupole moments.
        For more detailed documentation, see :func:`torchgdm.postproc.multipole.ecs`.
        kwargs (such as `batch_size`) are passed to :func:`torchgdm.postproc.multipole.ecs`.

        For details about the extinction section of multipole moments, see:
            Evlyukhin, A. B. et al. *Multipole analysis of light scattering by
            arbitrary-shaped nanoparticles on a plane surface.*,
            JOSA B 30, 2589 (2013)

        Args:
            illumination_index (int, optional): optional index of a specific illumination. If None, batch-evaluate all illuminations. Defaults to None.
            r0 (torch.Tensor, optional): [x,y,z] position of multipole decomposition development. Defaults to None, in which case the center of gravity is used.
            epsilon (float, optional): positions too close to r0 will moved away from r0 by epsilon (in units of step) to avoid numerical divergence of the Bessel terms. Defaults to 0.1.
            eps_dd (float, optional): numerical integration step for field gradients calc. (in nm). Required for e/m quadrupoles. Defaults to 0.1.
            normalization_E0 (bool, optional): Normalize to illumination amplitude at `r0`. Can be useful to get approximate results for non-plane wave illumination. Defaults to False.
            long_wavelength_approx (bool, optional): if True, use long wavelength approximation. Defaults to False.

        Returns:
            dict:
            - 'ecs_ed': electric dipole extinction cross section spectra (in nm^2)
            - 'ecs_md': magnetic dipole extinction cross section spectra (in nm^2)
            - 'ecs_eq': electric quadrupole extinction cross section spectra (in nm^2)
            - 'ecs_mq': magnetic quadrupole extinction cross section spectra (in nm^2)
        """
        import torchgdm as tg

        scs_mpd_spec = tg.tools.batch.calc_spectrum(
            self, tg.postproc.multipole.scs, **kwargs
        )
        return scs_mpd_spec

    def get_spectra_multipole_ecs(self, **kwargs):
        """spectrum of multipole decomposition of scattering cross section

        Returns the exact multipole decomposition of the scattering cross section spectra: electric and magnetic dipole and quadrupole moments.
        For more detailed documentation, see :func:`torchgdm.postproc.multipole.scs`.
        kwargs (such as `batch_size`) are passed to :func:`torchgdm.postproc.multipole.scs`.

        For details about the exact multipole formalism and scs calculation, see:
            Alaee, R., Rockstuhl, C. & Fernandez-Corbaton, I. *An electromagnetic
            multipole expansion beyond the long-wavelength approximation.*
            Optics Communications 407, 17–21 (2018)

        Args:
            illumination_index (int, optional): optional index of a specific illumination. If None, batch-evaluate all illuminations. Defaults to None.
            with_toroidal (bool, optional): whether to add toroidal moments to electric dipole and quadrupole. Defaults to True.
            r0 (torch.Tensor, optional): [x,y,z] position of multipole decomposition development. Defaults to None, in which case the center of gravity is used.
            epsilon (float, optional): positions too close to r0 will moved away from r0 by epsilon (in units of step) to avoid numerical divergence of the Bessel terms. Defaults to 0.1.
            normalization_E0 (bool, optional): Normalize to illumination amplitude at `r0`. Can be useful to get approximate results for non-plane wave illumination. Defaults to False.
            long_wavelength_approx (bool, optional): if True, use long wavelength approximation. Defaults to False.

        Returns:
            dict:
            - 'scs_ed': electric dipole scattering cross section spectra (in nm^2)
            - 'scs_md': magnetic dipole scattering cross section spectra (in nm^2)
            - 'scs_eq': electric quadrupole scattering cross section spectra (in nm^2)
            - 'scs_mq': magnetic quadrupole scattering cross section spectra (in nm^2)
        """
        import torchgdm as tg

        scs_mpd_spec = tg.tools.batch.calc_spectrum(
            self, tg.postproc.multipole.ecs, **kwargs
        )
        return scs_mpd_spec
