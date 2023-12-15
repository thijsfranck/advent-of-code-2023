"""Advent of Code 2023 Day 15 Part 2."""

import logging
from collections import defaultdict
from collections.abc import Generator, Iterable
from functools import reduce
from pathlib import Path

Step = tuple[str, str, int]


def read_char_stream(path: Path) -> Generator[str, None, None]:
    """Read a file as a stream of characters."""
    with Path.open(path) as f:
        while char := f.read(1):
            yield char


def parse_initialization_sequences(stream: Iterable[str]) -> Generator[Step, None, None]:
    """Parse steps from a stream of characters."""
    current_label = ""
    current_operator = ""
    current_focal_length = ""

    for char in stream:
        if char in {"\n", ","}:
            yield (
                current_label,
                current_operator,
                int(current_focal_length) if current_focal_length else 0,
            )
            current_label = ""
            current_operator = ""
            current_focal_length = ""
            continue

        if char.isalpha():
            current_label += char
            continue

        if char.isdigit():
            current_focal_length += char
            continue

        if char in {"=", "-"}:
            current_operator += char
            continue


def calculate_hash(initialization_sequence: str) -> int:
    """Calculate the hash of an initialization sequence."""
    return reduce(
        lambda result, char: ((result + ord(char)) * 17) % 256,
        initialization_sequence,
        0,
    )


def calculate_solution(path: Path) -> int:
    """Calculate the solution."""
    boxes: dict[int, dict[str, int]] = defaultdict(dict)

    for label, operator, focal_length in parse_initialization_sequences(read_char_stream(path)):
        label_hash = calculate_hash(label)
        box = boxes[label_hash]
        if operator == "=":
            box[label] = focal_length
        elif operator == "-" and label in box:
            del box[label]

    return sum(
        (1 + box) * (1 + slot) * focal_length
        for box, lenses in boxes.items()
        for slot, focal_length in enumerate(lenses.values())
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    solution = calculate_solution(Path(__file__).parent / "input/input")
    logging.info(solution)
