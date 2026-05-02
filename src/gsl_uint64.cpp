#include <gsl/gsl_rng.h>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>

// Use compile-time BENCH_N for iterations
#ifndef BENCH_N
#define BENCH_N 1000000000ULL
#endif

static const unsigned long long N = (unsigned long long)BENCH_N;

int main() {
    gsl_rng *r = gsl_rng_alloc(gsl_rng_mt19937);
    gsl_rng_set(r, 1234);
    const unsigned long long report_interval = (N >= 10) ? (N / 10) : 1;
    for (unsigned long long i = 0; i < N; ++i) {
        volatile uint32_t x = gsl_rng_get(r);
        (void)x;
        if ((i % report_interval) == 0) {
            std::fprintf(stderr, "gsl_c_uint: Progress: %llu/%llu\n", (unsigned long long)i, (unsigned long long)N);
            std::fflush(stderr);
        }
    }
    gsl_rng_free(r);
    std::fprintf(stderr, "gsl_c_uint: Progress: %llu/%llu (100%%)\n", (unsigned long long)N, (unsigned long long)N);
    return 0;
}
