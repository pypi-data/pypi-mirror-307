#include "qumeas/quantum_utils.h"
#include <unsupported/Eigen/KroneckerProduct>

// Misc. operations
// Pauli matrices as sparse matrices
SparseMatrixXcd getI() {
    SparseMatrixXcd I(2, 2);
    I.insert(0, 0) = 1.0;
    I.insert(1, 1) = 1.0;
    return I;
}

SparseMatrixXcd getX() {
    SparseMatrixXcd X(2, 2);
    X.insert(0, 1) = 1.0;
    X.insert(1, 0) = 1.0;
    return X;
}

SparseMatrixXcd getY() {
    SparseMatrixXcd Y(2, 2);
    Y.insert(0, 1) = complex<double>(0, -1.0);
    Y.insert(1, 0) = complex<double>(0, 1.0);
    return Y;
}

SparseMatrixXcd getZ() {
    SparseMatrixXcd Z(2, 2);
    Z.insert(0, 0) = 1.0;
    Z.insert(1, 1) = -1.0;
    return Z;
}

// Kronecker product for a list
SparseMatrixXcd kronProductList(const vector<SparseMatrixXcd> &matrices) {
    SparseMatrixXcd result = matrices[0];
    for (size_t i = 1; i < matrices.size(); ++i) {
        SparseMatrixXcd temp = kroneckerProduct(result, matrices[i]).eval();
        result = temp;
    }
    return result;
}

// Get a matrix (eigen SparseMatrixXcd) corresponding to a given Pauli string
SparseMatrixXcd block_2_operator(int Nqubit, const int* id_list, const int* pauli_string, size_t size) {
    std::vector<SparseMatrixXcd> operator_(Nqubit, getI());
    for (size_t idx = 0; idx < size; ++idx) {
        int pos = id_list[idx];
        int pauli_type = pauli_string[idx];
        if (pauli_type == 1) operator_[pos] = getX();
        else if (pauli_type == 2) operator_[pos] = getY();
        else if (pauli_type == 3) operator_[pos] = getZ();
    }
    return kronProductList(operator_);
}
