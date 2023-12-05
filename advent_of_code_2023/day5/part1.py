"""Advent of Code 2023 Day 5 Part 1."""

import contextlib
import logging
from collections.abc import Generator, Iterable
from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class Range:
    """A range of location numbers."""

    source: int
    destination: int
    length: int

    def __contains__(self, value: int) -> bool:
        return self.source <= value < self.source + self.length

    def __getitem__(self, index: int) -> int:
        if index not in self:
            msg = f"Index {index} is not in range {self}"
            raise IndexError(msg)
        return self.destination - self.source + index

    def __str__(self) -> str:
        return f"{self.source}..{self.source + self.length}"


@dataclass
class SeedsReader:
    """Read the seeds from the almanac."""

    current_seed: str = ""
    seeds: set[int] = field(default_factory=set)

    def __call__(self, char: str) -> None:
        """Read a character."""
        if char.isdigit():
            self.current_seed += char
            return

        if char in {"\n", " "} and self.current_seed:
            self.seeds.add(int(self.current_seed))
            self.current_seed = ""
            return

    def reset(self) -> None:
        """Reset the reader."""
        self.current_seed = ""
        self.seeds.clear()


@dataclass
class MapReader:
    """Read a map from the almanac."""

    ranges: list[Range] = field(default_factory=list)
    current_range: str = ""

    def __call__(self, char: str) -> None:
        """Read a character."""
        if char == "\n" and self.current_range:
            destination, source, length = self.current_range.split(" ")
            self.ranges.append(Range(int(source), int(destination), int(length)))
            self.current_range = ""
            return

        if char != "\n":
            self.current_range += char

    def reset(self) -> None:
        """Reset the reader."""
        self.ranges.clear()
        self.current_range = ""


@dataclass
class MapKeyReader:
    """Read a map key from the almanac."""

    current_key: str = ""

    def __call__(self, char: str) -> None:
        """Read a character."""
        if char.isalpha():
            self.current_key += char

    def reset(self) -> None:
        """Reset the reader."""
        self.current_key = ""


@dataclass
class Parser:
    """Parser for the input data."""

    seeds_reader: SeedsReader = field(default_factory=SeedsReader, init=False)
    map_reader: MapReader = field(default_factory=MapReader, init=False)
    map_key_reader: MapKeyReader = field(default_factory=MapKeyReader, init=False)

    def __call__(self, stream: Iterable[str]) -> tuple[set[int], dict[str, list[Range]]]:
        """Iterate over the stream."""
        self.seeds_reader.reset()
        self.map_reader.reset()
        self.map_key_reader.reset()

        current_reader = self.seeds_reader

        maps: dict[str, list[Range]] = {}

        for line in stream:
            for char in line:
                current_reader(char)

            match current_reader:
                case SeedsReader():
                    if line == "\n":
                        current_reader = self.map_key_reader

                case MapKeyReader():
                    if line.endswith(":\n"):
                        current_reader = self.map_reader

                case MapReader():
                    if line == "\n":
                        maps[self.map_key_reader.current_key] = self.map_reader.ranges.copy()
                        current_reader = self.map_key_reader
                        self.map_key_reader.reset()
                        self.map_reader.reset()

        return self.seeds_reader.seeds, maps


def read_lines(path: Path) -> Generator[str, None, None]:
    """Read a file as a stream of lines."""
    with Path.open(path) as f:
        while line := f.readline():
            yield line


def calculate_solution(path: Path) -> int:
    """Calculate the solution."""
    parser = Parser()
    seeds, maps = parser(read_lines(path))

    destinations = set()

    for seed in seeds:
        source = seed

        for map_ranges in maps.values():
            try:
                source = min(r[source] for r in map_ranges if source in r)
            except ValueError:
                # Keep the current source if it is not in any range
                contextlib.suppress(ValueError)

        destinations.add(source)

    return min(destinations)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    solution = calculate_solution(Path(__file__).parent / "input/input")
    logging.info(solution)
