from __future__ import annotations

from functools import lru_cache, partial
from typing import ParamSpec, TypeVar

from categories.type import Cons, Expr, Lambda, Map, Void

__all__ = (
    'ap',
    'let',
    'memo',
    'rec',
    'seq',
    'undefined',
)


a = TypeVar('a')

b = TypeVar('b')

x = TypeVar('x')

xs = ParamSpec('xs')

y = TypeVar('y')


def ap(f : Expr[Cons[x, xs], y], x : x, /) -> Expr[xs, y]:
    return partial(f, x)


def let(**_ : a) -> Map[str, a]:
    return Map(_)


def memo(f : Expr[xs, y], /) -> Expr[xs, y]:
    return lru_cache(None, True)(f)


def rec(*fs : Expr[..., a]) -> tuple[Expr[..., a], ...]:
    return (x := (*map(lambda f, /: lambda *_: f(*x, *_), fs),))


def seq(_ : a, x : b, /) -> b:
    return x


def undefined() -> Void:
    assert None, '⊥'
