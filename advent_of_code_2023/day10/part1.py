"""Advent of Code 2023 Day 10 Part 1."""

import logging
from collections import defaultdict, deque
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Graph:
    """A basic graph that maps the metal island landscape."""

    nodes: set[tuple[int, int]] = field(default_factory=set)
    edges: dict[tuple[int, int], set[tuple[int, int]]] = field(
        default_factory=lambda: defaultdict(set),
    )
    start: tuple[int, int] = (0, 0)

    def add_node(self, node: tuple[int, int]) -> None:
        """Add a node to the graph."""
        self.nodes.add(node)

    def add_edge(self, node1: tuple[int, int], node2: tuple[int, int]) -> None:
        """Add an edge to the graph."""
        self.add_node(node1)
        self.add_node(node2)
        self.edges[node1].add(node2)
        self.edges[node2].add(node1)

    def find_longest_path(self, start: tuple[int, int]) -> int:
        """Find the longest path from the given start position."""
        queue: deque[list[tuple[int, int]]] = deque([[start]])
        max_distance = 0

        while queue:
            path = queue.pop()
            node = path[-1]

            for neighbor in self.edges[node]:
                if neighbor == node:
                    continue
                if neighbor == start:
                    max_distance = max(max_distance, len(path))
                elif neighbor not in path:
                    queue.append([*path, neighbor])

        return max_distance


def read_graph(path: Path) -> Graph:
    """Read a Graph from a file."""
    with Path.open(path) as f:
        lines = [line.strip() for line in f.readlines()]

    graph = Graph()

    if not any(lines):
        return graph

    line_length = len(lines[0])

    actions = {
        ".": lambda x, y: graph.add_node((x, y)),
        "S": lambda x, y: (graph.add_node((x, y)), setattr(graph, "start", (x, y))),
        "|": lambda x, y: (
            (
                y - 1 >= 0
                and lines[y - 1][x] in {"S", "|", "7", "F"}
                and graph.add_edge((x, y), (x, y - 1))
            ),
            (
                y + 1 < len(lines)
                and lines[y + 1][x] in {"S", "|", "L", "J"}
                and graph.add_edge((x, y), (x, y + 1))
            ),
        ),
        "-": lambda x, y: (
            (
                x - 1 >= 0
                and lines[y][x - 1] in {"S", "-", "L", "F"}
                and graph.add_edge((x, y), (x - 1, y))
            ),
            (
                x + 1 < line_length
                and lines[y][x + 1] in {"S", "-", "J", "7"}
                and graph.add_edge((x, y), (x + 1, y))
            ),
        ),
        "L": lambda x, y: (
            (
                y - 1 >= 0
                and lines[y - 1][x] in {"S", "|", "7", "F"}
                and graph.add_edge((x, y), (x, y - 1))
            ),
            (
                x + 1 < line_length
                and lines[y][x + 1] in {"S", "-", "J", "7"}
                and graph.add_edge((x, y), (x + 1, y))
            ),
        ),
        "J": lambda x, y: (
            (
                y - 1 >= 0
                and lines[y - 1][x] in {"S", "|", "7", "F"}
                and graph.add_edge((x, y), (x, y - 1))
            ),
            (
                x - 1 >= 0
                and lines[y][x - 1] in {"S", "-", "L", "F"}
                and graph.add_edge((x, y), (x - 1, y))
            ),
        ),
        "7": lambda x, y: (
            (
                x - 1 >= 0
                and lines[y][x - 1] in {"S", "-", "L", "F"}
                and graph.add_edge((x, y), (x - 1, y))
            ),
            (
                y + 1 < len(lines)
                and lines[y + 1][x] in {"S", "|", "L", "J"}
                and graph.add_edge((x, y), (x, y + 1))
            ),
        ),
        "F": lambda x, y: (
            (
                x + 1 < line_length
                and lines[y][x + 1] in {"S", "-", "J", "7"}
                and graph.add_edge((x, y), (x + 1, y))
            ),
            (
                y + 1 < len(lines)
                and lines[y + 1][x] in {"S", "|", "L", "J"}
                and graph.add_edge((x, y), (x, y + 1))
            ),
        ),
    }

    for i in range(len(lines) * line_length):
        y, x = divmod(i, line_length)
        char = lines[y][x]

        action = actions.get(char)
        if action:
            action(x, y)
        else:
            logging.error("Unknown character %s at position %s", char, (x, y))

    return graph


def calculate_solution(path: Path) -> int:
    """Calculate the solution."""
    graph = read_graph(path)
    return graph.find_longest_path(graph.start) // 2


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    solution = calculate_solution(Path(__file__).parent / "input/input")
    logging.info(solution)
