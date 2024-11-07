from __future__ import annotations

from dataclasses import dataclass
from typing import TypeVar

from categories.type import Lambda, hkt, typeclass

__all__ = (
    'Category',
    'CategoryLambda',
)


a = TypeVar('a')

b = TypeVar('b')

c = TypeVar('c')

cat = TypeVar('cat')


@dataclass(frozen=True)
class Category(typeclass[cat]):
    '''
    Minimal complete definition
        id, o
    '''

    def id(self, /) -> hkt[cat, a, a]: ...

    def o(self, f : hkt[cat, b, c], g : hkt[cat, a, b], /) -> hkt[cat, a, c]: ...


@dataclass(frozen=True)
class CategoryLambda(Category[Lambda]):
    def id(self, /) -> Lambda[a, a]:
        return lambda x, /: x

    def o(self, f : Lambda[b, c], g : Lambda[a, b], /) -> Lambda[a, c]:
        return lambda x, /: f(g(x))
