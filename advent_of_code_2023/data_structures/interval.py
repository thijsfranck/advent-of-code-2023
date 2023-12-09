"""An Interval data structure for Advent of Code 2023."""

from collections.abc import Generator
from dataclasses import dataclass


@dataclass(frozen=True)
class Interval:
    """An Interval data structure."""

    start: int
    end: int

    def __repr__(self) -> str:
        return f"Interval({self.start}, {self.end})"

    def __str__(self) -> str:
        return f"[{self.start}, {self.end})"

    def __len__(self) -> int:
        return self.end - self.start

    def __lt__(self, other: "Interval") -> bool:
        return self.start < other.start and self.end < other.end

    def __gt__(self, other: "Interval") -> bool:
        return self.start > other.start and self.end > other.end

    def __bool__(self) -> bool:
        return self.start < self.end

    def __iter__(self) -> Generator[int, None, None]:
        yield from range(self.start, self.end)

    def __contains__(self, other: int) -> bool:
        return self.start <= other < self.end

    def __and__(self, other: "Interval") -> "Interval":
        """Return the intersection between two intervals."""
        if self.end < other.start or other.end < self.start:
            return Interval(0, 0)

        return Interval(max(self.start, other.start), min(self.end, other.end))

    def __add__(self, other: "Interval") -> "Interval":
        """Return the union between two intervals."""
        return Interval(min(self.start, other.start), max(self.end, other.end))

    def __sub__(self, other: "Interval") -> "Interval":
        """Return the gap between two intervals."""
        if self.end < other.start:
            return Interval(self.end, other.start)

        if other.end < self.start:
            return Interval(other.end, self.start)

        return Interval(0, 0)
