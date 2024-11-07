from __future__ import annotations

from dataclasses import dataclass
from typing import TypeVar

from categories.type import typeclass

__all__ = (
    'Eq',
    'EqFloat',
    'EqInt',
)


a = TypeVar('a')


@dataclass(frozen=True)
class Eq(typeclass[a]):
    '''
    Minimal complete definition
        eq | ne
    '''

    def eq(self, x : a, y : a, /) -> bool:
        return not self.ne(x, y)

    def ne(self, x : a, y : a, /) -> bool:
        return not self.eq(x, y)


@dataclass(frozen=True)
class EqFloat(Eq[float]):
    def eq(self, x : float, y : float, /) -> bool:
        return x == y

    def ne(self, x : float, y : float, /) -> bool:
        return x != y


@dataclass(frozen=True)
class EqInt(Eq[int]):
    def eq(self, x : int, y : int, /) -> bool:
        return x == y

    def ne(self, x : int, y : int, /) -> bool:
        return x != y
