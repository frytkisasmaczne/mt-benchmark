#!/usr/bin/env python3
"""Generate a benchmark bar chart from results.csv."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import matplotlib.pyplot as plt


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a bar chart from benchmark CSV results."
    )
    parser.add_argument(
        "csv_path",
        nargs="?",
        default="results.csv",
        help="Path to CSV file (default: results.csv)",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="benchmark_chart.png",
        help="Output image path (default: benchmark_chart.png)",
    )

    return parser.parse_args()


def read_results(csv_path: Path) -> tuple[str | None, list[dict[str, str]]]:
    with csv_path.open("r", encoding="utf-8", newline="") as f:
        first_line = f.readline().strip()
        second_line = f.readline().strip()

        rows: list[dict[str, str]] = []

        if second_line.lower() == "program,n,elapsed_seconds":
            timestamp = first_line or None
            reader = csv.DictReader(f, fieldnames=["program", "N", "elapsed_seconds"])
            rows = [row for row in reader if row.get("program")]
        else:
            f.seek(0)
            timestamp = None
            reader = csv.DictReader(f)
            rows = [row for row in reader if row.get("program")]

    return timestamp, rows


def main() -> None:
    args = parse_args()
    csv_path = Path(args.csv_path)
    output_path = Path(args.output)

    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    timestamp, rows = read_results(csv_path)
    if not rows:
        raise ValueError("No benchmark rows found in CSV file.")

    labels = [row["program"] for row in rows]
    elapsed = [float(row["elapsed_seconds"]) for row in rows]

    fastest = min(elapsed)
    values = [value / fastest for value in elapsed]

    plt.figure(figsize=(12, 5))
    bars = plt.bar(labels, values, color="#5a9b1f", edgecolor="#4c841a", width=0.62)
    plt.title("Porownanie wzglednej predkosci dla generacji 1e9 liczb")
    plt.ylabel("Czas, wielokrotnosc najszybszego (sekundy)")
    plt.grid(axis="y", linestyle="-", linewidth=0.7, alpha=0.35)
    plt.gca().set_axisbelow(True)
    plt.xticks(rotation=45, ha="right")

    # Add elapsed-seconds labels above each bar (show actual seconds measured)
    max_val = max(values) if values else 0.0
    offset = max_val * 0.01 if max_val > 0 else 0.01
    for rect, secs, val in zip(bars, elapsed, values):
        height = rect.get_height()
        plt.text(
            rect.get_x() + rect.get_width() / 2,
            height + offset,
            f"{val:.2f} ({float(secs):.1f}s)",
            ha="center",
            va="bottom",
            fontsize=9,
        )

    if timestamp:
        plt.figtext(0.99, 0.01, timestamp, ha="right", va="bottom", fontsize=9, alpha=0.7)

    plt.tight_layout()
    plt.savefig(output_path, dpi=160)
    print(f"Chart saved to {output_path}")


if __name__ == "__main__":
    main()