"""Tests for Advent of Code 2023 Day 2 Part 1."""

from pathlib import Path

from .part2 import calculate_set_power


def test_find_valid_cube_sets_with_example_data() -> None:
    """Test whether the sum of all valid cube sets matches the example solution."""
    assert calculate_set_power(Path(__file__).parent / "input/test__input") == 2286


def test_find_valid_cube_sets_with_puzzle_data() -> None:
    """Test whether the sum of all valid cube sets matches the puzzle solution."""
    assert calculate_set_power(Path(__file__).parent / "input/input") == 65122
