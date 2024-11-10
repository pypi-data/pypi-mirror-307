# -*- coding: utf-8 -*-
"""3D visualization tools based on pyvista

requirements:
 - numpy
 - pyvista
 
for use in jupyter:
 - trame
 - trame-vtk
 - trame-vuetify
 - ipywidgets
 
install with:

     pip install 'jupyterlab>=3' ipywidgets 'pyvista[all,trame]'
 
"""
from . import geo3d
from . import vec3d

from .geo3d import structure
from .vec3d import vectorfield, vectorfield_inside
