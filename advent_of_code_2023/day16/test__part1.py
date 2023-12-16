"""Tests for Advent of Code 2023 Day 16 Part 1."""

from pathlib import Path

from .part1 import calculate_solution


def test__calculate_solution_with_example_data() -> None:
    """Test whether the calculated_solution matches the example solution."""
    assert calculate_solution(Path(__file__).parent / "input/test__input") == 46


def test__calculate_solution_with_puzzle_data() -> None:
    """Test whether the calculated_solution matches the puzzle solution."""
    assert calculate_solution(Path(__file__).parent / "input/input") == 8146
