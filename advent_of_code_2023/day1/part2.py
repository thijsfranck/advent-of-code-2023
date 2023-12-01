"""Advent of Code 2023 Day 1 Part 2."""

import logging
from collections.abc import Generator
from pathlib import Path


class InsufficientDigitsError(Exception):
    """Raised when the input does not contain enough digits."""


DIGIT_MAP = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}

REVERSE_MAP = {
    "eno": "1",
    "owt": "2",
    "eerht": "3",
    "ruof": "4",
    "evif": "5",
    "xis": "6",
    "neves": "7",
    "thgie": "8",
    "enin": "9",
}


def read_lines(path: Path) -> Generator[str, None, None]:
    """Read the input file line by line."""
    with Path.open(path) as f:
        while line := f.readline():
            yield line.rstrip()


def find_digit(line: str, dictionary: dict[str, str]) -> str | None:
    """Find the first digit in a line. The given dictionary lists digits as words."""
    sequence = ""

    for char in line:
        if char.isdigit():
            return char

        sequence += char

        if digit := dictionary.get(sequence):
            return digit

        while not any(word.startswith(sequence) for word in dictionary):
            sequence = sequence[1:]

    return None


def find_calibration_value(line: str) -> int:
    """Find the calibration value for the given line."""
    first = find_digit(line, DIGIT_MAP)
    last = find_digit(line[::-1], REVERSE_MAP)

    if not first or not last:
        raise InsufficientDigitsError

    return int(first + last)


def sum_calibration_values(path: Path) -> int:
    """Sum all calibration values in the input file."""
    return sum(find_calibration_value(line) for line in read_lines(path))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    solution = sum_calibration_values(Path(__file__).parent / "input/input")
    logging.info(solution)
