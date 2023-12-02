"""A TrieMap data structure for Advent of Code 2023."""

from collections.abc import Iterator
from typing import Generic, TypeVar

T = TypeVar("T")


class TrieMap(Generic[T]):
    """A TrieMap data structure."""

    def __init__(self) -> None:
        self.children: dict[str, TrieMap[T]] = {}
        self.value: T | None = None

    @classmethod
    def create(cls, kv_pairs: dict[str, T]) -> "TrieMap[T]":
        """Create a TrieMap from a dictionary of key-value pairs."""
        trie = cls()
        for key, value in kv_pairs.items():
            trie[key] = value
        return trie

    def __setitem__(self, key: str, value: T) -> None:
        if not key:
            self.value = value
        else:
            self.children.setdefault(key[0], TrieMap[T]())[key[1:]] = value

    def __getitem__(self, key: str) -> T | None:
        if not key:
            return self.value

        if key[0] not in self.children:
            return None

        return self.children[key[0]][key[1:]]

    def __contains__(self, key: str) -> bool:
        if not key:
            return self.value is not None

        if key[0] not in self.children:
            return False

        return key[1:] in self.children[key[0]]

    def __delitem__(self, key: str) -> None:
        if not key:
            self.value = None

        if key[0] not in self.children:
            return

        del self.children[key[0]][key[1:]]

        if not self.children[key[0]]:
            del self.children[key[0]]

    def __iter__(self) -> Iterator[tuple[str, T]]:
        if self.value is not None:
            yield ("", self.value)

        for key, child in self.children.items():
            for suffix, value in child:
                yield (key + suffix, value)

    def find(self, key: str) -> Iterator[tuple[str, T]]:
        """Find all entries with the given prefix."""
        if not key:
            yield from self
            return

        if key[0] not in self.children:
            return

        yield from self.children[key[0]].find(key[1:])
