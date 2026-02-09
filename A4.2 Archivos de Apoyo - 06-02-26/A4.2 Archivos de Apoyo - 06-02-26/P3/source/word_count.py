#!/usr/bin/env python3
"""
word_count.py

Reads a file with words separated by spaces/newlines, counts distinct words and
their frequencies using basic algorithms (no Counter), prints results and writes
them to WordCountResults.txt.
"""

from __future__ import annotations

import sys
import time
from typing import Dict, List, Tuple


RESULTS_FILENAME = "WordCountResults.txt"


def normalize_token(token: str) -> str:
    """Normalize a token: lowercase and remove punctuation."""
    token = token.strip().lower()

    while token and token[0] in ".,;:!?\"'()[]{}<>":
        token = token[1:]
    while token and token[-1] in ".,;:!?\"'()[]{}<>":
        token = token[:-1]

    return token


def parse_words(file_path: str) -> Tuple[List[str], List[str]]:
    """Read file and return (normalized_words, error_messages)."""
    words: List[str] = []
    errors: List[str] = []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            for raw in file:
                text = raw.strip()
                if not text:
                    continue

                for part in text.split():
                    word = normalize_token(part)
                    if word:
                        words.append(word)

    except FileNotFoundError:
        errors.append(f"File not found: {file_path}")
    except OSError as exc:
        errors.append(f"Could not read file '{file_path}': {exc}")

    return words, errors


def count_words(words: List[str]) -> Tuple[Dict[str, int], Dict[str, int]]:
    """Count word frequencies and track first appearance index."""
    counts: Dict[str, int] = {}
    first_index: Dict[str, int] = {}

    for idx, word in enumerate(words):
        if word not in counts:
            counts[word] = 1
            first_index[word] = idx
        else:
            counts[word] += 1

    return counts, first_index


def sort_words(counts: Dict[str, int], first_index: Dict[str, int]) -> List[str]:
    """Sort by frequency (desc) then first appearance (asc)."""
    items = list(counts.keys())
    items.sort(key=lambda w: (-counts[w], first_index[w]))
    return items


def write_results(lines: List[str]) -> None:
    """Write output lines to results file."""
    with open(RESULTS_FILENAME, "w", encoding="utf-8") as file:
        for line in lines:
            file.write(line + "\n")


def main(argv: List[str]) -> int:
    """Program entry point."""
    if len(argv) != 2:
        print("Usage: python word_count.py fileWithData.txt")
        return 2

    file_path = argv[1]
    start = time.perf_counter()

    words, errors = parse_words(file_path)

    for err in errors:
        print(f"ERROR: {err}")

    lines: List[str] = []
    base_name = file_path.split("/")[-1]
    lines.append(f"Row Labels\tCount of {base_name}")

    if words:
        counts, first_idx = count_words(words)
        ordered = sort_words(counts, first_idx)

        for word in ordered:
            lines.append(f"{word}\t{counts[word]}")
    else:
        lines.append("(no words found)\t0")

    elapsed = time.perf_counter() - start
    lines.append(f"Time Elapsed (s):\t{elapsed:.6f}")

    for line in lines:
        print(line)

    write_results(lines)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
