#ifndef COMPUTE_EXPECTATION_CUMU3_H
#define COMPUTE_EXPECTATION_CUMU3_H

#include <vector>

double compute_expectation_cumu3(
    const std::vector<std::vector<int>>& bitlists,
    const std::vector<std::vector<int>>& outbits,
    const int idxlist[3],
    const int pstring[3]);

#endif 
