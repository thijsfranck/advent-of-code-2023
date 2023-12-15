"""Advent of Code 2023 Day 15 Part 2."""

import contextlib
import logging
from collections import defaultdict
from collections.abc import Generator, Iterable
from dataclasses import dataclass
from functools import reduce
from pathlib import Path


def read_char_stream(path: Path) -> Generator[str, None, None]:
    """Read a file as a stream of characters."""
    with Path.open(path) as f:
        while char := f.read(1):
            yield char


@dataclass(frozen=True)
class Step:
    """A step in the initialization sequence."""

    label: str
    operator: str
    focal_length: int = 0

    def __hash__(self) -> int:
        return reduce(
            lambda result, char: ((result + ord(char)) * 17) % 256,
            self.label,
            0,
        )

    def __eq__(self, other: "Step") -> bool:
        return self.label == other.label

    def apply(self, box: list["Step"]) -> None:
        """Apply the step to the box."""
        if self.operator == "-":
            try:
                box.remove(self)
            except ValueError:
                contextlib.suppress(ValueError)
            return
        try:
            index = box.index(self)
            box[index] = self
        except ValueError:
            box.append(self)


def parse_initialization_sequences(stream: Iterable[str]) -> Generator[Step, None, None]:
    """Parse steps from a stream of characters."""
    current_label = ""
    current_operator = ""
    current_focal_length = ""

    for char in stream:
        if char in {"\n", ","}:
            yield Step(
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


def calculate_solution(path: Path) -> int:
    """Calculate the solution."""
    boxes: dict[int, list[Step]] = defaultdict(list)

    for step in parse_initialization_sequences(read_char_stream(path)):
        step.apply(boxes[hash(step)])

    return sum(
        (1 + box) * (1 + slot) * lens.focal_length
        for box, lenses in boxes.items()
        for slot, lens in enumerate(lenses)
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    solution = calculate_solution(Path(__file__).parent / "input/input")
    logging.info(solution)
