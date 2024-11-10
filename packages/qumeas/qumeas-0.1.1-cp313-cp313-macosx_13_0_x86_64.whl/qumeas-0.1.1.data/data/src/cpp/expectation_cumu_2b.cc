#include "qumeas/expectation_cumu_2b.h"
#include <omp.h>

// expectation from 2-body cumulant
double compute_expectation_cumu2(
    const std::vector<std::vector<int>>& bitlists,
    const std::vector<std::vector<int>>& outbits,
    const int idxlist[2],
    const int pstring[2])
{
    double Eab = 0.0;
    double Ea = 0.0;
    double Eb = 0.0;
    double count_match = 0.0;
    double expectation = 0.0;
    const int outlen = static_cast<int>(outbits.size());
    const int p1_idx = idxlist[0];
    const int p2_idx = idxlist[1];
    const int p1_val = pstring[0];
    const int p2_val = pstring[1];

    #pragma omp parallel for reduction(+:Eab, Ea, Eb, count_match)
    for (int bdx = 0; bdx < outlen; bdx++) {
        if (p1_val != bitlists[bdx][p1_idx] ||
            p2_val != bitlists[bdx][p2_idx]) {
            continue;
        }

        const double outbit1 = outbits[bdx][p1_idx];
        const double outbit2 = outbits[bdx][p2_idx];

        Eab += outbit1 * outbit2;
        Ea += outbit1;
        Eb += outbit2;
        count_match += 1.0;
    }

    if (count_match != 0.0) {
        const double factm = 1.0 / count_match;
        Eab *= factm;
        Ea *= factm;
        Eb *= factm;
        expectation = Eab - Ea * Eb;
    }
    return expectation;
}
