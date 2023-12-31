"""Advent of Code 2023 Day 17 Part 2."""

import heapq
import logging
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

Coordinate = tuple[int, int]
Direction = tuple[int, int]
Distance = float
Step = int

# The directions we can move in, and the directions we can turn in from each direction.
DIRECTIONS: dict[Direction, list[Direction]] = {
    (0, 0): [(0, 1), (0, -1), (1, 0), (-1, 0)],
    (0, 1): [(1, 0), (-1, 0)],
    (0, -1): [(1, 0), (-1, 0)],
    (1, 0): [(0, 1), (0, -1)],
    (-1, 0): [(0, 1), (0, -1)],
}

# The maximum number of steps we can take in the same direction.
MAX_STEPS = 10
MIN_STEPS = 4


@dataclass
class NoPathFoundError(Exception):
    """Raised when no path is found."""

    end: Coordinate
    start: Coordinate

    def __str__(self) -> str:
        """Return the string representation of the error."""
        return f"No path found between {self.start} and {self.end}."


def read_heatmap(path: Path) -> list[list[int]]:
    """Read a map from a file."""
    with Path.open(path) as f:
        return [[int(c) for c in line.strip()] for line in f.readlines() if line.strip()]


def dijkstra(
    graph: list[list[int]],
    start: Coordinate,
    end: Coordinate,
) -> Distance:
    """Find the smallest distance between the given start and end points."""
    distances: dict[tuple[Coordinate, Direction, Step], Distance] = defaultdict(
        lambda: float("inf"),
    )

    bound_x, bound_y = len(graph[0]), len(graph)

    min_heap: list[tuple[Distance, Coordinate, Direction, Step]] = [
        (0, start, (0, 0), MAX_STEPS),
    ]

    while len(min_heap):
        distance_from_start, (x, y), direction, steps = heapq.heappop(min_heap)

        directions = (
            [direction]
            if steps < MIN_STEPS
            else [direction, *DIRECTIONS[direction]]
            if steps < MAX_STEPS
            else DIRECTIONS[direction]
        )

        for new_direction in directions:
            dx, dy = new_direction
            nx, ny = x + dx, y + dy

            if not (0 <= nx < bound_x and 0 <= ny < bound_y):
                continue

            dist_to_new_point = distance_from_start + graph[ny][nx]
            new_coordinate = (nx, ny)
            new_steps = steps + 1 if new_direction == direction else 1

            if new_coordinate == end and new_steps >= MIN_STEPS:
                return dist_to_new_point

            key = (new_coordinate, new_direction, new_steps)

            if dist_to_new_point >= distances[key]:
                continue

            distances[key] = dist_to_new_point

            heapq.heappush(
                min_heap,
                (
                    dist_to_new_point,
                    new_coordinate,
                    new_direction,
                    new_steps,
                ),
            )

    raise NoPathFoundError(start=start, end=end)


def calculate_solution(path: Path) -> Distance:
    """Calculate the solution."""
    heatmap = read_heatmap(path)

    start = (0, 0)
    end = (len(heatmap[0]) - 1, len(heatmap) - 1)

    return dijkstra(heatmap, start, end)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    solution = calculate_solution(Path(__file__).parent / "input/input")
    logging.info(solution)
