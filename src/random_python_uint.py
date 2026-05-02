#!/usr/bin/env python3
import random
import sys
import os

if len(sys.argv) > 1:
    N = int(sys.argv[1])
else:
    N = int(os.environ.get('BENCH_N', '1000000000'))

random.seed(1234)
report_interval = N // 10 if N >= 10 else 1
for i in range(N):
    x = random.getrandbits(32)
    if (i % report_interval) == 0:
        sys.stderr.write(f"random_python_uint: Progress: {i}/{N} ({(i*100)//N}%)\n")
        sys.stderr.flush()
sys.stderr.write(f"random_python_uint: Progress: {N}/{N} (100%)\n")
sys.stderr.flush()
