#include "qumeas/expectation_cumu_4b.h"
#include <omp.h>

// expectation from 4-body cumulant
double compute_expectation_cumu4(
    const std::vector<std::vector<int>>& bitlists,
    const std::vector<std::vector<int>>& outbits,
    const int idxlist[4],
    const int pstring[4])
{
    double Eabcd = 0.0;
    double Eabc = 0.0, Ebcd = 0.0, Eacd = 0.0, Eabd = 0.0;
    double Eab = 0.0, Eac = 0.0, Ead = 0.0, Ebc = 0.0, Ebd = 0.0, Ecd = 0.0;
    double Ea = 0.0, Eb = 0.0, Ec = 0.0, Ed = 0.0;
    double expectation = 0.0, matchn = 0.0;

    const int outlen = static_cast<int>(outbits.size());
    const int p1_idx = idxlist[0];
    const int p2_idx = idxlist[1];
    const int p3_idx = idxlist[2];
    const int p4_idx = idxlist[3];

    const int p1_val = pstring[0];
    const int p2_val = pstring[1];
    const int p3_val = pstring[2];
    const int p4_val = pstring[3];

    #pragma omp parallel for reduction(+:Eabcd, Eabc, Ebcd, Eacd, Eabd, Eab, Eac, Ead, Ebc, Ebd, Ecd, Ea, Eb, Ec, Ed, matchn)
    for (int bdx = 0; bdx < outlen; bdx++) {
        if (p1_val != bitlists[bdx][p1_idx] ||
            p2_val != bitlists[bdx][p2_idx] ||
            p3_val != bitlists[bdx][p3_idx] ||
            p4_val != bitlists[bdx][p4_idx]) {
            continue;
        }

        const double oa = outbits[bdx][p1_idx];
        const double ob = outbits[bdx][p2_idx];
        const double oc = outbits[bdx][p3_idx];
        const double od = outbits[bdx][p4_idx];

        Eabcd += oa * ob * oc * od;

        Eabc += oa * ob * oc;
        Ebcd += ob * oc * od;
        Eacd += oa * oc * od;
        Eabd += oa * ob * od;

        Eab += oa * ob;
        Eac += oa * oc;
        Ead += oa * od;
        Ebc += ob * oc;
        Ebd += ob * od;
        Ecd += oc * od;

        Ea += oa;
        Eb += ob;
        Ec += oc;
        Ed += od;

        matchn += 1.0;
    }

    if (matchn != 0.0) {
        const double factm = 1.0 / matchn;
        Eabcd *= factm;
        Eabc *= factm;
        Ebcd *= factm;
        Eacd *= factm;
        Eabd *= factm;
        Eab *= factm;
        Eac *= factm;
        Ead *= factm;
        Ebc *= factm;
        Ebd *= factm;
        Ecd *= factm;
        Ea *= factm;
        Eb *= factm;
        Ec *= factm;
        Ed *= factm;

        expectation = Eabcd
            - (Ea * Ebcd + Eb * Eacd + Ec * Eabd + Ed * Eabc)
            - (Eab * Ecd + Ead * Ebc + Eac * Ebd)
            + 2.0 * (Ea * Eb * Ecd + Ea * Ebc * Ed + Ea * Ec * Ebd + Eab * Ec * Ed + Eb * Eac * Ed + Eb * Ec * Ead)
            - 6.0 * Ea * Eb * Ec * Ed;
    }

    return expectation;
}
