#ifndef QUANTUM_UTILS_H
#define QUANTUM_UTILS_H

#include <Eigen/Sparse>
#include <complex>
#include <vector>
#include <string>

using namespace Eigen;
using namespace std;

typedef SparseMatrix<complex<double>> SparseMatrixXcd;

SparseMatrixXcd getI();
SparseMatrixXcd getX();
SparseMatrixXcd getY();
SparseMatrixXcd getZ();

SparseMatrixXcd kronProductList(const vector<SparseMatrixXcd> &matrices);

SparseMatrixXcd block_2_operator(int Nqubit, const int* id_list, const int* pauli_string, size_t size);

#endif 
