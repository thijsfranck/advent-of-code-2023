"""Advent of Code 2023 Day 12 Part 1."""

import logging
from collections.abc import Generator
from pathlib import Path


def find_all_variations(row: str) -> Generator[str, None, None]:
    """Find all variations of a row."""
    if not len(row):
        yield ""
        return

    *rest, char = row
    trunk = "".join(rest)

    for variation in find_all_variations(trunk):
        if char != "?":
            yield variation + char
            continue
        yield variation + "."
        yield variation + "#"


def tokenize(row: str) -> list[str]:
    """Tokenize a row."""
    return [token for token in row.split(".") if token]


def find_valid_alternatives(row: str, tokens: list[str]) -> int:
    """Find the number of valid alternatives for a row."""
    result = 0

    for variation in find_all_variations(row):
        variation_tokens = tokenize(variation)
        if tokens == variation_tokens:
            result += 1

    return result


def read_rows(path: Path) -> Generator[tuple[str, list[str]], None, None]:
    """Read a file as a stream of characters."""
    with Path.open(path) as f:
        while line := f.readline():
            row, token_lengths = line.strip().split(" ")
            tokens: list[str] = ["#" * int(length) for length in token_lengths.split(",")]
            yield row, tokens


def calculate_solution(path: Path) -> int:
    """Calculate the solution."""
    return sum(find_valid_alternatives(row, tokens) for row, tokens in read_rows(path))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    solution = calculate_solution(Path(__file__).parent / "input/input")
    logging.info(solution)
