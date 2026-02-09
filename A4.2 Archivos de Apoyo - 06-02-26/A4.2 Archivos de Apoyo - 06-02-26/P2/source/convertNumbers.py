#!/usr/bin/env python3
"""
convertNumbers.py

Reads a file with integers (one per line). For each valid integer, converts it
to binary and hexadecimal using basic algorithms (no bin/hex/format), prints
and writes to ConvertionResults.txt. Handles invalid data and continues.
"""

from __future__ import annotations

import sys
import time
from typing import List, Tuple


RESULTS_FILENAME = "ConvertionResults.txt"
HEX_DIGITS = "0123456789ABCDEF"


def parse_integers(file_path: str) -> Tuple[List[int], List[str]]:
    ints: List[int] = []
    errors: List[str] = []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            for line_no, raw in enumerate(file, start=1):
                text = raw.strip()
                if not text:
                    errors.append(f"Line {line_no}: empty line (skipped)")
                    continue
                try:
                    # allow leading +/-, but no decimals
                    value = int(text)
                    ints.append(value)
                except ValueError:
                    errors.append(f"Line {line_no}: invalid integer '{text}' (skipped)")
    except FileNotFoundError:
        errors.append(f"File not found: {file_path}")
    except OSError as exc:
        errors.append(f"Could not read file '{file_path}': {exc}")

    return ints, errors


def to_base(n: int, base: int) -> str:
    """Convert integer n to string in given base (2..16) using basic algorithm."""
    if base < 2 or base > 16:
        raise ValueError("Base must be between 2 and 16")

    if n == 0:
        return "0"

    sign = ""
    value = n
    if value < 0:
        sign = "-"
        value = -value

    digits: List[str] = []
    while value > 0:
        remainder = value % base
        digits.append(HEX_DIGITS[remainder])
        value //= base

    # reverse digits
    out = ""
    for i in range(len(digits) - 1, -1, -1):
        out += digits[i]

    return sign + out


def write_results(lines: List[str]) -> None:
    with open(RESULTS_FILENAME, "w", encoding="utf-8") as file:
        for line in lines:
            file.write(line + "\n")


def main(argv: List[str]) -> int:
    if len(argv) != 2:
        print("Usage: python convertNumbers.py fileWithData.txt")
        return 2

    file_path = argv[1]
    start = time.perf_counter()

    numbers, errors = parse_integers(file_path)
    for err in errors:
        print(f"ERROR: {err}")

    lines: List[str] = []
    lines.append("ITEM\tDEC\tBIN\tHEX")

    item_no = 1
    for n in numbers:
        b2 = to_base(n, 2)
        b16 = to_base(n, 16)
        line = f"{item_no}\t{n}\t{b2}\t{b16}"
        lines.append(line)
        item_no += 1

    elapsed = time.perf_counter() - start
    lines.append(f"Time Elapsed (s):\t{elapsed:.6f}")

    for line in lines:
        print(line)

    write_results(lines)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

