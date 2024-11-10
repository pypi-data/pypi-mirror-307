# -*- coding: utf-8 -*-
"""package for torchgdm structures
"""
from . import volume
from . import point
from . import surface_2d
from . import line_2d

# - 3D
# from .volume.pola import StructDiscretized3D
from .volume.pola import StructDiscretizedCubic3D
from .volume.pola import StructDiscretizedHexagonal3D

from .point.pola import StructEffPola3D
from .point.pola import StructMieSphereEffPola3D  # Mie core-shell

# - 2D
# from .surface_2d.pola import StructDiscretized2D
from .surface_2d.pola import StructDiscretizedSquare2D

from .line_2d.pola import StructEffPola2D