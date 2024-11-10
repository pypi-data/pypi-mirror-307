#ifndef _SHA256_H_
#define _SHA256_H_

#ifdef __cplusplus
extern "C" {
#endif  // __cplusplus

#include <stdint.h>
#include <stdio.h>

typedef struct {
  uint64_t length;
  uint32_t state[8];
  uint32_t curlen;
  uint8_t buf[64];
} Sha256Context;

#define SHA256_HASH_SIZE (256 / 8)

typedef struct {
  uint8_t bytes[SHA256_HASH_SIZE];
} SHA256_HASH;

void Sha256Initialise(Sha256Context* Context  // [out]
);

void Sha256Update(Sha256Context* Context,  // [in out]
                  void const* Buffer,      // [in]
                  uint32_t BufferSize      // [in]
);

void Sha256Finalise(Sha256Context* Context,  // [in out]
                    SHA256_HASH* Digest      // [out]
);

void Sha256Calculate(void const* Buffer,   // [in]
                     uint32_t BufferSize,  // [in]
                     SHA256_HASH* Digest   // [in]
);

void* sha256(const void* data, const size_t datalen, void* out,
             const size_t outlen);

#ifdef __cplusplus
}
#endif  // __cplusplus

#endif  // _SHA256_H_