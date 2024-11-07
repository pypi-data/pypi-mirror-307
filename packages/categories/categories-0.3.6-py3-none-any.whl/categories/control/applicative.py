from __future__ import annotations

from dataclasses import dataclass
from typing import TypeVar

from categories.data.functor import Functor, FunctorIO, FunctorLambda, FunctorList, FunctorStream
from categories.type import Expr, IO, Lambda, Stream, Yield, _, hkt, typeclass

__all__ = (
    'Applicative',
    'ApplicativeIO',
    'ApplicativeLambda',
    'ApplicativeList',
    'ApplicativeStream',
)


a = TypeVar('a')

b = TypeVar('b')

c = TypeVar('c')

f = TypeVar('f')

r = TypeVar('r')


@dataclass(frozen=True)
class Applicative(Functor[f], typeclass[f]):
    '''
    Minimal complete definition
        pure, (apply | binary)
    '''

    def pure(self, x : a, /) -> hkt[f, a]: ...

    def apply(self, f : hkt[f, Lambda[a, b]], x : hkt[f, a], /) -> hkt[f, b]:
        return self.binary(lambda f, x, /: f(x), f, x)

    def binary(self, f : Expr[[a, b], c], x : hkt[f, a], y : hkt[f, b], /) -> hkt[f, c]:
        return self.apply(self.map(lambda x, /: lambda y, /: f(x, y), x), y)

    def seq(self, _ : hkt[f, a], x : hkt[f, b], /) -> hkt[f, b]:
        return self.apply(self.const(lambda x, /: x, _), x)


@dataclass(frozen=True)
class ApplicativeIO(FunctorIO, Applicative[IO]):
    def pure(self, x : a, /) -> IO[a]:
        async def action() -> a:
            return x
        return action

    def apply(self, m : IO[Lambda[a, b]], m_ : IO[a], /) -> IO[b]:
        async def action() -> b:
            match await m(), await m_():
                case f, x:
                    return f(x)
            assert None
        return action

    def binary(self, f : Expr[[a, b], c], m : IO[a], m_ : IO[b], /) -> IO[c]:
        async def action() -> c:
            match await m(), await m_():
                case x, y:
                    return f(x, y)
            assert None
        return action

    def seq(self, m : IO[a], k : IO[b], /) -> IO[b]:
        async def action() -> b:
            match await m():
                case _:
                    return await k()
            assert None
        return action


@dataclass(frozen=True)
class ApplicativeLambda(FunctorLambda[r], Applicative[Lambda[r, _]]):
    def pure(self, x : a, /) -> Lambda[r, a]:
        return lambda _, /: x

    def apply(self, f : Lambda[r, Lambda[a, b]], g : Lambda[r, a], /) -> Lambda[r, b]:
        return lambda x, /: f(x)(g(x))

    def binary(self, f : Expr[[a, b], c], g : Lambda[r, a], h : Lambda[r, b], /) -> Lambda[r, c]:
        return lambda x, /: f(g(x), h(x))


@dataclass(frozen=True)
class ApplicativeList(FunctorList, Applicative[list]):
    def pure(self, x : a, /) -> list[a]:
        return [x]

    def apply(self, fs : list[Lambda[a, b]], xs : list[a], /) -> list[b]:
        return [f(x) for f in fs for x in xs]

    def binary(self, f : Expr[[a, b], c], xs : list[a], ys : list[b], /) -> list[c]:
        return [f(x, y) for x in xs for y in ys]

    def seq(self, xs : list[a], ys : list[b], /) -> list[b]:
        return [y for _ in xs for y in ys]


@dataclass(frozen=True)
class ApplicativeStream(FunctorStream, Applicative[Stream]):
    def pure(self, x : a, /) -> Stream[a]:
        def stream() -> Yield[a]:
            yield x
        return stream

    def apply(self, fs : Stream[Lambda[a, b]], xs : Stream[a], /) -> Stream[b]:
        def stream() -> Yield[b]:
            yield from (f(x) for f in fs() for x in xs())
        return stream

    def binary(self, f : Expr[[a, b], c], xs : Stream[a], ys : Stream[b], /) -> Stream[c]:
        def stream() -> Yield[c]:
            yield from (f(x, y) for x in xs() for y in ys())
        return stream

    def seq(self, xs : Stream[a], ys : Stream[b], /) -> Stream[b]:
        def stream() -> Yield[b]:
            yield from (y for _ in xs() for y in ys())
        return stream
