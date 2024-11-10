# -*- coding: utf-8 -*-
"""base classes for structures
"""
import warnings

import torch

from torchgdm.constants import DTYPE_FLOAT, DTYPE_COMPLEX, STRUCTURE_IDS
from torchgdm.tools.misc import get_default_device
from torchgdm.tools.geometry import test_structure_distances


# --- base class structure container
class StructBase:
    """base class for structure container

    Defines the polarizabilities and self-terms
    """

    __name__ = "structure base class"

    def __init__(self, radiative_correction=True, device: torch.device = None):
        """Initialization"""
        if device is None:
            self.device = get_default_device()
        else:
            self.device = device

        self.n_dim = -1  # problem dimension needs to be set by child class

        self.positions = torch.as_tensor(
            [], dtype=DTYPE_FLOAT, device=self.device
        )  # shape: (N, 3)
        self.step = torch.as_tensor(
            [], dtype=DTYPE_FLOAT, device=self.device
        )  # shape: (N, 3)

        self.mesh_normalization_factor = 1.0

        self.radiative_correction = radiative_correction

        # a structure may have a pure electric or pure magnetic response
        # this can be specified, which will reduce the memory and
        # computation requirements for these scatterers
        self.evaluation_terms = ["E", "H"]

        # unique identifier
        self.id = next(STRUCTURE_IDS)

    def __add__(self, other):
        if issubclass(type(other), StructBase):
            # add a structure: try combining both.
            return self.combine(other)
        elif len(other) == 3:
            # add a 3-tuple: Try shift
            return self.translate(other)
        else:
            raise ValueError("Unknown addition.")

    def __sub__(self, other):
        if issubclass(type(other), StructBase):
            # subtract a structure:  TODO (not clear yet what to do)
            raise NotImplementedError(
                "Removing a structure from another is not implemented yet."
            )
        elif len(other) == 3:
            # subtract a 3-tuple: Try shift
            return self.translate(
                -1 * torch.as_tensor(other, dtype=DTYPE_FLOAT, device=self.device)
            )
        else:
            raise ValueError("Unknown addition.")

    def __repr__(self, verbose: bool = False):
        """description about structure"""
        out_str = " ------ base structure class - doesn't define anything yet -------"
        return out_str

    def set_device(self, device):
        """move all tensors of the class to device"""
        self.device = device
        self.positions = self.positions.to(device=device)

    # --- plot placeholder
    def plot(self):
        raise NotImplementedError("Plot not implement yet.")

    def plot_contour(self, **kwargs):
        """if not implemented: fall back to full structure plot"""
        return self.plot(**kwargs)

    def plot3d(self):
        raise NotImplementedError("3D Plot not implement yet.")

    # --- common interface for positions / step
    def get_all_positions(self) -> torch.Tensor:
        return self.positions

    def get_source_validity_radius(self) -> torch.Tensor:
        """get the radius of the validity zone of each effective source"""

        # effective pola structure: step=diameter. return step / 2
        if hasattr(self, "full_geometries"):
            _r = self.step / 2
        # discretized structure: step=cell side length. return sqrt(2) * step / 2
        else:
            _r = 2**0.5 * self.step / 2
        return _r

    # --- self-terms
    def get_selfterm_6x6(self, wavelength: float, environment) -> torch.Tensor:
        """return list of magneto-electric self-term tensors (6x6) at each meshpoint

        Args:
            wavelength (float): in nm
            environment (environment class): 3D environement class

        Returns:
            torch.Tensor: 6x6 selfterm tensor
        """
        selfterm_6x6 = torch.cat(
            [
                torch.cat(
                    [
                        self.get_selfterm_pE(wavelength, environment),
                        self.get_selfterm_pH(wavelength, environment),
                    ],
                    dim=-1,
                ),
                torch.cat(
                    [
                        self.get_selfterm_mE(wavelength, environment),
                        self.get_selfterm_mH(wavelength, environment),
                    ],
                    dim=-1,
                ),
            ],
            dim=-2,
        )
        return selfterm_6x6

    def get_selfterm_pE(self, wavelength: float, environment):
        """return list of 'EE' self-term tensors (3x3) at each meshpoint"""
        return torch.zeros(
            (len(self.positions), 3, 3), device=self.device, dtype=DTYPE_COMPLEX
        )

    def get_selfterm_mE(self, wavelength: float, environment):
        """return list of 'HE' self-term tensors (3x3) at each meshpoint"""
        return torch.zeros(
            (len(self.positions), 3, 3), device=self.device, dtype=DTYPE_COMPLEX
        )

    def get_selfterm_pH(self, wavelength: float, environment):
        """return list of 'EH' self-term tensors (3x3) at each meshpoint"""
        return torch.zeros(
            (len(self.positions), 3, 3), device=self.device, dtype=DTYPE_COMPLEX
        )

    def get_selfterm_mH(self, wavelength: float, environment):
        """return list of 'HH' self-term tensors (3x3) at each meshpoint"""
        return torch.zeros(
            (len(self.positions), 3, 3), device=self.device, dtype=DTYPE_COMPLEX
        )

    # --- polarizabilities
    def get_polarizability_6x6(self, wavelength: float, environment) -> torch.Tensor:
        """return list of magneto-electric polarizability tensors (6x6) at each meshpoint

        Args:
            wavelength (float): in nm
            environment (environment class): 3D environement class

        Returns:
            torch.Tensor: 6x6 polarizability tensor
        """
        alpha_6x6 = torch.cat(
            [
                torch.cat(
                    [
                        self.get_polarizability_pE(wavelength, environment),
                        self.get_polarizability_pH(wavelength, environment),
                    ],
                    dim=-1,
                ),
                torch.cat(
                    [
                        self.get_polarizability_mE(wavelength, environment),
                        self.get_polarizability_mH(wavelength, environment),
                    ],
                    dim=-1,
                ),
            ],
            dim=-2,
        )
        return alpha_6x6

    def get_polarizability_pmE_6x3(
        self, wavelength: float, environment
    ) -> torch.Tensor:
        alpha_pmE_6x3 = torch.cat(
            [
                self.get_polarizability_pE(wavelength, environment),
                self.get_polarizability_mE(wavelength, environment),
            ],
            dim=-2,
        )
        return alpha_pmE_6x3

    def get_polarizability_pEH_3x6(
        self, wavelength: float, environment
    ) -> torch.Tensor:
        """return list of magneto-electric self-term tensors (6x6) at each meshpoint"""
        alpha_pEH_3x6 = torch.cat(
            [
                self.get_polarizability_pE(wavelength, environment),
                self.get_polarizability_pH(wavelength, environment),
            ],
            dim=-1,
        )
        return alpha_pEH_3x6

    def get_polarizability_pmH_6x3(
        self, wavelength: float, environment
    ) -> torch.Tensor:
        alpha_pmH_6x3 = torch.cat(
            [
                self.get_polarizability_pH(wavelength, environment),
                self.get_polarizability_mH(wavelength, environment),
            ],
            dim=-2,
        )
        return alpha_pmH_6x3

    def get_polarizability_mEH_3x6(
        self, wavelength: float, environment
    ) -> torch.Tensor:
        """return list of magneto-electric self-term tensors (6x6) at each meshpoint"""
        alpha_pmH_3x6 = torch.cat(
            [
                self.get_polarizability_mE(wavelength, environment),
                self.get_polarizability_mH(wavelength, environment),
            ],
            dim=-1,
        )
        return alpha_pmH_3x6

    def get_polarizability_pE(self, wavelength: float, environment):
        """return list of EE polarizability tensors (3x3) at each meshpoint"""
        return torch.zeros(
            (len(self.positions), 3, 3), device=self.device, dtype=DTYPE_COMPLEX
        )

    def get_polarizability_mE(self, wavelength: float, environment):
        """return list of HE polarizability tensors (3x3) at each meshpoint"""
        return torch.zeros(
            (len(self.positions), 3, 3), device=self.device, dtype=DTYPE_COMPLEX
        )

    def get_polarizability_pH(self, wavelength: float, environment):
        """return list of EH polarizability tensors (3x3) at each meshpoint"""
        return torch.zeros(
            (len(self.positions), 3, 3), device=self.device, dtype=DTYPE_COMPLEX
        )

    def get_polarizability_mH(self, wavelength: float, environment):
        """return list of HH polarizability tensors (3x3) at each meshpoint"""
        return torch.zeros(
            (len(self.positions), 3, 3), device=self.device, dtype=DTYPE_COMPLEX
        )

    # --- geometry operations
    def copy(self, positions=None, rotation_angles=None):
        """(batch) copy structre to new position(s)

        optionally, the copied structures can also be batch-rotated along the `z` axis.

        Args:
            positions (list, optional): list of new positions to create copies at. If None, create a single, identical copy. Defaults to None.
            rotation_angles (list, optional): list of rotation angles for the copies. If None, keep orientations. Defaults to None.

        Returns:
            :class:`StructBase`: new structure
        """
        if type(positions) == dict:
            positions = positions["r_probe"]

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

            if rotation_angles is None:
                rotation_angles = torch.zeros(
                    len(positions), device=self.device, dtype=DTYPE_FLOAT
                )
            else:
                assert len(rotation_angles) == len(positions)
                assert len(rotation_angles.shape) == 1

            new_struct_list = []
            for _r, _a in zip(positions, rotation_angles):
                _struct = self.copy()
                _struct.set_center_of_mass(_r)
                if _a != 0:
                    _struct = _struct.rotate(_a)
                new_struct_list.append(_struct)

            new_struct = new_struct_list.pop(0)
            for _s in new_struct_list:
                new_struct = new_struct.combine(_s, inplace=True)

            return new_struct

    def get_geometric_crosssection(self, projection="xy"):
        """get geometric cross section the structure in nm^2

        Args:
            projection (str, optional): cartesian projection of cross section. Defaults to "xy"

        Returns:
            float: geometric cross section in nm^2
        """
        from torchgdm.tools.geometry import get_geometric_crosssection

        return get_geometric_crosssection(self, projection)

    def get_center_of_mass(self):
        """return the center of mass"""
        return torch.mean(self.positions, axis=0)

    def set_center_of_mass(self, r0_new: torch.Tensor):
        """move center of mass to new position `r0_new` (in-place)"""
        r0_new = torch.as_tensor(r0_new, device=self.positions.device)

        if len(r0_new.shape) != 1:
            if len(r0_new) not in [2, 3]:
                raise ValueError("`r0_new` needs to be (X,Y) or (X,Y,Z) tuple.")
        r0_old = self.get_center_of_mass()

        if len(r0_new) == 2:
            warnings.warn("Got 2-vector, assume xy coordinates.")
            r0_new = torch.as_tensor(
                [r0_new[0], r0_new[1], r0_old[2]], device=self.positions.device
            )

        # move
        self.positions -= r0_old  # move to origin
        self.positions += r0_new  # move to new location
        self.r0 = self.get_center_of_mass()

    def translate(self, vector):
        """return copy, moved by `vector`"""
        _shifted = self.copy()
        _shifted.positions += torch.as_tensor(
            vector, dtype=DTYPE_FLOAT, device=self.device
        ).unsqueeze(0)
        _shifted.r0 = _shifted.get_center_of_mass()
        return _shifted

    def rotate(self, alpha, center=torch.as_tensor([0.0, 0.0, 0.0]), axis="z"):
        raise NotImplementedError(
            "`rotate` is not yet implemented in the current class."
        )

    def combine(self, other, inplace=False, on_distance_violation="error"):
        """combine with a second structure (requires definition at same wavelengths!)

        Structures must be of same coupling type (electric / magnetic)

        Args:
            other (_type_): _description_
            inplace (bool, optional): Don't copy original structure, just add other structure. Can be necessary e.g. when gradients are required. Defaults to False.
            on_distance_violation (str, optional): can be "error", "warn", None (do nothing). Defaults to "error".

        Returns:
            :class:`StructBase`: new structure
        """
        if inplace:
            new_struct = self
        else:
            new_struct = self.copy()

        assert self.mesh_normalization_factor == other.mesh_normalization_factor
        assert self.radiative_correction == other.radiative_correction
        assert self.evaluation_terms == other.evaluation_terms
        assert type(self) == type(other)

        N_dist1, N_dist2 = test_structure_distances(
            self, other, on_distance_violation=on_distance_violation
        )

        new_struct.positions = torch.concatenate(
            [new_struct.positions, other.positions], dim=0
        )
        new_struct.step = torch.concatenate([new_struct.step, other.step], dim=0)
        new_struct.zeros = torch.concatenate([new_struct.zeros, other.zeros], dim=0)
        new_struct.materials = new_struct.materials + other.materials

        new_struct.r0 = self.get_center_of_mass()  # center of gravity
        return new_struct
