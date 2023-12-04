"""Tests for Advent of Code 2023 Day 4 Part 2."""

from pathlib import Path

from .part2 import count_total_cards


def test__count_total_cards_with_example_data() -> None:
    """Test whether the total card count matches the example solution."""
    assert count_total_cards(Path(__file__).parent / "input/test__input") == 30


def test__count_total_cards_with_puzzle_data() -> None:
    """Test whether the total card count matches the puzzle solution."""
    assert count_total_cards(Path(__file__).parent / "input/input") == 5704953
