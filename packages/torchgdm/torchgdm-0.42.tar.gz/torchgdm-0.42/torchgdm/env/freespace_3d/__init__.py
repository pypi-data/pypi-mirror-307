# encoding=utf-8
"""contains collections of Green's tensors,
describing environments and their boundary conditions
"""
from . import inc_fields

from .dyads import EnvHomogeneous3D

from .inc_fields import NullField
from .inc_fields import PlaneWave
from .inc_fields import GaussianParaxial
from .inc_fields import ElectricDipole
from .inc_fields import MagneticDipole