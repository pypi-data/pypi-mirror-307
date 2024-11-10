# quMeas

**quMeas** is a high-performance multi-threaded library for computing expectation values of Pauli strings using randomized measurement techniques and cumulant expansion of Pauli operators (strings). It combines **classical shadow tomography** with **statistical cumulant expansion** to efficiently estimate Pauli expectation values. Designed with a multi-layered parallelization strategy and optimized C++ backend, quMeas scales efficiently on multi-core systems, making it ideal to incorporate in large-scale quantum algorithms such as **VQE** for molecular simulation, **QAOA** for combinatorial optimization, or any other quantum algorithm that requires *expectation value of Pauli operators*, particularly long Pauli strings.

## Features
- **Randomized Measurements**: Implements an efficient classical shadow tomography quantum measurement to estimate expectation values with randomized measurement bases.
- **Cumulant Expansion**: Computes expectation values of Pauli operators from a truncated cumulant average expansion utilizing a non-crossing partitioning of the Pauli operators.
- **High-Performance Architecture**: Built with C++ for performance-critical tasks and exposed to Python via Pybind11, with a robust, multi-threaded layered parallelization strategy.

## Installation

quMeas can be installed from pip

```bash
pip install qumeas
```

Pre-built binary wheels for Linux and MacOS are also available at PyPI. Alternatively, to build the package and install from source,

1. Clone the repository:
	```bash
	git clone --recursive https://github.com/oimeitei/qumeas.git
	```
2. Navigate to the project directory, build wheel and install by running the following:
	```bash
	python -m build --wheel
	pip install dist/qumeas-*.whl	
	```
Check [installation guide](https://qumeas.readthedocs.io/en/latest/installation.html) in the documentation for more low-level installation options.


## Basic Usage

Check out [usage](https://qumeas.readthedocs.io/en/latest/usage.html) in the documentation as well the Python scripts in `/examples` for more details


```bash
from qumeas import PauliContainer, RandomShadow, QCumulant

# Get measurement basis and outcomes(basis, bits) from general quantum computing
# packages. See documentation & examples for more details

myPauli = PauliContainer(Nqubit=N, #Qubits
                 	pauli_list=plist, # list of Pauli strings
		 	pauli_list_coeff=clist) # list of coeffs for plist

# Compute expectation with classical shadow tomography
myRandom = RandomShadow(PauliObj=myPauli)
expectation_random = myRandom.compute_expectation(basis, bits)

# Compute expectation with cumulant expansion
myCumu = QCumulant(PauliObj=myPauli,
		  measure_basis=basis,
		  measure_outcome_bits=bits)
myCumu.generate_partitions(num_threads=4)
expectation_cumulant = myCumu.compute_expectation_bits()
```


## Documentation

Documentation on Python API, `libmeas` which expose C++ functions as well as installation instruction and usage are available at `/docs`. To build the documentation locally, simply navigate to `docs` and build using `make html` or `make latexpdf`.

Latest documentation is available online at [quemb.readthedocs.io](http://qumeas.readthedocs.io/en/stable).
