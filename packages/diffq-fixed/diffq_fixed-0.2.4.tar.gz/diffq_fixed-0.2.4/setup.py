#!/usr/bin/env python3
# Copyright (c) Facebook, Inc. and its affiliates.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
# Inspired from https://github.com/kennethreitz/setup.py

from pathlib import Path

from Cython.Build import cythonize
from setuptools import Extension, setup

NAME = "diffq-fixed"
DESCRIPTION = "Differentiable quantization framework for PyTorch -- fixed for compatibility with Python 3.11+"
URL = "https://github.com/JackismyShephard/diffq"
EMAIL = "jackismyshephard@gmail.com"
AUTHOR = "Alexandre Défossez, Yossi Adi, Gabriel Synnaeve, JackismyShephard"
REQUIRES_PYTHON = ">=3.7.0"

for line in open("diffq/__init__.py"):
    line = line.strip()
    if "__version__" in line:
        context = {}
        exec(line, context)
        VERSION = context["__version__"]

HERE = Path(__file__).parent

try:
    with open(HERE / "README.md", encoding="utf-8") as f:
        long_description = "\n" + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=["diffq"],
    install_requires=["Cython", "numpy", "torch"],
    ext_modules=cythonize([Extension("diffq.bitpack", sources=["bitpack.pyx"])]),
    extras_require={"dev": ["coverage", "flake8", "pdoc3", "torchvision"]},
    include_package_data=True,
    license="Creative Commons Attribution-NonCommercial 4.0 International",
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
)
