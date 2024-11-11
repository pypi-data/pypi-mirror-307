import glob
import os

from Cython.Build import cythonize
from setuptools import (
    Extension,
    find_packages,
    setup,
)

# Define the core directory for Cythonization
core_dir = "eclypse/core"

version = "0.6.0"

# Create Cython extensions for all .pyx files in eclypse/core
extensions = [
    Extension(os.path.splitext(file.replace("/", "."))[0], [file])
    for file in glob.glob(f"{core_dir}/**/*.pyx", recursive=True)
]

setup(
    name="eclypse",
    version=version,
    packages=find_packages(
        exclude=["tests*", "docs*"]
    ),  # Include packages, excluding tests/docs
    ext_modules=cythonize(
        extensions,
        compiler_directives={
            "language_level": "3",
            "annotation_typing": False,
            "binding": True,
            "embedsignature": True,
        },
    ),
)
