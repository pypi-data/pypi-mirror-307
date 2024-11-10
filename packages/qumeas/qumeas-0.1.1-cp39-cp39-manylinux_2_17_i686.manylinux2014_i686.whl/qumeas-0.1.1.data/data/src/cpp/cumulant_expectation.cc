#include "qumeas/cumulant_expectation.h"

typedef Matrix<complex<double>, Dynamic, 1> VectorXcd;

// each of the compute_expectation_cumu* has OpenMp parallel implementation
double run_block_bits(const std::vector<std::vector<int>>& bitlists,
		      const std::vector<std::vector<int>>& outbits,
		      const int* blocks,
		      const int* tstring,
		      size_t len_blocks)
{
    double e_ = 0.0;

    if (len_blocks == 1) {
        e_ = compute_expectation_cumu1(bitlists, outbits, blocks, tstring);
    }
    else if (len_blocks == 2) {
        e_ = compute_expectation_cumu2(bitlists, outbits, blocks, tstring);
    }
    else if (len_blocks == 3) {
        e_ = compute_expectation_cumu3(bitlists, outbits, blocks, tstring);
    }
    else if (len_blocks == 4) {
        e_ = compute_expectation_cumu4(bitlists, outbits, blocks, tstring);
    }
    else {
        throw std::runtime_error("blocks len > 4 in run_cumulant_block");
    }

    return e_;
}

double run_block_state(int Nqubit,
		       const Eigen::VectorXcd &state,
		       const int* blocks,
		       const int* tstring,
		       size_t len_blocks)
{
  double e_ = 0.0;
  
  if (len_blocks == 1) {
    e_ = compute_expectation_cumu1_exact(Nqubit, state, blocks, tstring);
  }
  else if (len_blocks == 2) {
    e_ = compute_expectation_cumu2_exact(Nqubit, state, blocks, tstring);
  }
  else if (len_blocks == 3) {
    e_ = compute_expectation_cumu3_exact(Nqubit, state, blocks, tstring);
  }
  else if (len_blocks == 4) {
    e_ = compute_expectation_cumu4_exact(Nqubit, state, blocks, tstring);
  }
  else {
    throw std::runtime_error("blocks len > 4 in run_cumulant_block");
  }
  
  return e_;
}		       

std::unordered_map<std::string, double> partition_expectation_bits(const std::vector<std::vector<int>>& bitlists,
								   const std::vector<std::vector<int>>& outbits,
								   const std::vector<std::tuple<std::string, std::vector<int>,
								   std::vector<int>>>& clist)
{
  std::unordered_map<std::string, double> cdict;
  std::vector<std::future<double>> futures;
  
  // Use async tasks for each entry in clist
  for (const auto& [tkey, blocks, tstring] : clist) {
    size_t len_blocks = blocks.size();
    
    futures.emplace_back(std::async(std::launch::async, run_block_bits, std::cref(bitlists),
				    std::cref(outbits), blocks.data(), tstring.data(), len_blocks));
  }
  
  // Collect results and store in cdict
  for (size_t i = 0; i < clist.size(); ++i) {
    const auto& [tkey, blocks, tstring] = clist[i];
    // Waits for each future and retrieves the result
    cdict[tkey] = futures[i].get(); 
  }
  
  return cdict;
}

std::unordered_map<std::string, double> partition_expectation_state(int Nqubit,
								    const Eigen::VectorXcd &state,
								    const std::vector<std::tuple<std::string, std::vector<int>, std::vector<int>>>& clist)
{
  std::unordered_map<std::string, double> cdict;
  std::vector<std::future<double>> futures;
  
  for (const auto& [tkey, blocks, tstring] : clist) {
    size_t len_blocks = blocks.size();
    
    futures.emplace_back(std::async(std::launch::async, run_block_state,
				    Nqubit, std::cref(state),
				    blocks.data(), tstring.data(), len_blocks));
  }
  
  for (size_t i = 0; i < clist.size(); ++i) {
    const auto& [tkey, blocks, tstring] = clist[i];
    cdict[tkey] = futures[i].get();
  }
  
  return cdict;
}
