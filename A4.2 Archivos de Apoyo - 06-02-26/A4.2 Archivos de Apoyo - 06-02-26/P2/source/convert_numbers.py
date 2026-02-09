#!/usr/bin/env python3
"""
compute_statistics.py

Reads numbers from a file and computes descriptive statistics using
basic algorithms (no numpy/statistics). Prints results and writes them
to StatisticsResults.txt. Invalid lines are reported but execution continues.
"""

from __future__ import annotations

import sys
import time
from typing import List, Optional, Tuple


RESULTS_FILENAME = "StatisticsResults.txt"


def parse_numbers(file_path: str) -> Tuple[List[float], List[str]]:
    """Read numbers from a file and return (valid_numbers, error_messages)."""
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
                    errors.append(
                        f"Line {line_no}: invalid number '{text}' (skipped)"
                    )
    except FileNotFoundError:
        errors.append(f"File not found: {file_path}")

    return numbers, errors


def selection_sort(values: List[float]) -> List[float]:
    """Return a sorted copy using the selection sort algorithm."""
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
    total = 0.0
    for v in values:
        total += v
    return total / len(values)


def median(values: List[float]) -> float:
    """Compute median value."""
    sorted_vals = selection_sort(values)
    n = len(sorted_vals)
    mid = n // 2

    if n % 2:
        return sorted_vals[mid]

    return (sorted_vals[mid - 1] + sorted_vals[mid]) / 2


def mode(values: List[float]) -> Optional[float]:
    """Return most frequent value. None if no repetition."""
    freq: dict[float, int] = {}

    for v in values:
        freq[v] = freq.get(v, 0) + 1

    best_value: Optional[float] = None
    best_count = 0

    for v, c in freq.items():
        if c > best_count or (
            c == best_count and best_value is not None and v < best_value
        ):
            best_count = c
            best_value = v

    if best_count <= 1:
        return None

    return best_value


def variance_population(values: List[float]) -> float:
    """Compute population variance."""
    mu = mean(values)
    total = 0.0

    for v in values:
        diff = v - mu
        total += diff * diff

    return total / len(values)


def stddev_population(values: List[float]) -> float:
    """Compute population standard deviation."""
    return variance_population(values) ** 0.5


def format_results(values: List[float], elapsed: float) -> str:
    """Format statistics results as printable text."""
    mu = mean(values)
    med = median(values)
    mod = mode(values)
    var = variance_population(values)
    std = stddev_population(values)

    mod_text = "N/A" if mod is None else f"{mod:.6f}"

    return (
        f"Count: {len(values)}\n"
        f"Mean: {mu:.6f}\n"
        f"Median: {med:.6f}\n"
        f"Mode: {mod_text}\n"
        f"Standard Deviation (Population): {std:.6f}\n"
        f"Variance (Population): {var:.6f}\n"
        f"Time Elapsed (s): {elapsed:.6f}\n"
    )


def write_results(text: str) -> None:
    """Write results to output file."""
    with open(RESULTS_FILENAME, "w", encoding="utf-8") as file:
        file.write(text)


def main(argv: List[str]) -> int:
    """Program entry point."""
    if len(argv) != 2:
        print("Usage: python compute_statistics.py fileWithData.txt")
        return 2

    start = time.perf_counter()
    numbers, errors = parse_numbers(argv[1])

    for err in errors:
        print(f"ERROR: {err}")

    if not numbers:
        return 1

    elapsed = time.perf_counter() - start
    out = format_results(numbers, elapsed)

    print(out, end="")
    write_results(out)

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
