"""Tests for Advent of Code 2023 Day 15 Part 1."""

from pathlib import Path

import pytest

from .part1 import calculate_hash, calculate_solution


@pytest.mark.parametrize(
    ("sequence", "expected_result"),
    [
        ("HASH", 52),
        ("rn=1", 30),
        ("cm-", 253),
        ("qp=3", 97),
        ("cm=2", 47),
        ("qp-", 14),
        ("pc=4", 180),
        ("ot=9", 9),
        ("ab=5", 197),
        ("pc-", 48),
        ("pc=6", 214),
        ("ot=7", 231),
    ],
)
def test__calculate_hash(sequence: str, expected_result: int) -> None:
    """Test whether the calculated hash matches the expected result."""
    assert calculate_hash(sequence) == expected_result


def test__calculate_solution_with_example_data() -> None:
    """Test whether the calculated_solution matches the example solution."""
    assert calculate_solution(Path(__file__).parent / "input/test__input") == 1320


def test__calculate_solution_with_puzzle_data() -> None:
    """Test whether the calculated_solution matches the puzzle solution."""
    assert calculate_solution(Path(__file__).parent / "input/input") == 519041
