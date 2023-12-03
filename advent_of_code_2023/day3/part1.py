"""Advent of Code 2023 Day 3 Part 1."""

import logging
from collections.abc import Generator
from pathlib import Path

Matrix = list[str]


def read_matrix(path: Path) -> Matrix:
    """Read a matrix from a file and return it as a list of strings."""
    with Path.open(path) as f:
        return [line.strip() for line in f.readlines() if line.strip()]


def find_part_numbers(matrix: Matrix) -> Generator[int, None, None]:
    """Find all numbers adjacent to a symbol in the given matrix."""
    for row, line in enumerate(matrix):
        number: str = ""

        for column, char in enumerate(line):
            is_digit = char.isdigit()

            if is_digit:
                number += char

            end_of_number = number and (not is_digit or column == len(line) - 1)

            if end_of_number:
                coordinates = [
                    (row, column - (len(number) if is_digit else len(number) + 1)),
                    (row, column),
                ]

                if row > 0:
                    coordinates.extend(
                        [
                            (row - 1, column)
                            for column in range(
                                max(0, column - len(number) - 1),
                                min(len(line), column + 1),
                            )
                        ],
                    )

                if row < len(matrix) - 1:
                    coordinates.extend(
                        [
                            (row + 1, column)
                            for column in range(
                                max(0, column - len(number) - 1),
                                min(len(line), column + 1),
                            )
                        ],
                    )

                for x, y in coordinates:
                    neighbour = matrix[x][y]
                    if not neighbour.isalnum() and neighbour != ".":
                        yield int(number)
                        break

                number = ""


def sum_part_numbers(path: Path) -> int:
    """Sum all numbers adjacent to a symbol in the given matrix."""
    return sum(find_part_numbers(read_matrix(path)))


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    solution = sum_part_numbers(Path(__file__).parent / "input/input")
    logging.info(solution)
