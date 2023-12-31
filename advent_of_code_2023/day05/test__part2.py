"""Tests for Advent of Code 2023 Day 5 Part 2."""

from pathlib import Path

from .part2 import calculate_solution


def test__calculate_solution_with_puzzle_data() -> None:
    """Test whether the calculated_solution matches the puzzle solution."""
    assert calculate_solution(Path(__file__).parent / "input/input") == 15290096
