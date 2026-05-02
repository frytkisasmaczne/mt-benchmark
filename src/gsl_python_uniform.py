#!/usr/bin/env python3
import sys
import os
from pygsl import rng

if len(sys.argv) > 1:
    N = int(sys.argv[1])
else:
    N = int(os.environ.get('BENCH_N', '1000000000'))

r = rng.mt19937()
r.set(1234)
report_interval = N//10 if N>=10 else 1
for i in range(N):
    x = r.uniform()
    if i % report_interval == 0:
        sys.stderr.write(f"gsl_python_uniform: Progress: {i}/{N}\n")
        sys.stderr.flush()
sys.stderr.write(f"gsl_python_uniform: Progress: {N}/{N} (100%)\n")
sys.stderr.flush()
