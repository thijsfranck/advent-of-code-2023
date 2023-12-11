"""Tests for Advent of Code 2023 Day 10 Part 2."""

from pathlib import Path

from .part2 import calculate_solution


def test__calculate_solution_with_simple_example_data() -> None:
    """Test whether the calculated_solution matches the simple example solution."""
    assert calculate_solution(Path(__file__).parent / "input/test__input_part2_simple") == 4

def test__calculate_solution_with_complex_example_data() -> None:
    """Test whether the calculated_solution matches the complex example solution."""
    assert calculate_solution(Path(__file__).parent / "input/test__input_part2_complex") == 8


def test__calculate_solution_with_puzzle_data() -> None:
    """Test whether the calculated_solution matches the puzzle solution."""
    assert calculate_solution(Path(__file__).parent / "input/input") == 6867
