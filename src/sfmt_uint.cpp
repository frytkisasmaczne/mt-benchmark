#include <cstdio>
#include <cstdint>
#include "SFMT.h"
#include <cstdlib>
#include <cstring>

static unsigned long long parse_N(int argc, char** argv) {
    if (argc > 1) return std::strtoull(argv[1], nullptr, 10);
    const char* env = std::getenv("BENCH_N");
    if (env) return std::strtoull(env, nullptr, 10);
    // Use compile-time BENCH_N for iterations
    #ifndef BENCH_N
    #define BENCH_N 1000000000ULL
    #endif

    static const unsigned long long N = (unsigned long long)BENCH_N;

}

int main(int argc, char** argv) {
    const unsigned long long N = (unsigned long long)BENCH_N;
    sfmt_t sfmt;
    sfmt_init_gen_rand(&sfmt, 1234);

    const unsigned long long report_interval = (N >= 10) ? (N / 10) : 1;
    for (unsigned long long i = 0; i < N; ++i) {
        volatile uint32_t r = sfmt_genrand_uint32(&sfmt);
        (void)r;
        if ((i % report_interval) == 0) {
            std::fprintf(stderr, "sfmt_uint: Progress: %llu/%llu\n", (unsigned long long)i, (unsigned long long)N);
            std::fflush(stderr);
        }
    }
    std::fprintf(stderr, "sfmt_uint: Progress: %llu/%llu (100%%)\n", (unsigned long long)N, (unsigned long long)N);
    return 0;
}


