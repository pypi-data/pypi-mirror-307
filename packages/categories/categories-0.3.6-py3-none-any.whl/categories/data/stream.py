from __future__ import annotations

from builtins import filter as filter_, map as map_, zip as zip_
from functools import reduce
from itertools import accumulate, islice
from typing import TypeVar

from categories.type import Expr, Lambda, Stream, Yield

__all__ = (
    'nil',
    'cons',
    'null',
    'head',
    'tail',
    'uncons',
    'index',
    'append',
    'concat',
    'filter',
    'foldl',
    'foldr',
    'map',
    'scanl',
    'scanr',
    'unfoldr',
    'zip',
)


a = TypeVar('a')

b = TypeVar('b')


def nil() -> Yield[a]:
    yield from []


def cons(x : a, xs : Stream[a], /) -> Stream[a]:
    def stream() -> Yield[a]:
        yield x
        yield from xs()
    return stream


def null(xs : Stream[a], /) -> bool:
    return next(map_(lambda _, /: False, xs()), True)


def head(xs : Stream[a], /) -> a:
    return next(xs())


def tail(xs : Stream[a], /) -> Stream[a]:
    def stream() -> Yield[a]:
        yield from islice(xs(), 1, None)
    return stream


def uncons(xs : Stream[a], /) -> None | tuple[a, Stream[a]]:
    match null(xs):
        case True:
            return None
        case False:
            return (head(xs), tail(xs))
    assert None


def index(n : int, xs : Stream[a], /) -> a:
    return next(islice(xs(), n, None))


def append(xs : Stream[a], ys : Stream[a], /) -> Stream[a]:
    def stream() -> Yield[a]:
        yield from xs()
        yield from ys()
    return stream


def concat(xss : Stream[Stream[a]], /) -> Stream[a]:
    def stream() -> Yield[a]:
        yield from (x for xs in xss() for x in xs())
    return stream


def filter(f : Lambda[a, bool], xs : Stream[a], /) -> Stream[a]:
    def stream() -> Yield[a]:
        yield from filter_(f, xs())
    return stream


def foldl(f : Expr[[b, a], b], z : b, xs : Stream[a], /) -> b:
    return reduce(f, xs(), z)


def foldr(f : Expr[[a, b], b], z : b, xs : Stream[a], /) -> b:
    return reduce(lambda k, x, /: lambda y, /: k(f(x, y)), xs(), lambda z, /: z)(z)


def map(f : Lambda[a, b], xs : Stream[a], /) -> Stream[b]:
    def stream() -> Yield[b]:
        yield from map_(f, xs())
    return stream


def scanl(f : Expr[[b, a], b], z : b, xs : Stream[a], /) -> Stream[b]:
    def stream() -> Yield[b]:
        yield from accumulate(xs(), f, initial=z)
    return stream


def scanr(f : Expr[[a, b], b], z : b, xs : Stream[a], /) -> Stream[b]:
    def stream() -> Yield[b]:
        match null(xs):
            case True:
                yield z
            case False:
                match scanr(f, z, tail(xs)):
                    case ys:
                        yield f(head(xs), head(ys))
                        yield from ys()
    return stream


def unfoldr(f : Lambda[b, None | tuple[a, b]], z : b, /) -> Stream[a]:
    def stream() -> Yield[a]:
        match f(z):
            case None: ...
            case x, y:
                yield x
                yield from unfoldr(f, y)()
    return stream


def zip(xs : Stream[a], ys : Stream[b], /) -> Stream[tuple[a, b]]:
    def stream() -> Yield[tuple[a, b]]:
        yield from zip_(xs(), ys())
    return stream
