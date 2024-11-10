#include <iostream>
#include "qumeas/expectation_exact.h"



// <state|operator|state>
complex<double> compute_expectation_mul(const SparseMatrixXcd &operator_,
                                        const Eigen::VectorXcd &state) {
    return state.adjoint() * operator_ * state;
}

// 1-body cumulant
double compute_expectation_cumu1_exact(int Nqubit, const Eigen::VectorXcd &state,
				       const int idxlist[1],
				       const int pauli_string[1]){
  
  // Same as expectation value
  complex<double> Ea = block_2_expect(Nqubit, state, idxlist, pauli_string, 1);
  
  return Ea.real();
}

// 2-body cumulant
double compute_expectation_cumu2_exact(int Nqubit, const Eigen::VectorXcd &state,
				       const int idxlist[2],
				       const int pauli_string[2]) {
  
  // Compute expectation for each blocks
  complex<double> Eab = block_2_expect(Nqubit, state, idxlist, pauli_string, 2);
  complex<double> Ea = block_2_expect(Nqubit, state, idxlist[0], pauli_string[0]);
  complex<double> Eb = block_2_expect(Nqubit, state, idxlist[1], pauli_string[1]);
    
  complex<double> expectation = Eab - Ea * Eb;
  
  return expectation.real();
}

// 3-body cumulant
double compute_expectation_cumu3_exact(int Nqubit, const Eigen::VectorXcd &state,
				       const int idxlist[3],
				       const int pauli_string[3]) {
  
  // Compute expectation for each blocks
  complex<double> E_abc  = block_2_expect(Nqubit, state, idxlist, pauli_string, 3); // Full 3-qubit expectation    
  complex<double> E_ab   = block_2_expect(Nqubit, state, idxlist[0], idxlist[1], pauli_string[0], pauli_string[1]);
  complex<double> E_c    = block_2_expect(Nqubit, state, idxlist[2], pauli_string[2]);
  complex<double> E_ac   = block_2_expect(Nqubit, state, idxlist[0], idxlist[2], pauli_string[0], pauli_string[2]);
  complex<double> E_b    = block_2_expect(Nqubit, state, idxlist[1], pauli_string[1]);
  complex<double> E_bc   = block_2_expect(Nqubit, state, idxlist[1], idxlist[2], pauli_string[1], pauli_string[2]);
  complex<double> E_a    = block_2_expect(Nqubit, state, idxlist[0], pauli_string[0]);
  
  complex<double> E_ac_b = E_ac * E_b;
  complex<double> E_ab_c = E_ab * E_c;
  complex<double> E_bc_a = E_bc * E_a;
  complex<double> E_a_b_c = E_a * E_b * E_c;
  
  complex<double> E_result = E_abc - E_ab_c - E_ac_b - E_bc_a + 2.0 * E_a_b_c;
    
  return E_result.real();
}

// 4-body cumulant
double compute_expectation_cumu4_exact(int Nqubit, const Eigen::VectorXcd &state,
				       const int idxlist[4],
				       const int pauli_string[4]) {
  
  // Compute expectation for each blocks
  complex<double> Eabcd = block_2_expect(Nqubit, state, idxlist, pauli_string, 4); // Full 4-qubit expectation
  complex<double> Eabc  = block_2_expect(Nqubit, state, idxlist[0], idxlist[1], idxlist[2], pauli_string[0],
					 pauli_string[1], pauli_string[2]);
  complex<double> Ebcd  = block_2_expect(Nqubit, state, idxlist[1], idxlist[2], idxlist[3], pauli_string[1],
					 pauli_string[2], pauli_string[3]);
  complex<double> Eacd  = block_2_expect(Nqubit, state, idxlist[0], idxlist[2], idxlist[3], pauli_string[0],
					 pauli_string[2], pauli_string[3]);
  complex<double> Eabd  = block_2_expect(Nqubit, state, idxlist[0], idxlist[1], idxlist[3], pauli_string[0],
					 pauli_string[1], pauli_string[3]);
  
  complex<double> Eab   = block_2_expect(Nqubit, state, idxlist[0], idxlist[1], pauli_string[0], pauli_string[1]);
  complex<double> Eac   = block_2_expect(Nqubit, state, idxlist[0], idxlist[2], pauli_string[0], pauli_string[2]);
  complex<double> Ead   = block_2_expect(Nqubit, state, idxlist[0], idxlist[3], pauli_string[0], pauli_string[3]);
  complex<double> Ebc   = block_2_expect(Nqubit, state, idxlist[1], idxlist[2], pauli_string[1], pauli_string[2]);
  complex<double> Ebd   = block_2_expect(Nqubit, state, idxlist[1], idxlist[3], pauli_string[1], pauli_string[3]);
  complex<double> Ecd   = block_2_expect(Nqubit, state, idxlist[2], idxlist[3], pauli_string[2], pauli_string[3]);
  
  complex<double> Ea    = block_2_expect(Nqubit, state, idxlist[0], pauli_string[0]);
  complex<double> Eb    = block_2_expect(Nqubit, state, idxlist[1], pauli_string[1]);
  complex<double> Ec    = block_2_expect(Nqubit, state, idxlist[2], pauli_string[2]);
  complex<double> Ed    = block_2_expect(Nqubit, state, idxlist[3], pauli_string[3]);
  
  complex<double> expectation = Eabcd
    - (Ea * Ebcd + Eb * Eacd + Ec * Eabd + Ed * Eabc)
    - (Eab * Ecd + Ead * Ebc + Eac * Ebd)
    + 2.0 * (Ea * Eb * Ecd + Ea * Ebc * Ed + Ea * Ec * Ebd + Eab * Ec * Ed + Eb * Eac * Ed + Eb * Ec * Ead)
    - 6.0 * Ea * Eb * Ec * Ed;
  
  return expectation.real();
}
