"""Advent of Code 2023 Day 6 Part 1."""

import logging
from collections.abc import Generator, Iterable
from functools import reduce
from pathlib import Path


def read_lines(path: Path) -> Generator[str, None, None]:
    """Read a file as a stream of lines."""
    with Path.open(path) as f:
        while line := f.readline():
            yield line


def read_numbers(line: str) -> list[int]:
    """Read all numbers from a line."""
    numbers: list[int] = []
    current_number = ""

    for char in line:
        if char.isdigit():
            current_number += char
        elif current_number:
            numbers.append(int(current_number))
            current_number = ""

    return numbers


def read_time_distance(lines: Iterable[str]) -> Generator[tuple[int, ...], None, None]:
    """Read the time and corresponding record distance from a stream of lines."""
    yield from zip(*map(read_numbers, lines), strict=True)


def calculate_winning_strategies(time_distance: tuple[int, ...]) -> int:
    """
    Calculate the number of winning strategies.

    Distance travelled must be greater than the record distance in the same time.
    Accelleration is linear to the time spent charging. One unit of charge is one unit of time.
    """
    time, record_distance = time_distance

    winning_strategies = 0

    for charge_time in range(time + 1):
        distance_travelled = charge_time * (time - charge_time)
        if distance_travelled > record_distance:
            winning_strategies += 1

    return winning_strategies


def calculate_solution(path: Path) -> int:
    """Calculate the solution."""
    time_distance = read_time_distance(read_lines(path))

    return reduce(
        lambda solution, winning_strategies: solution * winning_strategies,
        map(calculate_winning_strategies, time_distance),
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    solution = calculate_solution(Path(__file__).parent / "input/input")
    logging.info(solution)
