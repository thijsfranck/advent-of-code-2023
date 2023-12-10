"""Advent of Code 2023 Day 8 Part 2."""

import logging
from collections.abc import Callable, Generator, Iterable
from dataclasses import dataclass, field
from itertools import cycle
from math import lcm
from pathlib import Path


@dataclass
class DirectionsReader:
    """Read directions from a stream of characters."""

    directions = ""

    def read(self, char: str) -> None:
        """Read a character."""
        if char != "\n":
            self.directions += char


@dataclass
class LabelReader:
    """Read a label from a stream of characters."""

    label = ""

    def read(self, char: str) -> None:
        """Read a character."""
        if char.isalnum():
            self.label += char

    def reset(self) -> None:
        """Reset the reader."""
        self.label = ""


@dataclass(frozen=True)
class Node:
    """A node in a map."""

    label: str
    edges: dict[str, str] = field(default_factory=dict)

    def get_left_edge(self) -> str:
        """Return the label of the node on the left edge."""
        return self.edges["L"]

    def get_right_edge(self) -> str:
        """Return the label of the node on the right edge."""
        return self.edges["R"]


@dataclass(frozen=True)
class Map:
    """A map consisting of base directions and a set of nodes."""

    directions: str
    nodes: dict[str, Node] = field(default_factory=dict)

    def navigate(self, start: str, predicate: Callable[[str], bool]) -> list[str]:
        """Navigate from the start to the end."""
        path = [start]

        # Follow the known directions until the path is found.
        for direction in cycle(self.directions):
            current = path[-1]
            if predicate(current):
                return path
            if direction == "L":
                path.append(self.nodes[current].get_left_edge())
            elif direction == "R":
                path.append(self.nodes[current].get_right_edge())

        return []


def parse_map(stream: Iterable[str]) -> Map:
    """Parse a stream of characters into a Map."""
    directions_reader = DirectionsReader()
    node_label_reader = LabelReader()
    left_edge_label_reader = LabelReader()
    right_edge_label_reader = LabelReader()

    current_reader = directions_reader

    nodes: dict[str, Node] = {}

    for char in stream:
        if char == "\n":
            break

        directions_reader.read(char)

    current_reader = node_label_reader

    for char in stream:
        if char == "\n" and node_label_reader.label:
            nodes[node_label_reader.label] = Node(
                label=node_label_reader.label,
                edges={"L": left_edge_label_reader.label, "R": right_edge_label_reader.label},
            )

            node_label_reader.reset()
            left_edge_label_reader.reset()
            right_edge_label_reader.reset()
            current_reader = node_label_reader

            continue

        if char == "\n":
            continue

        if char == "=":
            current_reader = left_edge_label_reader
            continue

        if char == ",":
            current_reader = right_edge_label_reader
            continue

        current_reader.read(char)

    return Map(directions=directions_reader.directions, nodes=nodes)


def read_char_stream(path: Path) -> Generator[str, None, None]:
    """Read a file as a stream of characters."""
    with Path.open(path) as f:
        while char := f.read(1):
            yield char


def calculate_solution(path: Path) -> int:
    """Calculate the solution."""
    stream = read_char_stream(path)
    map_ = parse_map(stream)

    positions = [label for label in map_.nodes if label.endswith("A")]

    def predicate(position: str) -> bool:
        return position.endswith("Z")

    paths = [map_.navigate(position, predicate) for position in positions]

    return lcm(*[len(path) - 1 for path in paths])


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    solution = calculate_solution(Path(__file__).parent / "input/input")
    logging.info(solution)
