"""Tests for Advent of Code 2023 Day 9 Part 1."""

from pathlib import Path

import pytest

from .part1 import OasisReading, calculate_solution


@pytest.mark.parametrize(
    ("reading", "expected_value"),
    [
        ([0, 3, 6, 9, 12, 15], 18),
        ([1, 3, 6, 10, 15, 21], 28),
        ([10, 13, 16, 21, 30, 45], 68),
    ],
)
def test__extrapolate_next_reading(reading: list[int], expected_value: int) -> None:
    """Test whether the extrapolated next reading matches the expected value."""
    oasis = OasisReading(reading)
    assert oasis.next_reading == expected_value


def test__calculate_solution_with_example_data() -> None:
    """Test whether the calculated_solution matches the example solution."""
    assert calculate_solution(Path(__file__).parent / "input/test__input") == 114


def test__calculate_solution_with_puzzle_data() -> None:
    """Test whether the calculated_solution matches the puzzle solution."""
    assert calculate_solution(Path(__file__).parent / "input/input") == 2038472161
