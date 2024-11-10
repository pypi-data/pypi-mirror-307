#pragma once
#include <mutex>
#include <vector>

#include "sha256.h"

class SecureRandom {
 public:
  SecureRandom(const std::vector<uint8_t>& seed) : seed_(seed) {
    remCount_ = 0;
    nextNextGaussian_ = 0.0;
    haveNextNextGaussian_ = false;
    digestOutSize_ = SHA256_HASH_SIZE;

    std::unique_lock<std::mutex> lock(mutex_);
    state_.resize(SHA256_HASH_SIZE);
    sha256(seed_.data(), seed_.size(), state_.data(), SHA256_HASH_SIZE);
    lock.unlock();
  }

  double next_float64();

  /** nextGaussian: Returns the next pseudorandom, Gaussian ("normally")
   * distributed double value with mean 0.0 and standard deviation 1.0 from this
   * random number generator's sequence. This uses the polar method of G. E. P.
   * Box, M. E. Muller, and G. Marsaglia, as described by Donald E. Knuth in The
   * Art of Computer Programming, Volume 3: Seminumerical Algorithms,
   * section 3.4.1, subsection C, algorithm P. Note that it generates two
   * independent values at the cost of only one call to StrictMath.log and one
   * call to StrictMath.sqrt.
   */
  double next_gaussian();

 private:
  void engine_next_bytes(std::vector<uint8_t>& result);

  inline void next_bytes(std::vector<uint8_t>& result) {
    engine_next_bytes(result);
  }

  void update_state(std::vector<uint8_t>& state,
                    const std::vector<uint8_t>& output);

  double next_float64_wo_lock();

  std::vector<uint8_t> seed_;
  std::vector<uint8_t> state_;
  std::vector<uint8_t> remainder_;
  int remCount_;
  int digestOutSize_;
  double nextNextGaussian_;
  bool haveNextNextGaussian_;
  std::mutex mutex_;
  static constexpr double DoubleUnit = 1.0 / (1L << 53);
};