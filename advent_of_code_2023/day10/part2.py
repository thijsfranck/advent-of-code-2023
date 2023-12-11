"""Advent of Code 2023 Day 10 Part 2."""

import logging
from pathlib import Path


def find_enclosed_tiles(path: Path) -> int:
    """Count the number of tiles that cannot be reached from the edges."""
    with Path.open(path) as f:
        lines = [line.strip() for line in f.readlines()]

    if not any(lines):
        return 0

    reachable = set()
    unreachable = set()

    matrix_width = len(lines[0])
    matrix_height = len(lines)
    matrix_size = matrix_width * matrix_height

    # Iterate over the matrix in a spiral pattern to find the unreachable tiles.

    x = 0
    y = 0
    dx = 1
    dy = 0

    def is_reachable() -> bool:
        """Check whether any of the surrounding tiles are reachable."""
        return any(
            [
                x == 0,
                y == 0,
                x == matrix_width - 1,
                y == matrix_height - 1,
                (x - 1, y) in reachable,
                (x + 1, y) in reachable,
                (x, y - 1) in reachable,
                (x, y + 1) in reachable,
            ],
        )

    for _ in range(matrix_size):
        if lines[y][x] == ".":
            if is_reachable():
                reachable.add((x, y))
            else:
                unreachable.add((x, y))

        if (
            x + dx < 0
            or x + dx >= matrix_width
            or y + dy < 0
            or y + dy >= matrix_height
            or (x + dx, y + dy) in reachable
        ):
            dx, dy = -dy, dx

        x += dx
        y += dy

    return len(unreachable)


def calculate_solution(path: Path) -> int:
    """Calculate the solution to the problem."""
    return find_enclosed_tiles(path)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    solution = calculate_solution(Path(__file__).parent / "input/input")
    logging.info(solution)
