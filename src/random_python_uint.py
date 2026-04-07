#!/usr/bin/env python3
import random
import sys
import os

# Generate N 32-bit unsigned integers using Python's PRNG
# Default to 1_000_000_000 unless overridden by argv[1] or BENCH_N
if len(sys.argv) > 1:
    N = int(sys.argv[1])
else:
    N = int(os.environ.get('BENCH_N', '1000000000'))

random.seed(1234)
report_interval = N // 10 if N >= 10 else 1
for i in range(N):
    x = random.getrandbits(32)
    if (i % report_interval) == 0:
        pct = (i * 100) / N
        sys.stderr.write(f"random_python_uint: Progress: {i}/{N} ({pct:.0f}%)\n")
        sys.stderr.flush()
sys.stderr.write(f"random_python_uint: Progress: {N}/{N} (100%)\n")
sys.stderr.flush()
