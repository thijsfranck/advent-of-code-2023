"""Advent of Code 2023 Day 7 Part 1."""

import logging
from collections.abc import Generator, Iterable
from dataclasses import dataclass
from functools import cached_property
from pathlib import Path

CARD_STRENGTH = "23456789TJQKA"


def score(hand: str) -> int:
    """Return the score of the hand."""
    return sum(hand.count(card) for card in hand)


@dataclass
class Hand:
    """A hand of cards."""

    bid: int
    cards: str

    def __lt__(self, other: "Hand") -> bool:
        """
        Return whether the strength of this hand is less than the strength of the other hand.

        Strength is primarily based on the highest possible win condition. If both hands have the
        same win condition, the hand with the highest card going from left to right wins.
        """
        if self.strength == other.strength:
            for a, b in zip(self.cards, other.cards, strict=True):
                if a != b:
                    return CARD_STRENGTH.index(a) < CARD_STRENGTH.index(b)

        return self.strength < other.strength

    @cached_property
    def strength(self) -> int:
        """Return the strength of the hand based on the highest possible win condition."""
        return score(self.cards)


@dataclass
class CardsReader:
    """Read cards from a stream of characters."""

    cards = ""

    def read(self, char: str) -> None:
        """Read a character."""
        if char in CARD_STRENGTH:
            self.cards += char

    def reset(self) -> None:
        """Reset the reader."""
        self.cards = ""


@dataclass
class BidReader:
    """Read a bid from a stream of characters."""

    _bid = ""

    def read(self, char: str) -> None:
        """Read a character."""
        if char.isdigit():
            self._bid += char

    def reset(self) -> None:
        """Reset the reader."""
        self._bid = ""

    @property
    def bid(self) -> int:
        """Return the bid."""
        return int(self._bid)


def parse_hands(stream: Iterable[str]) -> Generator[Hand, None, None]:
    """Parse a stream of characters."""
    bid_reader = BidReader()
    cards_reader = CardsReader()

    current_reader = cards_reader

    for char in stream:
        current_reader.read(char)

        if char == " ":
            current_reader = bid_reader
            continue

        if char == "\n":
            yield Hand(bid=bid_reader.bid, cards=cards_reader.cards)
            bid_reader.reset()
            cards_reader.reset()
            current_reader = cards_reader


def read_char_stream(path: Path) -> Generator[str, None, None]:
    """Read a file as a stream of characters."""
    with Path.open(path) as f:
        while char := f.read(1):
            yield char


def calculate_solution(path: Path) -> int:
    """Calculate the solution."""
    stream = read_char_stream(path)
    hands = parse_hands(stream)

    sorted_hands = sorted(hands)

    return sum(hand.bid * i for i, hand in enumerate(sorted_hands, start=1))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    solution = calculate_solution(Path(__file__).parent / "input/input")
    logging.info(solution)
