#!/usr/bin/env python3
"""
computeStatistics.py

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
    except OSError as exc:
        errors.append(f"Could not read file '{file_path}': {exc}")

    return numbers, errors


def selection_sort(values: List[float]) -> List[float]:
    """Return a sorted copy using selection sort (basic algorithm)."""
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
    total = 0.0
    for v in values:
        total += v
    return total / len(values)


def median(values: List[float]) -> float:
    sorted_vals = selection_sort(values)
    n = len(sorted_vals)
    mid = n // 2
    if n % 2 == 1:
        return sorted_vals[mid]
    return (sorted_vals[mid - 1] + sorted_vals[mid]) / 2.0


def mode(values: List[float]) -> Optional[float]:
    """
    Mode using a basic frequency count.
    If there is no repeated value (all frequencies == 1), return None.
    If multiple modes, return the smallest one (deterministic).
    """
    freq: dict[float, int] = {}
    for v in values:
        freq[v] = freq.get(v, 0) + 1

    best_count = 0
    best_value: Optional[float] = None

    for v, c in freq.items():
        if c > best_count:
            best_count = c
            best_value = v
        elif c == best_count and best_value is not None and v < best_value:
            best_value = v

    if best_count <= 1:
        return None
    return best_value


def variance_population(values: List[float]) -> float:
    mu = mean(values)
    total = 0.0
    for v in values:
        diff = v - mu
        total += diff * diff
    return total / len(values)


def stddev_population(values: List[float]) -> float:
    # sqrt without math library: use exponent 0.5 (simple, still basic).
    return variance_population(values) ** 0.5


def format_results(
    count: int,
    mu: float,
    med: float,
    mod: Optional[float],
    std: float,
    var: float,
    elapsed_sec: float,
) -> str:
    mod_text = "N/A" if mod is None else f"{mod:.6f}"
    return (
        f"Count: {count}\n"
        f"Mean: {mu:.6f}\n"
        f"Median: {med:.6f}\n"
        f"Mode: {mod_text}\n"
        f"Standard Deviation (Population): {std:.6f}\n"
        f"Variance (Population): {var:.6f}\n"
        f"Time Elapsed (s): {elapsed_sec:.6f}\n"
    )


def write_results(text: str) -> None:
    with open(RESULTS_FILENAME, "w", encoding="utf-8") as file:
        file.write(text)


def main(argv: List[str]) -> int:
    if len(argv) != 2:
        print("Usage: python computeStatistics.py fileWithData.txt")
        return 2

    file_path = argv[1]
    start = time.perf_counter()

    numbers, errors = parse_numbers(file_path)
    for err in errors:
        print(f"ERROR: {err}")

    if not numbers:
        elapsed = time.perf_counter() - start
        msg = (
            "No valid numbers to process.\n"
            f"Time Elapsed (s): {elapsed:.6f}\n"
        )
        print(msg, end="")
        write_results(msg)
        return 1

    mu = mean(numbers)
    med = median(numbers)
    mod = mode(numbers)
    var = variance_population(numbers)
    std = stddev_population(numbers)

    elapsed = time.perf_counter() - start
    out = format_results(len(numbers), mu, med, mod, std, var, elapsed)

    print(out, end="")
    write_results(out)
    return 0



if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
