#ifndef EXPECTATION_EXACT_H
#define EXPECTATION_EXACT_H

#include <complex>
#include <vector>
#include <string>
#include <Eigen/Sparse>
#include "qumeas/quantum_utils.h"

using Eigen::SparseMatrix;
using Eigen::Matrix;
using std::complex;
using std::vector;
using std::string;

typedef SparseMatrix<complex<double>> SparseMatrixXcd;
// typedef Matrix<complex<double>, Eigen::Dynamic, 1> VectorXcd;

complex<double> compute_expectation_mul(const SparseMatrixXcd &operator_, const Eigen::VectorXcd &state);

// Overloaded functions
// Convert to operator (Eigen SparseMatrixXcd) for expectation computation using C-style arrays
// Dynamic
inline complex<double> block_2_expect(int Nqubit, const Eigen::VectorXcd &state,
				      const int* id_list, const int* pauli_string, size_t size) {
    SparseMatrixXcd operator_ = block_2_operator(Nqubit, id_list, pauli_string, size);
    return compute_expectation_mul(operator_, state);
}

// 1-element
inline complex<double> block_2_expect(int Nqubit, const Eigen::VectorXcd &state, int idx, int pauli) {
    int id_list[1] = {idx};
    int pauli_string[1] = {pauli};
    return block_2_expect(Nqubit, state, id_list, pauli_string, 1);
}

// 2-element
inline complex<double> block_2_expect(int Nqubit, const Eigen::VectorXcd &state, 
                                      int idx1, int idx2, 
                                      int pauli1, int pauli2) {
    int id_list[2] = {idx1, idx2};
    int pauli_string[2] = {pauli1, pauli2};
    return block_2_expect(Nqubit, state, id_list, pauli_string, 2);
}

// 3-element
inline complex<double> block_2_expect(int Nqubit, const Eigen::VectorXcd &state, 
                                      int idx1, int idx2, int idx3, 
                                      int pauli1, int pauli2, int pauli3) {
    int id_list[3] = {idx1, idx2, idx3};
    int pauli_string[3] = {pauli1, pauli2, pauli3};
    return block_2_expect(Nqubit, state, id_list, pauli_string, 3);
}

double compute_expectation_cumu1_exact(int Nqubit, const Eigen::VectorXcd &state, const int idxlist[1], const int pauli_string[1]);

double compute_expectation_cumu2_exact(int Nqubit, const Eigen::VectorXcd &state, const int idxlist[2], const int pauli_string[2]);

double compute_expectation_cumu3_exact(int Nqubit, const Eigen::VectorXcd &state, const int idxlist[3], const int pauli_string[3]);

double compute_expectation_cumu4_exact(int Nqubit, const Eigen::VectorXcd &state, const int idxlist[4], const int pauli_string[4]);

#endif 
