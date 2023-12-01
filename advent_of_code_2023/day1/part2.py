"""Advent of Code 2023 Day 1 Part 1."""

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


def read_lines(path: Path) -> Generator[str, None, None]:
    """Read the input file line by line."""
    with Path.open(path) as f:
        while line := f.readline():
            yield line


def find_fist_digit(line: str) -> str | None:
    """Find the first digit in a line."""
    seen = ""
    for char in line:
        if char.isdigit():
            return char
        seen += char
        for word, digit in DIGIT_MAP.items():
            if seen.endswith(word):
                return digit
    return None


def find_last_digit(line: str) -> str | None:
    """Find the last digit in a line."""
    seen = ""
    for char in reversed(line):
        if char.isdigit():
            return char
        seen = char + seen
        for word, digit in DIGIT_MAP.items():
            if seen.startswith(word):
                return digit
    return None


def get_calibration_value(line: str) -> int:
    """Get the calibration value for the given line."""
    first_digit = find_fist_digit(line)
    last_digit = find_last_digit(line)

    if first_digit is None or last_digit is None:
        raise InsufficientDigitsError

    return int(first_digit + last_digit)


def sum_calibration_values(path: Path) -> int:
    """Sum all calibration values in the input file."""
    return sum(get_calibration_value(line) for line in read_lines(path))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    solution = sum_calibration_values(Path(__file__).parent / "input/input")
    logging.info(solution)
