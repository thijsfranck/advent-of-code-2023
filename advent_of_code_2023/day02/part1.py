"""Advent of Code 2023 Day 2 Part 1."""

import logging
from collections import defaultdict
from collections.abc import Generator, Iterable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Protocol, TypedDict


class CubeSet(TypedDict):
    """A cube set."""

    id: int
    config: dict[str, int]


class NoGameIdError(Exception):
    """Raised when a cube set has no game id."""


class CubeSetReader(Protocol):
    """A cube set reader."""

    def read(self, char: str) -> None:
        """Read a character."""

    def reset(self) -> None:
        """Reset the reader."""


@dataclass
class ReadingGameIdState:
    """The state of the parser when reading a game id."""

    parser_state: "Parser"
    game_id: str = ""

    def read(self, char: str) -> None:
        """Read a character."""
        if char == ":":
            if not self.game_id:
                raise NoGameIdError

            self.parser_state.current_reader = self.parser_state.cube_set_state
            return

        if char.isdigit():
            self.game_id += char

    def reset(self) -> None:
        """Reset the reader."""
        self.game_id = ""


@dataclass
class ReadingCubeSetState:
    """The state of the parser when reading a cube set."""

    parser_state: "Parser"
    color: str = ""
    number: str = ""
    cube_config: dict[str, int] = field(default_factory=lambda: defaultdict(int))

    def read(self, char: str) -> None:
        """Read a character."""
        if char == " ":
            return

        if char.isdigit():
            self.number += char
            return

        if char in {",", ";", "\n"}:
            score = int(self.number)

            if score > self.cube_config[self.color]:
                self.cube_config[self.color] = score

            self.color = ""
            self.number = ""

            return

        self.color += char

    def reset(self) -> None:
        """Reset the reader."""
        self.color = ""
        self.number = ""
        self.cube_config = defaultdict(int)


@dataclass
class Parser:
    """A parser for cube sets."""

    stream: Iterable[str]

    current_reader: CubeSetReader = field(init=False)
    game_id_state: ReadingGameIdState = field(init=False)
    cube_set_state: ReadingCubeSetState = field(init=False)

    def __post_init__(self) -> None:
        """Initialize the parser state."""
        self.game_id_state = ReadingGameIdState(self)
        self.cube_set_state = ReadingCubeSetState(self)

        self.current_reader = self.game_id_state

    def build_cube_set(self) -> CubeSet:
        """Build a cube set from the parser state."""
        return {"id": int(self.game_id_state.game_id), "config": self.cube_set_state.cube_config}

    def __iter__(self) -> Generator[CubeSet, None, None]:
        """Read a stream of characters."""
        for char in self.stream:
            self.current_reader.read(char)

            if char == "\n":
                yield self.build_cube_set()
                self.reset()

    def reset(self) -> None:
        """Reset the parser state."""
        self.game_id_state.reset()
        self.cube_set_state.reset()
        self.current_reader = self.game_id_state


CONFIGURATION = {"red": 12, "green": 13, "blue": 14}


def read_char_stream(path: Path) -> Generator[str, None, None]:
    """Read a file as a stream of characters."""
    with Path.open(path) as f:
        while char := f.read(1):
            yield char


def is_valid(cube_set: CubeSet) -> bool:
    """Determine whether the given cube set is valid."""
    return all(
        cube_count <= CONFIGURATION[color] for color, cube_count in cube_set["config"].items()
    )


def find_valid_cube_sets(path: Path) -> int:
    """Find the sum of ids for all valid cube sets."""
    stream = read_char_stream(path)
    return sum(cube_set["id"] for cube_set in Parser(stream) if is_valid(cube_set))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    solution = find_valid_cube_sets(Path(__file__).parent / "input/input")
    logging.info(solution)
