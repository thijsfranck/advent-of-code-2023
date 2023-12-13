"""A Trie data structure for Advent of Code 2023."""

from collections.abc import Generator, Iterable


class Trie:
    """A Trie data structure."""

    def __init__(self) -> None:
        self.children: dict[str, Trie] = {}
        self.end_of_word: bool = False

    @classmethod
    def create(cls, words: Iterable[str]) -> "Trie":
        """Create a Trie from the given words."""
        trie = cls()
        for word in words:
            trie.add(word)
        return trie

    def __bool__(self) -> bool:
        return self.end_of_word

    def __contains__(self, word: str) -> bool:
        if not word:
            return self.end_of_word

        if word[0] not in self.children:
            return False

        return word[1:] in self.children[word[0]]

    def __delitem__(self, word: str) -> None:
        if not word:
            self.end_of_word = False

        if word[0] not in self.children:
            return

        del self.children[word[0]][word[1:]]

        if not self.children[word[0]]:
            del self.children[word[0]]

    def __iter__(self) -> Generator[str, None, None]:
        if self.end_of_word:
            yield ""

        for char, child in self.children.items():
            for word in child:
                yield char + word

    def __len__(self) -> int:
        return sum(1 for _ in self)

    def add(self, word: str) -> None:
        """Add a word to the Trie."""
        if not word:
            self.end_of_word = True
            return

        self.children.setdefault(word[0], Trie()).add(word[1:])

    def find(self, prefix: str) -> Generator[str, None, None]:
        """Find all words with the given prefix."""
        if not prefix:
            yield from self
            return

        if prefix[0] not in self.children:
            return

        for word in self.children[prefix[0]].find(prefix[1:]):
            yield prefix[0] + word
