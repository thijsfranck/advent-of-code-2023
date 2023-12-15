"""Advent of Code 2023 Day 14 Part 2."""

import logging
from collections.abc import Callable
from copy import deepcopy
from functools import reduce
from itertools import pairwise
from pathlib import Path


def transpose(platform: list[list[str]]) -> list[list[str]]:
    """Transpose a platform."""
    return [list(row) for row in zip(*platform, strict=True)]


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


def shift_south(platform: list[list[str]]) -> list[list[str]]:
    """Shift rounded rocks on the platform south."""
    return list(reversed(shift_north(list(reversed(platform)))))


def shift_west(platform: list[list[str]]) -> list[list[str]]:
    """Shift rounded rocks on the platform east."""
    return transpose(shift_north(transpose(platform)))


def shift_east(platform: list[list[str]]) -> list[list[str]]:
    """Shift rounded rocks on the platform west."""
    return transpose(shift_south(transpose(platform)))


def shift_platform(
    shift: Callable[[list[list[str]]], list[list[str]]], platform: list[list[str]],
) -> list[list[str]]:
    """Shift rounded rocks on the platform until they cannot shift any further."""
    while platform != (new_platform := shift(platform)):
        platform = new_platform
    return platform


def calculate_solution(path: Path, ticks: int) -> int:
    """Calculate the solution."""
    i = 0
    operations = [shift_north, shift_west, shift_south, shift_east]
    new_platform = []
    platform = read_platform(path)

    def tick(platform: list[list[str]]) -> list[list[str]]:
        return reduce(lambda acc, op: shift_platform(op, acc), operations, platform)

    while i < ticks and platform != (new_platform := tick(platform)):
        platform = new_platform
        i += 1

    if i < ticks - 1:
        logging.debug("Repeating pattern found after %d ticks", i)

    return sum(row.count("O") * (index + 1) for index, row in enumerate(reversed(new_platform)))


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    solution = calculate_solution(Path(__file__).parent / "input/input", 1000000000)
    logging.info(solution)
