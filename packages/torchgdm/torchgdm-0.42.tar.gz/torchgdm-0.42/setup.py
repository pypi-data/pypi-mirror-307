# -*- coding: utf-8 -*-
"""manage installation"""
from setuptools import setup, find_namespace_packages, Extension
import os
import re


# =============================================================================
# helper functions to extract meta-info from package
# =============================================================================
def read_version_file(*parts):
    return open(os.path.join(*parts), "r").read()


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


def find_version(*file_paths):
    version_file = read_version_file(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


def find_name(*file_paths):
    version_file = read_version_file(*file_paths)
    version_match = re.search(r"^__name__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find name string.")


def find_author(*file_paths):
    version_file = read_version_file(*file_paths)
    version_match = re.search(r"^__author__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find author string.")


# =============================================================================
# package module list
# =============================================================================
package_list = find_namespace_packages(where=".", include=["torchgdm*"])


# =============================================================================
# main setup
# =============================================================================
setup(
    name=find_name("torchgdm", "__init__.py"),
    version=find_version("torchgdm", "__init__.py"),
    author=find_author("torchgdm", "__init__.py"),
    author_email="pwiecha@laas.fr",
    description=(
        "A python electrodynamical CPU/GPU solver written in PyTorch,"
        "With full support of PyTorch's automatic differentiation."
        "Based on the Green's Dyadic Method (GDM, volume integral technique "
        "in frequency domain)."
    ),
    license="GPLv3+",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    packages=package_list,
    package_data={"torchgdm.materials.data": ["*.yml"]},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Topic :: Scientific/Engineering :: Physics",
        "Environment :: Console",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Intended Audience :: Science/Research",
    ],
    url="https://gitlab.com/wiechapeter/torchgdm",
    download_url="",
    keywords=[
        "volume integral method",
        "green dyadic method",
        "coupled dipoles method",
        "effective polarizabilities",
        "electrodynamical simulations",
        "nano optics",
        "frequency-domain",
        "automatic differentiation",
    ],
    install_requires=["torch>=2.0.0"],
    python_requires=">=3.9",
)
