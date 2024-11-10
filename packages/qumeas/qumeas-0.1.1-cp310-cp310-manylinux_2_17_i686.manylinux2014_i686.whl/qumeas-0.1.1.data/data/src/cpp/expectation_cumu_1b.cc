#include "qumeas/expectation_cumu_1b.h"
#include <omp.h>

// expectation from 1-body cumulant
double compute_expectation_cumu1(
    const std::vector<std::vector<int>>& bitlists,
    const std::vector<std::vector<int>>& outbits,
    const int idxlist[1],
    const int pstring[1]) {
    
    double Ea = 0.0;
    double count_match = 0.0;
    const int outlen = static_cast<int>(outbits.size());
    const int p1_idx = idxlist[0];
    const int p1_val = pstring[0];

    #pragma omp parallel for reduction(+:Ea, count_match)
    for (int bdx = 0; bdx < outlen; bdx++) {
        if (p1_val != bitlists[bdx][p1_idx]) {
            continue;
        }
        const double outbit1 = outbits[bdx][p1_idx];
        Ea += outbit1;
        count_match += 1.0;
    }

    if (count_match != 0.0) {
        Ea /= count_match;
    }
    return Ea;
}
