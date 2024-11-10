#include "qumeas/expectation_cumu_3b.h"
#include <omp.h>

// expectation from 3-body cumulant
double compute_expectation_cumu3(
    const std::vector<std::vector<int>>& bitlists,
    const std::vector<std::vector<int>>& outbits,
    const int idxlist[3],
    const int pstring[3])
{
    double Eabc = 0.0;
    double Eab = 0.0, Eac = 0.0, Ebc = 0.0;
    double Ea = 0.0, Eb = 0.0, Ec = 0.0;
    double expectation = 0.0, count_match = 0.0;

    const int outlen = static_cast<int>(outbits.size());
    const int p1_idx = idxlist[0];
    const int p2_idx = idxlist[1];
    const int p3_idx = idxlist[2];
    const int p1_val = pstring[0];
    const int p2_val = pstring[1];
    const int p3_val = pstring[2];

    #pragma omp parallel for reduction(+:Eabc, Eab, Eac, Ebc, Ea, Eb, Ec, count_match)
    for (int bdx = 0; bdx < outlen; bdx++) {
        if (p1_val != bitlists[bdx][p1_idx] ||
            p2_val != bitlists[bdx][p2_idx] ||
            p3_val != bitlists[bdx][p3_idx]) {
            continue;
        }

        const double oa = outbits[bdx][p1_idx];
        const double ob = outbits[bdx][p2_idx];
        const double oc = outbits[bdx][p3_idx];

        Eabc += oa * ob * oc;
        Eab += oa * ob;
        Eac += oa * oc;
        Ebc += ob * oc;
        Ea += oa;
        Eb += ob;
        Ec += oc;
        count_match += 1.0;
    }

    if (count_match != 0.0) {
        const double factm = 1.0 / count_match;
        Eabc *= factm;
        Eab *= factm;
        Eac *= factm;
        Ebc *= factm;
        Ea *= factm;
        Eb *= factm;
        Ec *= factm;
        expectation = Eabc - Eab * Ec - Eac * Eb - Ebc * Ea + 2.0 * Ea * Eb * Ec;
    }

    return expectation;
}
