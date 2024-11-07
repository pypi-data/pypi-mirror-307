from __future__ import annotations

from dataclasses import dataclass
from typing import TypeVar

from categories.type import IO, Lambda, Stream, Yield, _, hkt, typeclass

__all__ = (
    'Functor',
    'FunctorIO',
    'FunctorLambda',
    'FunctorList',
    'FunctorStream',
)


a = TypeVar('a')

b = TypeVar('b')

f = TypeVar('f')

r = TypeVar('r')


@dataclass(frozen=True)
class Functor(typeclass[f]):
    '''
    Minimal complete definition
        map
    '''

    def map(self, f : Lambda[a, b], x : hkt[f, a], /) -> hkt[f, b]: ...

    def const(self, x : a, _ : hkt[f, b], /) -> hkt[f, a]:
        return self.map(lambda _, /: x, _)


@dataclass(frozen=True)
class FunctorIO(Functor[IO]):
    def map(self, f : Lambda[a, b], m : IO[a], /) -> IO[b]:
        async def action() -> b:
            match await m():
                case x:
                    return f(x)
            assert None
        return action

    def const(self, x : a, _ : IO[b], /) -> IO[a]:
        async def action() -> a:
            match await _():
                case _:
                    return x
            assert None
        return action


@dataclass(frozen=True)
class FunctorLambda(Functor[Lambda[r, _]]):
    def map(self, f : Lambda[a, b], g : Lambda[r, a], /) -> Lambda[r, b]:
        return lambda x, /: f(g(x))


@dataclass(frozen=True)
class FunctorList(Functor[list]):
    def map(self, f : Lambda[a, b], xs : list[a], /) -> list[b]:
        return [f(x) for x in xs]


@dataclass(frozen=True)
class FunctorStream(Functor[Stream]):
    def map(self, f : Lambda[a, b], xs : Stream[a], /) -> Stream[b]:
        def stream() -> Yield[b]:
            yield from (f(x) for x in xs())
        return stream
