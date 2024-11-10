#include <vector>
#include <stdexcept>
#include <omp.h>
#include <future>
#include <numeric> 
#include "qumeas/expectation_basis.h"

std::vector<double> compute_expectations_basis(const std::vector<std::vector<int>> &bitlists,
						    const std::vector<std::vector<int>> &outbits,
						    const std::vector<std::vector<int>> &pauli_list,
						    int nqubit) {
  
  std::vector<double> expectations(pauli_list.size(), 0.0);
  std::vector<std::future<double>> futures;
  
  // Lambda function: compute expectation for each element of pauli_list
  auto compute_for_pstring = [&](int idx) {
    return compute_expectation_pauli_from_bits(bitlists, outbits, pauli_list[idx], nqubit);
  };
  
  // Create async tasks
  for (size_t idx = 0; idx < pauli_list.size(); ++idx) {
    futures.push_back(std::async(std::launch::async, compute_for_pstring, idx));
  }
  
  // Gather results from each async call
  for (size_t idx = 0; idx < pauli_list.size(); ++idx) {
    expectations[idx] = futures[idx].get();
  }
  
  return expectations;
}

double compute_expectation_pauli_from_bits(const std::vector<std::vector<int>> &bitlists,
				 const std::vector<std::vector<int>> &outbits,
				 const std::vector<int> &pstring,
				 int nqubit) {
  double expectation = 0.0;
  double count_match = 0.0;
  
  const int outlen = static_cast<int>(outbits.size());
  
  // OpenMP for the outer loop
  #pragma omp parallel for reduction(+:expectation, count_match) schedule(static)
  for (int bdx = 0; bdx < outlen; bdx++) {
    const std::vector<int> &bitlist_row = bitlists[bdx];
    const std::vector<int> &outbit_row = outbits[bdx];

    bool match = true;
    double prod_ = 1.0;
    
    for (int pdx = 0; pdx < nqubit; pdx++) {
      const int p_val = pstring[pdx];
      const int bit_val = bitlist_row[pdx];
      
      // Break for any mismatch
      if (p_val != 0 && p_val != bit_val) {
	match = false;
	break;
      }
      
      // If it match, multiply to prod_
      if (p_val != 0) {
	prod_ *= outbit_row[pdx];
      }
    }
    
    // If all qubits indices match, add to expectation
    if (match) {
      expectation += prod_;
      count_match += 1.0;
    }
  }
  
  // Divide by count_match
  if (count_match != 0.0) {
    expectation /= count_match;
  }
  
  return expectation;
}
