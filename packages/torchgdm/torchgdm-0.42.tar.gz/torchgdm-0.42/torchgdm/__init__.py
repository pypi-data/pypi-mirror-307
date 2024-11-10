# encoding=utf-8
#
# Copyright (C) 2023-2024, P. R. Wiecha
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
"""
torchgdm - a full-field electrodynamical solver written in pytorch.
Based on the Green Dyadic Method.
"""

__name__ = "torchgdm"
__version__ = "0.42"
__date__ = "11/09/2024"  # MM/DD/YYY
__license__ = "GPL3"
__status__ = "beta"

__copyright__ = "Copyright 2023-2024, Peter R. Wiecha"
__author__ = "Peter R. Wiecha"
__maintainer__ = "Peter R. Wiecha"
__email__ = "pwiecha@laas.fr"
__credits__ = [
    "Christian Girard",
    "Arnaud Arbouet",
    "Clément Majorel",
    "Sofia Ponomareva",
    "Antoine Azéma",
    "Adelin Patoux",
    "Renaud Marty",
]

# --- populate namespace
from .constants import DEFAULT_DEVICE

device = DEFAULT_DEVICE

# make some functions and classes available at top level
from .simulation import Simulation
from .field import Field
from .tools.misc import to_np, tqdm
from .tools.misc import use_cuda, get_default_device, set_default_device

# make some submodules available at top level
from .visu import visu2d
from .visu import visu3d

# modules
from . import constants
from . import linearsystem
from . import simulation
from . import field

# sub packages
from . import env
from . import materials
from . import struct
from . import postproc
from . import tools
