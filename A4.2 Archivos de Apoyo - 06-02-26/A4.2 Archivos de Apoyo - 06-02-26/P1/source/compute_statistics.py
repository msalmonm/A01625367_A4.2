#!/usr/bin/env python3
"""
compute_statistics.py

Reads a file with numbers (one per line), computes descriptive statistics using
basic algorithms (no statistics/numpy), prints results to console and writes
them to StatisticsResults.txt. Handles invalid lines and continues.
"""

from __future__ import annotations

import sys
import time
from typing import List, Optional, Tuple


RESULTS_FILENAME = "StatisticsResults.txt"


def parse_numbers(file_path: str) -> Tuple[List[float], List[str]]:
    """Parse numbers from a text file. Returns (numbers, error_messages)."""
    numbers: List[float] = []
    errors: List[str] = []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            for line_no, raw in enumerate(file, start=1):
                text = raw.strip()
                if not text:
                    errors.append(f"Line {line_no}: empty line (skipped)")
                    continue
                try:
                    numbers.append(float(text))
                except ValueError:
                    errors.append(f"Line {line_no}: invalid number '{text}' (skipped)")
    except FileNotFoundError:
        errors.append(f"File not found: {file_path}")

    return numbers, errors


def selection_sort(values: List[float]) -> List[float]:
    """Return a sorted copy using selection sort."""
    arr = values[:]
    n = len(arr)

    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]

    return arr


def mean(values: List[float]) -> float:
    """Compute arithmetic mean."""
    return sum(values) / len(values)


def median(values: List[float]) -> float:
    """Compute median value."""
    sorted_vals = selection_sort(values)
    n = len(sorted_vals)
    mid = n // 2
    return sorted_vals[mid] if n % 2 else (sorted_vals[mid - 1] + sorted_vals[mid]) / 2


def mode(values: List[float]) -> Optional[float]:
    """Return most frequent value or None if no repeats."""
    freq: dict[float, int] = {}

    for v in values:
        freq[v] = freq.get(v, 0) + 1

    best_count = 0
    best_value: Optional[float] = None

    for v, c in freq.items():
        if c > best_count or (c == best_count and best_value is not None and v < best_value):
            best_count = c
            best_value = v

    return best_value if best_count > 1 else None


def variance_population(values: List[float]) -> float:
    """Compute population variance."""
    mu = mean(values)
    return sum((v - mu) ** 2 for v in values) / len(values)


def stddev_population(values: List[float]) -> float:
    """Compute population standard deviation."""
    return variance_population(values) ** 0.5


def format_results(stats: Tuple[int, float, float, Optional[float], float, float, float]) -> str:
    """Format statistics into printable text."""
    count, mu, med, mod, std, var, elapsed = stats
    mod_text = "N/A" if mod is None else f"{mod:.6f}"

    return (
        f"Count: {count}\n"
        f"Mean: {mu:.6f}\n"
        f"Median: {med:.6f}\n"
        f"Mode: {mod_text}\n"
        f"Standard Deviation (Population): {std:.6f}\n"
        f"Variance (Population): {var:.6f}\n"
        f"Time Elapsed (s): {elapsed:.6f}\n"
    )


def write_results(text: str) -> None:
    """Write output to file."""
    with open(RESULTS_FILENAME, "w", encoding="utf-8") as file:
        file.write(text)


def main(argv: List[str]) -> int:
    """Program entry point."""
    if len(argv) != 2:
        print("Usage: python compute_statistics.py file.txt")
        return 2

    start = time.perf_counter()

    numbers, errors = parse_numbers(argv[1])

    for err in errors:
        print(f"ERROR: {err}")

    if not numbers:
        return 1

    mu = mean(numbers)
    med = median(numbers)
    mod = mode(numbers)
    var = variance_population(numbers)
    std = stddev_population(numbers)
    elapsed = time.perf_counter() - start

    output = format_results((len(numbers), mu, med, mod, std, var, elapsed))

    print(output, end="")
    write_results(output)

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
