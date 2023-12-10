"""Tests for Advent of Code 2023 Day 2 Part 1."""

from pathlib import Path

from .part1 import find_valid_cube_sets


def test__find_valid_cube_sets_with_example_data() -> None:
    """Test whether the sum of all valid cube sets matches the example solution."""
    assert find_valid_cube_sets(Path(__file__).parent / "input/test__input") == 8


def test__find_valid_cube_sets_with_puzzle_data() -> None:
    """Test whether the sum of all valid cube sets matches the puzzle solution."""
    assert find_valid_cube_sets(Path(__file__).parent / "input/input") == 2879
