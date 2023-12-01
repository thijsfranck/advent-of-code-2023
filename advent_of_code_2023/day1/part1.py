"""Advent of Code 2023 Day 1 Part 1."""

import logging
from collections.abc import Generator
from pathlib import Path


class InsufficientDigitsError(Exception):
    """Raised when the input does not contain enough digits."""


def read_lines(path: Path) -> Generator[str, None, None]:
    """Read the input file line by line."""
    with Path.open(path) as f:
        while line := f.readline():
            yield line


def find_calibration_value(line: str) -> int:
    """Find the calibration value for the given line."""
    digits = [char for char in line if char.isdigit()]

    if len(digits) == 0:
        raise InsufficientDigitsError

    return int(digits[0] + digits[-1])


def sum_calibration_values(path: Path) -> int:
    """Sum all calibration values in the input file."""
    return sum(find_calibration_value(line) for line in read_lines(path))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    solution = sum_calibration_values(Path(__file__).parent / "input/input")
    logging.info(solution)
