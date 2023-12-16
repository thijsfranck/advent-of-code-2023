"""Advent of Code 2023 Day 16 Part 1."""

import logging
from collections import defaultdict, deque
from pathlib import Path
from typing import Literal

Direction = Literal["d", "l", "r", "u"]

REFRACTION_TABLE: dict[str, dict[Direction, list[Direction]]] = {
    "\\": {
        "d": ["r"],
        "l": ["u"],
        "r": ["d"],
        "u": ["l"],
    },
    "/": {
        "d": ["l"],
        "l": ["d"],
        "r": ["u"],
        "u": ["r"],
    },
    "|": {
        "d": ["d"],
        "l": ["d", "u"],
        "r": ["d", "u"],
        "u": ["u"],
    },
    "-": {
        "d": ["l", "r"],
        "l": ["l"],
        "r": ["r"],
        "u": ["l", "r"],
    },
}


def read_contraption(path: Path) -> list[str]:
    """Read a contraption from a file."""
    with Path.open(path) as f:
        return [line.strip() for line in f.readlines() if line.strip()]


def find_energized_tiles(
    contraption: list[str],
    start: tuple[int, int, Direction],
) -> list[tuple[int, int]]:
    """Find all energized tiles in the given contraption."""
    queue: deque[tuple[int, int, Direction]] = deque([start])
    seen: dict[tuple[int, int], set[Direction]] = defaultdict(set)

    while len(queue) > 0:
        x, y, direction = queue.popleft()
        seen[(x, y)].add(direction)

        if direction == "d":
            y += 1
        elif direction == "l":
            x -= 1
        elif direction == "r":
            x += 1
        elif direction == "u":
            y -= 1

        if x < 0 or y < 0 or x >= len(contraption[0]) or y >= len(contraption):
            continue

        symbol = contraption[y][x]

        if symbol == ".":
            queue.append((x, y, direction))
            continue

        queue.extend(
            (x, y, new_direction)
            for new_direction in REFRACTION_TABLE[symbol][direction]
            if new_direction not in seen[(x, y)]
        )

    return [tile for tile, directions in seen.items() if len(directions)]


def calculate_solution(path: Path) -> int:
    """Calculate the solution."""
    contraption = read_contraption(path)
    energized_tiles = find_energized_tiles(contraption, (-1, 0, "r"))
    return len(energized_tiles) - 1


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    solution = calculate_solution(Path(__file__).parent / "input/input")
    logging.info(solution)
