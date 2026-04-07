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
    parser.add_argument(
        "--title",
        default="Porownanie wzglednej predkosci dla generacji 1e9 liczb",
        help="Chart title",
    )
    parser.add_argument(
        "--ylabel",
        default="Wzgledny czas / najszybszy",
        help="Y axis label",
    )
    parser.add_argument(
        "--mode",
        choices=["relative", "seconds"],
        default="relative",
        help=(
            "Chart value mode: 'relative' plots elapsed_seconds normalized "
            "to the fastest run (fastest=1), 'seconds' plots raw elapsed_seconds."
        ),
    )
    parser.add_argument(
        "--figsize",
        default="12,5",
        help="Figure size in inches as width,height (default: 12,5)",
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


def normalize_labels(labels: list[str]) -> list[str]:
    return [label.replace("_", " ").replace(".py", "") for label in labels]


def main() -> None:
    args = parse_args()
    csv_path = Path(args.csv_path)
    output_path = Path(args.output)

    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    timestamp, rows = read_results(csv_path)
    if not rows:
        raise ValueError("No benchmark rows found in CSV file.")

    labels = normalize_labels([row["program"] for row in rows])
    elapsed = [float(row["elapsed_seconds"]) for row in rows]

    if args.mode == "relative":
        fastest = min(elapsed)
        values = [value / fastest for value in elapsed]
    else:
        values = elapsed

    width_str, height_str = args.figsize.split(",", maxsplit=1)
    fig_width = float(width_str.strip())
    fig_height = float(height_str.strip())

    plt.figure(figsize=(fig_width, fig_height))
    plt.bar(labels, values, color="#5a9b1f", edgecolor="#4c841a", width=0.62)
    plt.title(args.title)
    plt.ylabel(args.ylabel)
    plt.grid(axis="y", linestyle="-", linewidth=0.7, alpha=0.35)
    plt.gca().set_axisbelow(True)
    plt.xticks(rotation=45, ha="right")

    if timestamp:
        plt.figtext(0.99, 0.01, timestamp, ha="right", va="bottom", fontsize=9, alpha=0.7)

    plt.tight_layout()
    plt.savefig(output_path, dpi=160)
    print(f"Chart saved to {output_path}")


if __name__ == "__main__":
    main()