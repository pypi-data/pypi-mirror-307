from __future__ import annotations

from dataclasses import dataclass
from functools import reduce
from typing import TypeVar

from categories.data.semigroup import Semigroup, SemigroupBytes, SemigroupStr
from categories.type import typeclass

__all__ = (
    'Monoid',
    'MonoidBytes',
    'MonoidStr',
)


a = TypeVar('a')


@dataclass(frozen=True)
class Monoid(Semigroup[a], typeclass[a]):
    '''
    Minimal complete definition
        empty | concat
    '''

    def empty(self, /) -> a:
        return self.concat([])

    def concat(self, xs : list[a], /) -> a:
        return reduce(self.append, xs, self.empty())


@dataclass(frozen=True)
class MonoidBytes(SemigroupBytes, Monoid[bytes]):
    def empty(self, /) -> bytes:
        return bytes()

    def concat(self, xs : list[bytes], /) -> bytes:
        return bytes().join(xs)


@dataclass(frozen=True)
class MonoidStr(SemigroupStr, Monoid[str]):
    def empty(self, /) -> str:
        return str()

    def concat(self, xs : list[str], /) -> str:
        return str().join(xs)
