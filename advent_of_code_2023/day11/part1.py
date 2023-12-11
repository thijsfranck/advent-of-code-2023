"""Advent of Code 2023 Day 11 Part 1."""

import logging
from itertools import combinations
from pathlib import Path


def read_galaxies(path: Path) -> set[tuple[int, int]]:
    """Read a set of galaxies from a file."""
    with Path.open(path) as f:
        lines = [line.strip() for line in f.readlines()]

    galaxies: set[tuple[int, int]] = set()

    if not any(lines):
        return galaxies

    empty_columns = [i for i in range(len(lines[0])) if all(line[i] == "." for line in lines)]
    y_offset = 0

    for y, line in enumerate(lines):
        expanded_line = line

        local_galaxies: set[tuple[int, int]] = set()

        for x, char in enumerate(expanded_line):
            if char == "#":
                x_offset = len([i for i in empty_columns if i < x])
                local_galaxies.add((x + x_offset, y + y_offset))

        if len(local_galaxies) == 0:
            y_offset += 1

        galaxies.update(local_galaxies)

    return galaxies


def manhattan_distance(a: tuple[int, int], b: tuple[int, int]) -> int:
    """Calculate the Manhattan distance between two points."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def calculate_solution(path: Path) -> int:
    """Calculate the solution."""
    galaxies = read_galaxies(path)
    return sum(manhattan_distance(a, b) for a, b in combinations(galaxies, 2))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    solution = calculate_solution(Path(__file__).parent / "input/input")
    logging.info(solution)
