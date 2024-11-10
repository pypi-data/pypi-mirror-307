#ifndef CUMULANT_EXPECTATION_H
#define CUMULANT_EXPECTATION_H

#include <vector>
#include <string>
#include <complex>
#include <unordered_map>
#include <tuple>
#include <future>
#include <stdexcept>
#include <Eigen/Sparse>
#include <Eigen/Dense>
#include "qumeas/expectation_exact.h"
#include "qumeas/expectation_cumu_1b.h"
#include "qumeas/expectation_cumu_2b.h"
#include "qumeas/expectation_cumu_3b.h"
#include "qumeas/expectation_cumu_4b.h"

using Eigen::Matrix;
using std::complex;

// typedef Matrix<complex<double>, Eigen::Dynamic, 1> VectorXcd;

double run_block_bits(const std::vector<std::vector<int>>& bitlists,
                      const std::vector<std::vector<int>>& outbits,
                      const int* blocks,
		      const int* tstring,
		      size_t len_blocks);
  
double run_block_state(int Nqubit,
		       const Eigen::VectorXcd &state,
		       const int* blocks,
		       const int* tstring,
		       size_t len_blocks);

std::unordered_map<string, double> partition_expectation_bits(
    const std::vector<std::vector<int>>& bitlists,
    const std::vector<std::vector<int>>& outbits,
    const std::vector<std::tuple<std::string, std::vector<int>, std::vector<int>>>& clist);

std::unordered_map<string, double> partition_expectation_state(
    int Nqubit,
    const Eigen::VectorXcd &state,
    const std::vector<std::tuple<std::string, std::vector<int>, std::vector<int>>>& clist);
    

#endif 
