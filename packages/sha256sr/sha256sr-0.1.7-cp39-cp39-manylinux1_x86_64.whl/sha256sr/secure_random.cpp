#include "secure_random.h"

#include <cmath>
#include <iostream>

void SecureRandom::update_state(std::vector<uint8_t>& state,
                                const std::vector<uint8_t>& output) {
  int last = 1;
  int v = 0;
  int8_t t = 0;
  bool zeroFlag = false;
  // state(n + 1) = (state(n) + output(n) + 1) % 2^{8* digest_out_size};
  for (size_t i = 0; i < state.size(); i++) {
    // Add two bytes
    v = static_cast<int>(static_cast<int8_t>(state[i])) +
        static_cast<int>(static_cast<int8_t>(output[i])) + last;
    // Result is lower 8 bits
    t = static_cast<int8_t>(v);
    // Store result. Check for state collision.
    zeroFlag = zeroFlag || (static_cast<int8_t>(state[i]) != t);
    state[i] = t;
    // High 8 bits are carry. Store for next iteration.
    last = v >> 8;
  }

  // Make sure at least one bit changes!
  if (!zeroFlag) {
    state[0]++;
  }

  return;
}

void SecureRandom::engine_next_bytes(std::vector<uint8_t>& result) {
  int index = 0;
  int todo = 0;
  int r = this->remCount_;
  int result_size = result.size();
  std::vector<uint8_t> output;

  // Use remainder from last time
  if (r > 0) {
    // How many bytes?
    todo = result_size - index;
    if (todo >= this->digestOutSize_ - r) {
      todo = this->digestOutSize_ - r;
    }
    // Copy the bytes, zero the buffer
    for (int i = 0; i < todo; i++) {
      result[i] = this->remainder_[r];
      //   output[r] = 0;
      r = r + 1;
    }
    this->remCount_ += todo;
    index += todo;
  }

  // If we need more bytes, make them.
  while (index < result_size) {
    output = this->state_;
    sha256(output.data(), output.size(), state_.data(), SHA256_HASH_SIZE);
    update_state(this->state_, output);
    //  How many bytes?
    todo = result.size() - index;
    if (todo > this->digestOutSize_) {
      todo = this->digestOutSize_;
    }
    // Copy the bytes, zero the buffer
    for (int i = 0; i < todo; i++) {
      result[index] = output[i];
      index = index + 1;
    }
    // std::cout << "index = " << index << std::endl;
    this->remCount_ += todo;
  }
  // Store remainder for next time
  this->remainder_ = output;
  this->remCount_ = this->remCount_ % this->digestOutSize_;

  return;
}

double SecureRandom::next_float64_wo_lock() {
  std::vector<uint8_t> b(8, 0);
  next_bytes(b);
  int high, low;
  high = (b[0] << 24) | (b[1] << 16) | (b[2] << 8) | b[3];
  high = static_cast<unsigned int>(high) >> 6;
  low = (b[4] << 24) | (b[5] << 16) | (b[6] << 8) | b[7];
  low = static_cast<unsigned int>(low) >> 5;
  auto res = static_cast<long long>(high) << 27;
  res += static_cast<long long>(low);

  return static_cast<double>(res) * DoubleUnit;
}

double SecureRandom::next_float64() {
  std::unique_lock<std::mutex> lock(mutex_);
  auto res = next_float64_wo_lock();
  lock.unlock();

  return res;
}

double SecureRandom::next_gaussian() {
  double res;
  std::unique_lock<std::mutex> lock(mutex_);
  if (this->haveNextNextGaussian_) {
    this->haveNextNextGaussian_ = false;
    res = this->nextNextGaussian_;
  } else {
    double v1, v2, s;
    while (true) {
      v1 = next_float64_wo_lock();
      v1 = 2 * v1 - 1;  // between -1 and 1
      v2 = next_float64_wo_lock();
      v2 = 2 * v2 - 1;  // between -1 and 1
      s = v1 * v1 + v2 * v2;
      if (s > 0.0 && s < 1.0) {
        break;
      } else {
        // std::cout << "illegal" << std::endl;
      }
    }
    auto multiplier = sqrt(-2 * log(s) / s);
    res = v1 * multiplier;
    this->nextNextGaussian_ = v2 * multiplier;
    this->haveNextNextGaussian_ = true;
  }

  lock.unlock();
  return res;
}