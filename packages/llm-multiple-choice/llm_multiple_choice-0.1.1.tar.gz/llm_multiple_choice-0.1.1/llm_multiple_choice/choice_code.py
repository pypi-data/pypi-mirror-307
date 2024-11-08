from dataclasses import dataclass
from typing import Iterator, Set

from .exceptions import DuplicateChoiceError


@dataclass(frozen=True)
class ChoiceCode:
    code: int

    def __str__(self) -> str:
        return str(self.code)


class ChoiceCodeSet:
    """A set of unique ChoiceCode objects."""

    def __init__(self) -> None:
        self._codes: Set[ChoiceCode] = set()

    @property
    def codes(self) -> frozenset[ChoiceCode]:
        return frozenset(self._codes)

    def add(self, code: ChoiceCode) -> None:
        if code in self._codes:
            raise DuplicateChoiceError(
                f"Choice code {code.code} is already in the set."
            )
        self._codes.add(code)

    def has(self, code: ChoiceCode) -> bool:
        return code in self._codes

    def __len__(self) -> int:
        return len(self._codes)

    def __iter__(self) -> Iterator[ChoiceCode]:
        return iter(self._codes)
