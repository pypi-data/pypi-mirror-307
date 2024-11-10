#ifndef COMPUTE_EXPECTATION_BASIS_H
#define COMPUTE_EXPECTATION_BASIS_H

#include <vector>

double compute_expectation_pauli_from_bits(const std::vector<std::vector<int>> &bitlists,
					   const std::vector<std::vector<int>> &outbits,
					   const std::vector<int> &pstring,
					   int nqubit);

std::vector<double> compute_expectations_basis(const std::vector<std::vector<int>> &bitlists,
					       const std::vector<std::vector<int>> &outbits,
					       const std::vector<std::vector<int>> &pauli_list,
					       const int nqubit);

#endif 
