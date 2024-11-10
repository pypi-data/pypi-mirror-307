#ifndef COMPUTE_EXPECTATION_CUMU1_H
#define COMPUTE_EXPECTATION_CUMU1_H

#include <vector>

double compute_expectation_cumu1(
    const std::vector<std::vector<int>>& bitlists,
    const std::vector<std::vector<int>>& outbits,
    const int idxlist[1],
    const int pstring[1]);

#endif 
