"""Advent of Code 2023 Day 6 Part 2."""

import logging
from collections.abc import Generator, Iterable
from pathlib import Path


def read_lines(path: Path) -> Generator[str, None, None]:
    """Read a file as a stream of lines."""
    with Path.open(path) as f:
        while line := f.readline():
            yield line


def read_number(line: str) -> int:
    """Read all digits from a line as a single number."""
    current_number = ""

    for char in line:
        if char.isdigit():
            current_number += char

    return int(current_number)


def read_time_distance(lines: Iterable[str]) -> tuple[int, int]:
    """Read the time and corresponding record distance from a stream of lines."""
    time, distance = map(read_number, lines)
    return time, distance


def calculate_winning_strategies(time: int, record_distance: int) -> int:
    """
    Calculate the number of winning strategies.

    Distance travelled must be greater than the record distance in the same time.
    Accelleration is linear to the time spent charging. One unit of charge is one unit of time.
    """
    winning_strategies = 0

    for charge_time in range(time + 1):
        distance_travelled = charge_time * (time - charge_time)
        if distance_travelled > record_distance:
            winning_strategies += 1

    return winning_strategies


def calculate_solution(path: Path) -> int:
    """Calculate the solution."""
    time, distance = map(read_number, read_lines(path))

    return calculate_winning_strategies(time, distance)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    solution = calculate_solution(Path(__file__).parent / "input/input")
    logging.info(solution)
