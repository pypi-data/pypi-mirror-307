# -*- coding: utf-8 -*-
"""2D visualization tools based on matplotlib

requirements:
 - numpy
 - matplotlib
 - scipy (for scalar fields)
 
"""
from . import geo2d, vec2d, scalar2d

from .geo2d import _reset_color_iterator

from .geo2d import structure, contour
from .vec2d import vectorfield, vectorfield_inside, streamlines_energy_flux
from .scalar2d import field_intensity, field_amplitude
from .scalar2d import _scalarfield as scalarfield
