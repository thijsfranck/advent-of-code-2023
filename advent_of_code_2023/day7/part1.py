"""Advent of Code 2023 Day 7 Part 1."""

import logging
from collections.abc import Generator, Iterable
from dataclasses import dataclass
from functools import cached_property
from pathlib import Path

CARD_STRENGTH = "23456789TJQKA"

WIN_CONDITIONS = [
    "is_five_of_a_kind",
    "is_four_of_a_kind",
    "is_full_house",
    "is_three_of_a_kind",
    "is_two_pairs",
    "is_one_pair",
    "is_high_card",
]


@dataclass
class Hand:
    """A hand of cards."""

    bid: int
    cards: tuple[str, str, str, str, str]

    def is_five_of_a_kind(self) -> bool:
        """Return whether the hand is five of a kind."""
        return len(set(self.cards)) == 1

    def is_four_of_a_kind(self) -> bool:
        """Return whether the hand is four of a kind."""
        return (
            len(self.card_set) == 2  # noqa: PLR2004
            and any(self.cards.count(card) == 4 for card in self.card_set)  # noqa: PLR2004
        )

    def is_full_house(self) -> bool:
        """Return whether the hand is a full house."""
        return (
            len(self.card_set) == 2  # noqa: PLR2004
            and any(self.cards.count(card) == 3 for card in self.card_set)  # noqa: PLR2004
        )

    def is_three_of_a_kind(self) -> bool:
        """Return whether the hand is three of a kind."""
        return (
            len(self.card_set) == 3  # noqa: PLR2004
            and any(self.cards.count(card) == 3 for card in self.card_set)  # noqa: PLR2004
        )

    def is_two_pairs(self) -> bool:
        """Return whether the hand is two pairs."""
        return (
            len(self.card_set) == 3  # noqa: PLR2004
            and any(self.cards.count(card) == 2 for card in self.card_set)  # noqa: PLR2004
        )

    def is_one_pair(self) -> bool:
        """Return whether the hand is one pair."""
        return (
            len(self.card_set) == 4  # noqa: PLR2004
            and any(self.cards.count(card) == 2 for card in self.card_set)  # noqa: PLR2004
        )

    def is_high_card(self) -> bool:
        """Return whether the hand is a high card."""
        return len(self.card_set) == 5  # noqa: PLR2004

    @cached_property
    def card_set(self) -> set[str]:
        """Return the set of cards excluding jokers."""
        return set(self.cards)

    @property
    def high_card_strength(self) -> int:
        """Return the strength of the high card."""
        return max(CARD_STRENGTH.index(card) for card in self.cards)

    @cached_property
    def win_condition(self) -> str:
        """Return the win condition of the hand."""
        for win_condition in WIN_CONDITIONS:
            has_win_condition = getattr(self, win_condition)()
            if has_win_condition:
                return win_condition
        return WIN_CONDITIONS[-1]

    def __lt__(self, other: "Hand") -> bool:
        """Return whether the hand is less than the other hand."""
        if self.win_condition != other.win_condition:
            return WIN_CONDITIONS.index(other.win_condition) < WIN_CONDITIONS.index(
                self.win_condition,
            )

        for a, b in zip(self.cards, other.cards, strict=True):
            if a != b:
                return CARD_STRENGTH.index(a) < CARD_STRENGTH.index(b)

        return False


@dataclass
class CardsReader:
    """Read cards from a stream of characters."""

    _symbols = ""

    def read(self, char: str) -> None:
        """Read a character."""
        if char in CARD_STRENGTH:
            self._symbols += char

    def reset(self) -> None:
        """Reset the reader."""
        self._symbols = ""

    @property
    def cards(self) -> tuple[str, str, str, str, str]:
        """Return the cards as a tuple."""
        a, b, c, d, e = self._symbols
        return (a, b, c, d, e)


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
