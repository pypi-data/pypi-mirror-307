from __future__ import annotations

from typing import TypeVar

from categories.type import Expr, Lambda

__all__ = (
    'fst',
    'snd',
    'curry',
    'uncurry',
    'swap',
)


a = TypeVar('a')

b = TypeVar('b')

c = TypeVar('c')


def fst(z : tuple[a, b], /) -> a:
    match z:
        case (x, _):
            return x
    assert None


def snd(z : tuple[a, b], /) -> b:
    match z:
        case (_, y):
            return y
    assert None


def curry(f : Expr[[a, b], c], /) -> Lambda[a, Lambda[b, c]]:
    return lambda x, /: lambda y, /: f(x, y)


def uncurry(f : Lambda[a, Lambda[b, c]], /) -> Expr[[a, b], c]:
    return lambda x, y, /: f(x)(y)


def swap(z : tuple[a, b], /) -> tuple[b, a]:
    match z:
        case (x, y):
            return (y, x)
    assert None
