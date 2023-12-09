"""Advent of Code 2023 Day 9 Part 1."""

import logging
from collections.abc import Generator, Iterable
from dataclasses import dataclass
from functools import cached_property, reduce
from itertools import pairwise
from pathlib import Path


@dataclass(frozen=True)
class OasisReading:
    """A reading from the OASIS."""

    reading: list[int]

    @cached_property
    def next_reading(self) -> int:
        """Extrapolate the next reading."""
        layers = []
        current = self.reading

        while any(current):
            layers.append(current)
            current = [b - a for a, b in pairwise(current)]

        return reduce(lambda a, b: a + b, (layer[-1] for layer in reversed(layers)))


def parse_oasis(stream: Iterable[str]) -> Generator[OasisReading, None, None]:
    """Parse a stream of numbers as OASIS readings."""
    reading: list[int] = []
    current_number = ""

    for char in stream:
        if char.isdigit() or char == "-":
            current_number += char
            continue

        if char == " ":
            reading.append(int(current_number))
            current_number = ""
            continue

        if char == "\n":
            reading.append(int(current_number))
            current_number = ""
            yield OasisReading(reading)
            reading = []


def read_char_stream(path: Path) -> Generator[str, None, None]:
    """Read a file as a stream of characters."""
    with Path.open(path) as f:
        while char := f.read(1):
            yield char


def calculate_solution(path: Path) -> int:
    """Calculate the solution."""
    stream = read_char_stream(path)
    return sum(oasis.next_reading for oasis in parse_oasis(stream))


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    solution = calculate_solution(Path(__file__).parent / "input/input")
    logging.info(solution)
