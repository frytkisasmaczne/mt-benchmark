#include <random>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>

#ifndef BENCH_N
#define BENCH_N 1000000000ULL
#endif

static const unsigned long long N = (unsigned long long)BENCH_N;

int main() {
    std::mt19937 mt(1234);

    const unsigned long long report_interval = (N >= 10) ? (N / 10) : 1;
    for (unsigned long long i = 0; i < N; ++i) {
        volatile uint32_t x = mt();
        (void)x;
        if ((i % report_interval) == 0) {
            std::fprintf(stderr, "cpp11_uint32: Progress: %llu/%llu\n", (unsigned long long)i, (unsigned long long)N);
            std::fflush(stderr);
        }
    }
    std::fprintf(stderr, "cpp11_uint32: Progress: %llu/%llu (100%%)\n", (unsigned long long)N, (unsigned long long)N);
    return 0;
}
