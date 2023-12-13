"""Tests for Advent of Code 2023 Day 0 Part 1."""

from pathlib import Path

import pytest

from .part1 import calculate_solution, find_valid_alternatives


@pytest.mark.parametrize(
    ("row", "tokens", "expected_result"),
    [
        ("???.###", ["#", "#", "#" * 3], 1),
        (".??..??...?##.", ["#", "#", "#" * 3], 4),
        ("?#?#?#?#?#?#?#?", ["#", "#" * 3, "#", "#" * 6], 1),
        ("????.#...#...", ["#" * 4, "#", "#"], 1),
        ("????.######..#####.", ["#", "#" * 6, "#" * 5], 4),
        ("?###????????", ["#" * 3, "#" * 2, "#"], 10),
    ],
)
def test__find_valid_alternatives(row: str, tokens: list[str], expected_result: int) -> None:
    """Test whether the find_valid_alternatives function works as expected."""
    assert find_valid_alternatives(row, tokens) == expected_result

def test__calculate_solution_with_example_data() -> None:
    """Test whether the calculated_solution matches the example solution."""
    assert calculate_solution(Path(__file__).parent / "input/test__input") == 21


def test__calculate_solution_with_puzzle_data() -> None:
    """Test whether the calculated_solution matches the puzzle solution."""
    assert calculate_solution(Path(__file__).parent / "input/input") == 6958
