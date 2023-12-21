"""Tests for Advent of Code 2023 Day 0 Part 2."""

from pathlib import Path

import pytest

from .part2 import calculate_solution


@pytest.mark.parametrize(
    ("steps", "expected"),
    [(6, 16), (10, 50), (50, 1594), (100, 6536), (500, 167004)],
)
def test__calculate_solution_with_example_data(steps: int, expected: int) -> None:
    """Test whether the calculated_solution matches the example solution."""
    assert calculate_solution(Path(__file__).parent / "input/test__input", steps) == expected


def test__calculate_solution_with_puzzle_data() -> None:
    """Test whether the calculated_solution matches the puzzle solution."""
    assert calculate_solution(Path(__file__).parent / "input/input", 26501365) == 620348631910321
