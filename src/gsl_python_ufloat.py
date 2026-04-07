#!/usr/bin/env python3
import sys
import os
from ctypes import CDLL, c_void_p, c_double, c_ulong
from ctypes.util import find_library

if len(sys.argv) > 1:
    N = int(sys.argv[1])
else:
    N = int(os.environ.get('BENCH_N', '1000000000'))

libname = find_library('gsl')
if not libname:
    sys.stderr.write('ERROR: libgsl not found — this benchmark requires libgsl.\\n')
    sys.stderr.write('Install GSL and ensure it is discoverable by the system loader.\\n')
    sys.exit(2)

lib = CDLL(libname)
rng_type = c_void_p.in_dll(lib, 'gsl_rng_mt19937')
lib.gsl_rng_alloc.argtypes = [c_void_p]
lib.gsl_rng_alloc.restype = c_void_p
lib.gsl_rng_set.argtypes = [c_void_p, c_ulong]
lib.gsl_rng_uniform.argtypes = [c_void_p]
lib.gsl_rng_uniform.restype = c_double

r = lib.gsl_rng_alloc(rng_type)
lib.gsl_rng_set(r, 1234)
report_interval = N//10 if N>=10 else 1
for i in range(N):
    x = lib.gsl_rng_uniform(r)
    if i % report_interval == 0:
        sys.stderr.write(f"gsl_python_ufloat: Progress: {i}/{N}\n")
        sys.stderr.flush()
sys.stderr.write(f"gsl_python_ufloat: Progress: {N}/{N} (100%)\n")
sys.stderr.flush()