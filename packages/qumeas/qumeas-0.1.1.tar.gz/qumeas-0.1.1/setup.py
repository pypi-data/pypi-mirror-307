from skbuild import setup
from setuptools import find_packages
import os, sys


# Read VERSION and write python/qumeas/_version.py
def read_version():
    here = os.path.abspath(os.path.dirname(__file__))
    version_file = os.path.join(here, "VERSION")
    with open(version_file, "r", encoding="utf-8") as vf:
        return vf.read().strip()

version = read_version()
version_py = os.path.join("python", "qumeas", "_version.py")
with open(version_py, "w", encoding="utf-8") as vp:
    vp.write(f"__version__ = '{version}'\n")


# Read the long description from README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Define the setup configuration
setup(
    name="qumeas",
    version=version,
    author="Oinam Romesh Meitei",
    author_email="oinam.meitei@fau.de",
    description="A high-performance, multi-threaded, quantum computing library for Pauli measurements.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/oimeitei/qumeas",
    packages=find_packages(where='python'),
    package_dir={'': 'python'},
    cmake_install_dir='qumeas',
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: C++",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: Apache Software License",  
        "Topic :: Software Development :: Libraries",
        "Topic :: Scientific/Engineering :: Physics",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy",
        "scipy"
    ],
    extras_require={
        "qiskit": ["qiskit", "qiskit_nature", "qiskit_aer"],
    },
)
