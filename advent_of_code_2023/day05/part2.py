"""Advent of Code 2023 Day 5 Part 2."""

import logging
from dataclasses import dataclass
from pathlib import Path

from advent_of_code_2023 import Interval


@dataclass
class AlmanacEntry:
    """An entry in the almanac."""

    source: Interval
    destination: Interval


@dataclass
class Almanac:
    """An almanac."""

    entries: list[list[AlmanacEntry]]
    seeds: list[Interval]

    @classmethod
    def from_path(cls, path: Path) -> "Almanac":
        """Read an almanac from a file."""
        seeds: list[Interval] = []
        maps: list[list[AlmanacEntry]] = []
        current_map: list[AlmanacEntry] = []

        with path.open() as f:
            while line := f.readline():
                line = line.strip()
                if "seeds" in line:
                    numbers = list(map(int, line.split(": ")[1].split()))
                    seeds = [
                        Interval(numbers[i], numbers[i] + numbers[i + 1])
                        for i in range(0, len(numbers), 2)
                    ]
                elif "map" in line:
                    current_map = []
                elif line:
                    destination, source, length = map(int, line.split())
                    entry = AlmanacEntry(
                        source=Interval(source, source + length),
                        destination=Interval(destination, destination + length),
                    )
                    current_map.append(entry)
                elif len(current_map):
                    maps.append(current_map)

        maps.append(current_map)

        return cls(entries=maps, seeds=seeds)


def find_min_destination(almanac: Almanac) -> int:
    """Find the minimum destination from the Almanac."""
    current_sources = almanac.seeds

    for step in almanac.entries:
        next_sources = []
        for source in current_sources:
            for entry in step:
                offset = entry.destination.start - entry.source.start
                if overlap := entry.source & source:
                    next_sources.append(Interval(overlap.start + offset, overlap.end + offset))
        current_sources = next_sources

    return min(source.start for source in current_sources)


def calculate_solution(path: Path) -> int:
    """Calculate the solution."""
    almanac = Almanac.from_path(path)

    return find_min_destination(almanac)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    solution = calculate_solution(Path(__file__).parent / "input/test__input")
    logging.info(solution)
