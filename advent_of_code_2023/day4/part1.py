"""Advent of Code 2023 Day 4 Part 1."""

import logging
from collections.abc import Generator, Iterable
from dataclasses import dataclass, field
from functools import cached_property
from pathlib import Path


def read_char_stream(path: Path) -> Generator[str, None, None]:
    """Read a file as a stream of characters."""
    with Path.open(path) as f:
        while char := f.read(1):
            yield char


@dataclass(frozen=True)
class Card:
    """A scratch card."""

    card_id: str
    winning_numbers: set[int]
    your_numbers: set[int]

    @cached_property
    def matching_numbers(self) -> set[int]:
        """Calculate the matching numbers of the card."""
        return self.winning_numbers & self.your_numbers

    @cached_property
    def score(self) -> int:
        """Calculate the score of the card."""
        return pow(2, len(self.matching_numbers) - 1) if self.matching_numbers else 0


@dataclass
class CardIdReader:
    """A reader for scratch card ids."""

    card_id = ""

    def read(self, char: str) -> None:
        """Read a character."""
        if char.isdigit():
            self.card_id += char

    def reset(self) -> None:
        """Reset the reader."""
        self.card_id = ""


@dataclass
class NumbersReader:
    """A reader for scratch card numbers."""

    current_number = ""
    numbers: set[int] = field(default_factory=set)

    def read(self, char: str) -> None:
        """Read a character."""
        if char.isdigit():
            self.current_number += char
            return

        if self.current_number and char in {" ", "\n"}:
            self.numbers.add(int(self.current_number))
            self.current_number = ""

    def reset(self) -> None:
        """Reset the reader."""
        self.current_number = ""
        self.numbers.clear()


@dataclass
class Parser:
    """A scratch card parser."""

    stream: Iterable[str]

    current_reader: CardIdReader | NumbersReader = field(init=False)
    card_id_reader: CardIdReader = field(default_factory=CardIdReader)
    winning_numbers_reader: NumbersReader = field(default_factory=NumbersReader)
    your_numbers_reader: NumbersReader = field(default_factory=NumbersReader)

    def __post_init__(self) -> None:
        """Initialize the parser state."""
        self.current_reader = self.card_id_reader

    def __iter__(self) -> Generator[Card, None, None]:
        """Read a stream of characters."""
        for char in self.stream:
            if char == ":":
                self.current_reader = self.winning_numbers_reader
                continue

            if char == "|":
                self.current_reader = self.your_numbers_reader
                continue

            self.current_reader.read(char)

            if char == "\n":
                yield self.build_card()
                self.reset()

    def build_card(self) -> Card:
        """Build a card from the parser state."""
        return Card(
            card_id=self.card_id_reader.card_id,
            winning_numbers=self.winning_numbers_reader.numbers,
            your_numbers=self.your_numbers_reader.numbers,
        )

    def reset(self) -> None:
        """Reset the parser state."""
        self.card_id_reader.reset()
        self.winning_numbers_reader.reset()
        self.your_numbers_reader.reset()
        self.current_reader = self.card_id_reader


def calculate_total_score(path: Path) -> int:
    """Calculate the total score of all scratch cards."""
    return sum(card.score for card in Parser(read_char_stream(path)))


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    solution = calculate_total_score(Path(__file__).parent / "input/input")
    logging.info(solution)
