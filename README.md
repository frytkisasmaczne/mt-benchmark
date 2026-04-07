# mt-benchmark
Mersenne Twister c++(std,GSL,SFMT) and Python benchmark

# Usage
1. Clone the repo with SFMT submodule:
```
git clone --recurse-submodules https://github.com/frytkisasmaczne/mt-benchmark
```
2. Install dependencies:
```
pip3 install matplotlib
```
Install libGSL with dev headers from your system package manager, e.g.:
```
apt install libgsl-dev
pacman -S gsl
```
3. Build c++ and run the benchmarks:
```
make clean run
```
