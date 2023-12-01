"""Tests for Advent of Code 2023 Day 1 Part 2."""

from pathlib import Path

from .part2 import sum_calibration_values


def test__sum_calibration_values_with_test_input() -> None:
    """Test whether the sum of all calibration values matches the example solution."""
    assert sum_calibration_values(Path(__file__).parent / "input/test__input_part2") == 281


def test__sum_calibration_values_with_puzzle_input() -> None:
    """Test whether the sum of all calibration values matches the puzzle solution."""
    assert sum_calibration_values(Path(__file__).parent / "input/input") == 54824
