"""Tests for Advent of Code Day 3 Part 1."""

from pathlib import Path

from .part1 import sum_part_numbers


def test__sum_part_numbers_with_example_input() -> None:
    """Test sum_part_numbers with example input."""
    assert sum_part_numbers(Path(__file__).parent / "input/test__input") == 4361


def test__sum_part_numbers_with_puzzle_input() -> None:
    """Test sum_part_numbers with puzzle input."""
    assert sum_part_numbers(Path(__file__).parent / "input/input") == 539637
