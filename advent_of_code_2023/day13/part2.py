"""Advent of Code 2023 Day 13 Part 2."""

import logging
from collections.abc import Generator
from itertools import pairwise
from pathlib import Path


def read_patterns(path: Path) -> Generator[list[str], None, None]:
    """Read a stream of patterns from a file."""
    with Path.open(path) as f:
        current_pattern = []
        while line := f.readline():
            if line == "\n":
                yield current_pattern
                current_pattern = []
            else:
                current_pattern.append(line.strip())

        if len(current_pattern):
            yield current_pattern


def transpose(pattern: list[str]) -> list[str]:
    """Transpose a pattern."""
    return ["".join(row) for row in zip(*pattern, strict=True)]


def hamming_distance(a: str, b: str) -> int:
    """Calculate the hamming distance between two strings."""
    return sum(1 for x, y in zip(a, b, strict=True) if x != y)


def find_reflection(pattern: list[str], allowed_smudges: int = 1) -> int:
    """Check a pattern for reflections."""
    for index, (a, b) in enumerate(pairwise(pattern)):
        smudges_remaining = allowed_smudges - hamming_distance(a, b)

        if smudges_remaining < 0:
            continue

        for offset in range(1, min(index + 1, len(pattern) - index - 1)):
            smudges_remaining -= hamming_distance(
                pattern[index + 1 + offset], pattern[index - offset],
            )

            if smudges_remaining < 0:
                break
        else:
            if smudges_remaining == 0:
                return index + 1

    return 0


def find_reflections(pattern: list[str]) -> int:
    """Check a pattern for horizontal and vertical reflections."""
    if horizontal := find_reflection(pattern):
        return horizontal * 100

    if vertical := find_reflection(transpose(pattern)):
        return vertical

    return 0


def calculate_solution(path: Path) -> int:
    """Calculate the solution."""
    return sum(find_reflections(pattern) for pattern in read_patterns(path))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    solution = calculate_solution(Path(__file__).parent / "input/input")
    logging.info(solution)
