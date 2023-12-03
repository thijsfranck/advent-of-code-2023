"""Tests for Advent of Code Day 3 Part 2."""

from pathlib import Path

from .part2 import sum_gear_ratios


def test__sum_gear_ratios_with_example_input() -> None:
    """Test sum_gear_ratios with example input."""
    assert sum_gear_ratios(Path(__file__).parent / "input/test__input") == 467835


def test__sum_gear_ratios_with_puzzle_input() -> None:
    """Test sum_gear_ratios with puzzle input."""
    assert sum_gear_ratios(Path(__file__).parent / "input/input") == 539637
