"""Advent of Code 2023 Day 2 Part 1."""

import logging
from collections import defaultdict
from collections.abc import Generator
from pathlib import Path
from typing import TypedDict


class CubeSet(TypedDict):
    """A cube set."""

    id: int
    config: dict[str, int]


CONFIGURATION = {"red": 12, "green": 13, "blue": 14}


def read_lines(path: Path) -> Generator[str, None, None]:
    """Read the input file line by line."""
    with Path.open(path) as f:
        while line := f.readline():
            yield line.rstrip()


def parse_cube_set(line: str) -> CubeSet:
    """Parse a line of the input file into a cube set."""
    game, config_str = line.split(": ")

    config = defaultdict(int)

    cube_sets = config_str.split("; ")

    for cube_set in cube_sets:
        cubes = cube_set.split(", ")

        for cube in cubes:
            number_str, color = cube.split(" ")
            number = int(number_str)

            if number > config[color]:
                config[color] = number

    return {"id": int(game.split(" ")[1]), "config": config}


def is_valid(cube_set: CubeSet) -> bool:
    """Determine whether the given cube set is valid."""
    return all(
        cube_count <= CONFIGURATION[color] for color, cube_count in cube_set["config"].items()
    )


def find_valid_cube_sets(path: Path) -> int:
    """Find the sum of ids for all valid cube sets."""
    return sum(
        cube_set["id"] for cube_set in map(parse_cube_set, read_lines(path)) if is_valid(cube_set)
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    solution = find_valid_cube_sets(Path(__file__).parent / "input/input")
    logging.info(solution)
