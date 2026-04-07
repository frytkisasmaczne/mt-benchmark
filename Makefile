.PHONY: all run bench clean

N ?= 1000000000

SRCDIR := src
BINDIR := build
CC := g++
CFLAGS := -std=c++11 -O3 -DBENCH_N=$(N) -DSFMT_MEXP=19937
SFMT_DIR := SFMT
SFMT_C := $(SFMT_DIR)/SFMT.c
SFMT_INC := -I$(SFMT_DIR)

SRCS := $(wildcard $(SRCDIR)/*.cpp)
PROGS := $(patsubst $(SRCDIR)/%.cpp,$(BINDIR)/%,$(SRCS))

all: $(PROGS)

$(BINDIR)/%: $(SRCDIR)/%.cpp | $(BINDIR)
	@echo "Building $@"
	$(CC) $(CFLAGS) $< $(SFMT_C) $(SFMT_INC) -lgsl -lgslcblas -o $@

$(BINDIR):
	@mkdir -p $(BINDIR)

run: all
	@echo "Running benchmarks with N=$(N)"
	BENCH_N=$(N) ./run.sh
	python3 plot_results.py

clean:
	rm -f $(PROGS) results.csv run.log
