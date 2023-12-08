"""Tests for Advent of Code 2023 Day 8 Part 1."""

from pathlib import Path

from .part1 import calculate_solution


def test__calculate_solution_with_first_example_data() -> None:
    """Test whether the calculated_solution matches the first example solution."""
    assert calculate_solution(Path(__file__).parent / "input/test__input_part1_a") == 2

def test__calculate_solution_with_second_example_data() -> None:
    """Test whether the calculated_solution matches the second example solution."""
    assert calculate_solution(Path(__file__).parent / "input/test__input_part1_b") == 6


def test__calculate_solution_with_puzzle_data() -> None:
    """Test whether the calculated_solution matches the puzzle solution."""
    assert calculate_solution(Path(__file__).parent / "input/input") == 18113
