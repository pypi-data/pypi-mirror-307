#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/eigen.h>
#include "qumeas/expectation_basis.h"
#include "qumeas/cumulant_expectation.h"
#include "qumeas/partition.h"

namespace py = pybind11;

// Wrapper function for partitioning TODO: move to src/cpp
std::vector<std::vector<std::vector<std::vector<int>>>> generate_partition_non_crossing_wrapper(
    const std::vector<std::vector<int>>& list_of_lists,
    int max_size,
    int num_threads
) {
    std::vector<std::vector<std::vector<std::vector<int>>>> all_partitions;
    
    generate_partition_non_crossing(list_of_lists, max_size, num_threads, all_partitions);
    return all_partitions;
}

PYBIND11_MODULE(libmeas, m) {
  m.doc() = "Non-crossing partitions generator module";
  
  m.def("generate_partition_non_crossing", &generate_partition_non_crossing_wrapper,
	py::arg("list_of_lists"), py::arg("max_size"), py::arg("num_threads"),
	"Generate non-crossing partitions for a list of Pauli strings.");
  
  m.def("partition_expectation_bits", &partition_expectation_bits,
	py::arg("bitlists"), py::arg("outbits"), py::arg("clist"),
	"Compute expectation value using cumulant expansion given classical bits");
  
  m.def("partition_expectation_state", &partition_expectation_state,
	py::arg("Nqubit"), py::arg("state"), py::arg("clist"),
	"Compute expectation value using cumulant expansion given a state vector");
  
  m.def("compute_expectations_basis", &compute_expectations_basis,
	py::arg("bitlists"), py::arg("outbits"), 
	py::arg("pauli_list"), py::arg("nqubit"),
	"Compute expectation value from random measurements");
}
