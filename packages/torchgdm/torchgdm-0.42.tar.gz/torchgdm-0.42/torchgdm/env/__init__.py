# encoding=utf-8
"""contains classes necessary for describing simulations in a specific environment:
  - Green's tensors, describing environments and their boundary conditions.
  - illumination fields specific for the environment
"""
from . import freespace_2d
from . import freespace_3d

from .freespace_2d import EnvHomogeneous2D
from .freespace_3d import EnvHomogeneous3D