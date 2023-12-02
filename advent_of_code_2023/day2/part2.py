"""Advent of Code 2023 Day 2 Part 2."""

import logging
from collections import defaultdict
from collections.abc import Generator
from functools import reduce
from pathlib import Path
from typing import TypedDict


class CubeSet(TypedDict):
    """A cube set."""

    id: int
    config: dict[str, int]


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


def calculate_set_power(path: Path) -> int:
    """
    Calculate the sum of the power of all cube sets.

    The power of a cube set is the product of all cube counts.
    """
    return sum(
        reduce(lambda x, y: x * y, cube_set["config"].values())
        for cube_set in map(parse_cube_set, read_lines(path))
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    solution = calculate_set_power(Path(__file__).parent / "input/input")
    logging.info(solution)
