from __future__ import annotations

from dataclasses import dataclass
from typing import TypeVar

from categories.data.eq import Eq, EqFloat, EqInt
from categories.type import typeclass

__all__ = (
    'Ord',
    'OrdFloat',
    'OrdInt',
    'Ordering',
    'LT',
    'EQ',
    'GT',
)


a = TypeVar('a')


@dataclass(frozen=True)
class LT: ...


@dataclass(frozen=True)
class EQ: ...


@dataclass(frozen=True)
class GT: ...


Ordering = LT | EQ | GT


@dataclass(frozen=True)
class Ord(Eq[a], typeclass[a]):
    '''
    Minimal complete definition
        cmp | le
    '''

    def cmp(self, x : a, y : a, /) -> Ordering:
        return EQ() if self.eq(x, y) \
          else LT() if self.le(x, y) \
          else GT()

    def le(self, x : a, y : a, /) -> bool:
        match self.cmp(x, y):
            case GT():
                return False
            case _:
                return True
        assert None

    def ge(self, x : a, y : a, /) -> bool:
        return self.le(y, x)

    def gt(self, x : a, y : a, /) -> bool:
        return not self.le(x, y)

    def lt(self, x : a, y : a, /) -> bool:
        return not self.le(y, x)

    def max(self, x : a, y : a, /) -> a:
        return y if self.le(x, y) else x

    def min(self, x : a, y : a, /) -> a:
        return x if self.le(x, y) else y


@dataclass(frozen=True)
class OrdFloat(EqFloat, Ord[float]):
    def cmp(self, x : float, y : float, /) -> Ordering:
        return EQ() if x == y \
          else LT() if x <= y \
          else GT()

    def le(self, x : float, y : float, /) -> bool:
        return x <= y

    def ge(self, x : float, y : float, /) -> bool:
        return x >= y

    def gt(self, x : float, y : float, /) -> bool:
        return x > y

    def lt(self, x : float, y : float, /) -> bool:
        return x < y

    def max(self, x : float, y : float, /) -> float:
        return y if x <= y else x

    def min(self, x : float, y : float, /) -> float:
        return x if x <= y else y


@dataclass(frozen=True)
class OrdInt(EqInt, Ord[int]):
    def cmp(self, x : int, y : int, /) -> Ordering:
        return EQ() if x == y \
          else LT() if x <= y \
          else GT()

    def le(self, x : int, y : int, /) -> bool:
        return x <= y

    def ge(self, x : int, y : int, /) -> bool:
        return x >= y

    def gt(self, x : int, y : int, /) -> bool:
        return x > y

    def lt(self, x : int, y : int, /) -> bool:
        return x < y

    def max(self, x : int, y : int, /) -> int:
        return y if x <= y else x

    def min(self, x : int, y : int, /) -> int:
        return x if x <= y else y
