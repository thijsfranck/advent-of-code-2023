"""Tests for Advent of Code 2023 Day 4 Part 1."""

from pathlib import Path

from .part1 import calculate_total_score


def test__calculate_total_score_with_example_data() -> None:
    """Test whether the sum of all card scores matches the example solution."""
    assert calculate_total_score(Path(__file__).parent / "input/test__input") == 13


def test__calculate_total_score_with_puzzle_data() -> None:
    """Test whether the sum of all card scores matches the puzzle solution."""
    assert calculate_total_score(Path(__file__).parent / "input/input") == 19135
