#!/usr/bin/env bash
set -euo pipefail

# Read BENCH_N from environment (Makefile sets it) or fallback to argument/env
N=${BENCH_N:-${1:-1000000000}}

RESULTS_FILE="results.csv"
# Write timestamp on its own line, then CSV header
echo "$(date +%Y-%m-%d_%H-%M-%S)" > "$RESULTS_FILE"
echo "program,N,elapsed_seconds" >> "$RESULTS_FILE"

cmds=()

while IFS= read -r -d '' file; do
  cmds+=("${file#./}")
done < <(find build -maxdepth 1 -type f ! -name '*.*' ! -name 'Makefile' -print0)

while IFS= read -r -d '' file; do
  cmds+=("${file#src/}")
done < <(find src -maxdepth 1 -type f -name '*.py' -print0)

mapfile -t cmds < <(printf '%s\n' "${cmds[@]}" | sort -u)

echo "==============================="
echo "Mersenne Twister Benchmark Start"
echo "==============================="
echo

for c in "${cmds[@]}"; do
  echo "Running $c (N=$N) ..."
  if [[ "$c" == *.py ]]; then
    start=$(date +%s.%N)
    BENCH_N="$N" python "src/$c"
    end=$(date +%s.%N)
  else
    start=$(date +%s.%N)
    ./$c
    end=$(date +%s.%N)
  fi
  elapsed=$(awk "BEGIN{printf \"%.6f\", $end - $start}")
  printf "Elapsed Time (s): %s\n" "$elapsed"
  echo
  printf "%s,%s,%.6f\n" "$c" "$N" "$elapsed" >> "$RESULTS_FILE"
done

echo "==============================="
echo "Benchmarking complete!"
echo "Results: $RESULTS_FILE"
echo "==============================="
