#ifndef COMPUTE_EXPECTATION_CUMU4_H
#define COMPUTE_EXPECTATION_CUMU4_H

#include <vector>

double compute_expectation_cumu4(
    const std::vector<std::vector<int>>& bitlists,
    const std::vector<std::vector<int>>& outbits,
    const int idxlist[4],
    const int pstring[4]);

#endif 
