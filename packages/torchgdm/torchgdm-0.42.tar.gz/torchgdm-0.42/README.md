![torchgdm logo](https://homepages.laas.fr/pwiecha/_image_for_ext/torchgdm_logo.png)

# TorchGDM
> nano-optics full-field solver, written in PyTorch.

TorchGDM is a PyTorch implementation of the [Green's dyadic method (GDM)](https://doi.org/10.1088/0034-4885/68/8/R05), a electro-dynamics full-field volume integral technique. It's main features are mixed simulations **combining volume discretized and effective e/m dipole-pair polarizabilities**, as well as the general support of torch's **automatic differentiation**. 

TorchGDM is available on the [gitlab repository](https://gitlab.com/wiechapeter/torchgdm) and via [PyPi and pip](https://pypi.org/project/torchgdm/).  Please visit also the [TorchGDM documentation website](https://homepages.laas.fr/pwiecha/torchgdm_doc/).

TorchGDM is originally based on various theoretical works by [Christian Girard](https://scholar.google.de/citations?user=P3HnK28AAAAJ) at CEMES (see e.g. [Ch. Girard 2005 Rep. Prog. Phys. 68 1883](https://doi.org/10.1088/0034-4885/68/8/R05)), with contributions from G. Colas des Francs, A. Arbouet, R. Marty, C. Majorel, A. Patoux, Y. Brûlé and P. R. Wiecha.

If you use TorchGDM for your projects, please cite it.


## Getting started

Simulate and plot the scattering cross section spectrum between 550nm and 950nm of a silicon nano-cube (200nm side length), placed in vacuum, illuminated by an x-polarized plane wave:

```python
import torch
import matplotlib.pyplot as plt
import torchgdm as tg

# --- simulation setup
# - vacuum environment
mat_env = tg.materials.MatConstant(eps=1.0)
env = tg.env.freespace_3d.EnvHomogeneous3D(env_material=mat_env)

# - illumination field(s) and wavelength
wavelengths = torch.linspace(550.0, 950.0, 25)
plane_wave = tg.env.freespace_3d.PlaneWave(e0p=1.0, e0s=0.0)

# - discretized structure
structure = tg.struct.StructDiscretizedCubic3D(
    discretization_config=tg.struct.volume.cube(l=8),
    step=30.0,    # in nm
    materials=tg.materials.MatDatabase("GaN"),
)

# - define and run simulation.
sim = tg.Simulation(
    structures=[structure],
    illumination_fields=[plane_wave],
    environment=env,
    wavelengths=wavelengths,
)
sim.plot_structure()  # visualize structure
sim.run()             # run the main simulation

# - post-processing: cross sections
cs_results = sim.get_crosssections()

# plot
plt.figure(figsize=(5, 4))
plt.plot(tg.to_np(wavelengths), tg.to_np(cs_results["scs"]))
plt.xlabel("wavelength (nm)")
plt.ylabel("scs (nm^2)")
plt.show()
```


### GPU support

For GPU support, all you need is a [GPU enabled version of pytorch](https://pytorch.org/get-started/locally/). TorchGDM was tested with [CUDA](https://developer.nvidia.com/cuda-zone). CUDA can be enabled by using:

```python
  import torchgdm as tg
  tg.use_cuda(True)
```

Alternatively, GPU usage can be fine controlled by passing the `device="cuda"` argument when setting up the simulation class:

```python
  sim = tg.Simulation(..., device="cuda")
```


## Features

List of features

General:

* pure python
* run on CPU and GPU, parallelized and vectorized
* full support of torch's automatic differentiation

Simulations:

* 3D volume discretizations
* 3D effective polarizabilities (dipolar electric and magnetic)
* mix of both 3D types of structures (volume / point-polarizabilities)
* 2D surface discretization (infinitly long geometries)
* global (plane wave, focused Gaussian) and local illumination (point emitter)

Post-processing

* cross sections (extinction, scattering, absorption)
* nearfields and farfields
* optical chirality
* Poynting vector
* field gradients
* exact multipole decomposition
* Green's tensors in complex environments
* LDOS / decay rate
* extract ED/MD point-polarizability tensors
* plotting tools for convenient 2D / 3D visualizations
* ...


## Installing / Requirements

Installation should work via pip on all major operating systems. For now please use the [gitlab repository](https://gitlab.com/wiechapeter/torchgdm) as source, we will publish TorchGDM on PyPi once all main features are implemented and tested. 

```shell
pip install https://gitlab.com/wiechapeter/torchgdm/-/archive/main/torchgdm-main.zip
```

TorchGDM was tested under linux and windows with python versions 3.9 to 3.12. It requires following python packages

- **pytorch** (v2.0+)

Further optional dependencies

- **numpy** (for some tools)
- **scipy** (for some tools)
- **pymiecs** (for Mie theory tools)
- **pyyaml** (support for permittivity data from refractiveindex.info)
- **tqdm** (for progress bars)
- **psutil** (for automatic memory purge)
- **matplotlib** (2d plotting)
- **alphashape** (2d contour plotting)
- **pyvista** (3d visualization, install via: # pip install 'jupyterlab>=3' ipywidgets 'pyvista[all,trame]')

(install all optional dependencies via pip: `pip install numpy scipy pymiecs pyyaml tqdm psutil matplotlib alphashape pyvista`)


## Contributing

If you'd like to contribute, please fork the repository and use a feature
branch. Pull requests are warmly welcome.


## Links

- torchgdm documentation: [https://homepages.laas.fr/pwiecha/torchgdm_doc/](https://homepages.laas.fr/pwiecha/torchgdm_doc/)
- link to PyPi: [https://pypi.org/project/torchgdm/](https://pypi.org/project/torchgdm/)
- gitlab repository: [https://gitlab.com/wiechapeter/torchgdm](https://gitlab.com/wiechapeter/torchgdm)
- issue tracker: [https://gitlab.com/wiechapeter/torchgdm/-/issues](https://gitlab.com/wiechapeter/torchgdm/-/issues)
  - in case of sensitive bugs you can also contact me directly at
    pwiecha|AT|laas|DOT|fr.
- related projects:
  - pyGDM2: [https://homepages.laas.fr/pwiecha/pygdm_doc/](https://homepages.laas.fr/pwiecha/pygdm_doc/)


## Licensing

The code in this project is licensed under the [GNU GPLv3](http://www.gnu.org/licenses/).