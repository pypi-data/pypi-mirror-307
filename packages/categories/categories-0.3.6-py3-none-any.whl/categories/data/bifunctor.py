from __future__ import annotations

from dataclasses import dataclass
from typing import TypeVar

from categories.type import Lambda, _, hkt, typeclass

__all__ = (
    'Bifunctor',
    'BifunctorTuple',
)


a = TypeVar('a')

b = TypeVar('b')

c = TypeVar('c')

d = TypeVar('d')

p = TypeVar('p')


@dataclass(frozen=True)
class Bifunctor(typeclass[p]):
    '''
    Minimal complete definition
        bimap | first, second
    '''

    def bimap(self, f : Lambda[a, b], g : Lambda[c, d], x : hkt[p, a, c], /) -> hkt[p, b, d]:
        return self.first(f, self.second(g, x))

    def first(self, f : Lambda[a, b], x : hkt[p, a, c], /) -> hkt[p, b, c]:
        return self.bimap(f, lambda x, /: x, x)

    def second(self, g : Lambda[b, c], x : hkt[p, a, b], /) -> hkt[p, a, c]:
        return self.bimap(lambda x, /: x, g, x)


@dataclass(frozen=True)
class BifunctorTuple(Bifunctor[tuple[_, _]]):
    def bimap(self, f : Lambda[a, b], g : Lambda[c, d], z : tuple[a, c], /) -> tuple[b, d]:
        match z:
            case (x, y):
                return (f(x), g(y))
        assert None
