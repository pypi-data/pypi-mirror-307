#ifndef COMPUTE_EXPECTATION_CUMU2_H
#define COMPUTE_EXPECTATION_CUMU2_H

#include <vector>

double compute_expectation_cumu2(
    const std::vector<std::vector<int>>& bitlists,
    const std::vector<std::vector<int>>& outbits,
    const int idxlist[2],
    const int pstring[2]);

#endif 
