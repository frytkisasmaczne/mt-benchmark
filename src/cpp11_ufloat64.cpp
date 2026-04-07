#include <random>
#include <cstdio>
#include <cstdlib>
#include <cstring>

#ifndef BENCH_N
#define BENCH_N 1000000000ULL
#endif

static const unsigned long long N = (unsigned long long)BENCH_N;

int main() {
    std::mt19937_64 mt(1234ull);
    std::uniform_real_distribution<double> dist(0.0, 1.0);

    const unsigned long long report_interval = (N >= 10) ? (N / 10) : 1;
    for (unsigned long long i = 0; i < N; ++i) {
        volatile double x = dist(mt);
        (void)x;
        if ((i % report_interval) == 0) {
            std::fprintf(stderr, "cpp11_ufloat64: Progress: %llu/%llu\n", (unsigned long long)i, (unsigned long long)N);
            std::fflush(stderr);
        }
    }
    std::fprintf(stderr, "cpp11_ufloat64: Progress: %llu/%llu (100%%)\n", (unsigned long long)N, (unsigned long long)N);
    return 0;
}