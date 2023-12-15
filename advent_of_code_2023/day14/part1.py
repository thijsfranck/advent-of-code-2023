"""Advent of Code 2023 Day 14 Part 1."""

import logging
from copy import deepcopy
from itertools import pairwise
from pathlib import Path


def read_platform(path: Path) -> list[list[str]]:
    """Read a file as a list of strings."""
    with Path.open(path) as f:
        return [list(line) for line in f.read().splitlines()]


def shift_north(platform: list[list[str]]) -> list[list[str]]:
    """Shift rounded rocks on the platform north."""
    result = deepcopy(platform)
    for a, b in pairwise(result):
        for index, char in enumerate(b):
            if char == "O" and a[index] == ".":
                a[index] = "O"
                b[index] = "."
    return result


def calculate_solution(path: Path) -> int:
    """Calculate the solution."""
    platform = read_platform(path)

    while platform != (new_platform := shift_north(platform)):
        platform = new_platform

    return sum(row.count("O") * (index + 1) for index, row in enumerate(reversed(platform)))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    solution = calculate_solution(Path(__file__).parent / "input/input")
    logging.info(solution)
