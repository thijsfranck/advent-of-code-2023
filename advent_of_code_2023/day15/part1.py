"""Advent of Code 2023 Day 15 Part 1."""

import logging
from collections.abc import Generator, Iterable
from functools import reduce
from pathlib import Path


def read_char_stream(path: Path) -> Generator[str, None, None]:
    """Read a file as a stream of characters."""
    with Path.open(path) as f:
        while char := f.read(1):
            yield char


def parse_initialization_sequences(stream: Iterable[str]) -> Generator[str, None, None]:
    """Parse initialization sequences from a stream of characters."""
    current_sequence = ""

    for char in stream:
        if char in {"\n", ","} and current_sequence:
            yield current_sequence
            current_sequence = ""
            continue

        current_sequence += char


def calculate_hash(initialization_sequence: str) -> int:
    """Calculate the hash of an initialization sequence."""
    return reduce(
        lambda result, char: ((result + ord(char)) * 17) % 256, initialization_sequence, 0,
    )


def calculate_solution(path: Path) -> int:
    """Calculate the solution."""
    stream = read_char_stream(path)

    initialization_sequences = parse_initialization_sequences(stream)

    hashes = map(calculate_hash, initialization_sequences)

    return sum(hashes)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    solution = calculate_solution(Path(__file__).parent / "input/input")
    logging.info(solution)
