"""Advent of Code 2023 Day 3 Part 2."""

import logging
from pathlib import Path

Matrix = list[str]

GEAR_RATIO_LENGTH = 2


def read_matrix(path: Path) -> Matrix:
    """Read a matrix from a file and return it as a list of strings."""
    with Path.open(path) as f:
        return [line.strip() for line in f.readlines() if line.strip()]


def find_gear_ratios(matrix: Matrix) -> list[int]:
    """
    Find all gear ratios in the matrix.

    A gear ratio is the product of exactly two numbers in the matrix that are adjacent
    to the same asterisk.
    """
    gear_map: dict[tuple[int, int], list[int]] = {}

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
                    if neighbour == "*":
                        gear_map.setdefault((x, y), []).append(int(number))

                number = ""

    return [gear[0] * gear[1] for gear in gear_map.values() if len(gear) == GEAR_RATIO_LENGTH]


def sum_gear_ratios(path: Path) -> int:
    """Sum all gear ratios in the matrix at the given path."""
    return sum(find_gear_ratios(read_matrix(path)))


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    solution = sum_gear_ratios(Path(__file__).parent / "input/input")
    logging.info(solution)
