"""Advent of Code 2023 Day 0 Part 2."""

import logging
from collections.abc import Generator
from pathlib import Path


def read_char_stream(path: Path) -> Generator[str, None, None]:
    """Read a file as a stream of characters."""
    with Path.open(path) as f:
        while char := f.read(1):
            yield char


def calculate_solution(path: Path) -> int:
    """Calculate the solution."""
    return len([char for char in read_char_stream(path) if char == "\n"])


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    solution = calculate_solution(Path(__file__).parent / "input/input")
    logging.info(solution)
