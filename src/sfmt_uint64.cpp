#include <cstdio>
#include <cstdint>
#include "SFMT.h"
#include <cstdlib>
#include <cstring>

// Use compile-time BENCH_N for iterations
#ifndef BENCH_N
#define BENCH_N 1000000000ULL
#endif

static const unsigned long long N = (unsigned long long)BENCH_N;

int main() {
    sfmt_t sfmt;
    sfmt_init_gen_rand(&sfmt, 1234);
    const unsigned long long report_interval = (N >= 10) ? (N / 10) : 1;
    for (unsigned long long i = 0; i < N; ++i) {
        volatile uint64_t r = sfmt_genrand_uint64(&sfmt);
        (void)r;
        if ((i % report_interval) == 0) {
            std::fprintf(stderr, "sfmt_uint64: Progress: %llu/%llu\n", (unsigned long long)i, (unsigned long long)N);
            std::fflush(stderr);
        }
    }
    std::fprintf(stderr, "sfmt_uint64: Progress: %llu/%llu (100%%)\n", (unsigned long long)N, (unsigned long long)N);
    return 0;
}


