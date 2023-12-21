"""Advent of Code 2023 Day 21 Part 1."""

import logging
from collections import deque
from collections.abc import Generator
from pathlib import Path

Point = tuple[int, int]

DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1))


class NoStartFoundError(Exception):
    """No start found."""


def read_map(path: Path) -> list[str]:
    """Read the map."""
    with Path.open(path) as file:
        return [line.strip() for line in file if line.strip()]


def find_start(map_: list[str]) -> Point:
    """Find the start."""
    for y, line in enumerate(map_):
        for x, char in enumerate(line):
            if char == "S":
                return (x, y)
    raise NoStartFoundError


def find_points_in_range(
    map_: list[str],
    start: Point,
    range_: int,
) -> Generator[Point, None, None]:
    """Find all points reachable from start at the given range using BFS."""
    queue: deque[tuple[int, Point]] = deque([(0, start)])
    seen: set[Point] = {start}

    bound_x = len(map_[0])
    bound_y = len(map_)

    while queue:
        steps, (x, y) = queue.popleft()

        if steps % 2 == range_ % 2:
            yield (x, y)

        if steps == range_:
            continue

        for dx, dy in DIRECTIONS:
            new_x, new_y = x + dx, y + dy

            if (
                map_[new_y % bound_y][new_x % bound_x] in {".", "S"}
                and (new_x, new_y) not in seen
            ):
                seen.add((new_x, new_y))
                queue.append((steps + 1, (new_x, new_y)))


def calculate_solution(path: Path, steps: int) -> int:
    """Calculate the solution."""
    map_ = read_map(path)
    start = find_start(map_)

    points_in_range = set(find_points_in_range(map_, start, steps))

    return len(points_in_range)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    solution = calculate_solution(Path(__file__).parent / "input/input", 64)
    logging.info(solution)
