from __future__ import annotations

from dataclasses import dataclass
from typing import TypeVar

from categories.control.applicative import Applicative, ApplicativeIO, ApplicativeList, ApplicativeStream
from categories.type import IO, Stream, Yield, hkt, typeclass

__all__ = (
    'Alternative',
    'AlternativeIO',
    'AlternativeList',
    'AlternativeStream',
)


a = TypeVar('a')

b = TypeVar('b')

f = TypeVar('f')


@dataclass(frozen=True)
class Alternative(Applicative[f], typeclass[f]):
    '''
    Minimal complete definition
        empty, alt
    '''

    def empty(self, /) -> hkt[f, a]: ...

    def alt(self, x : hkt[f, a], y : hkt[f, a], /) -> hkt[f, a]: ...

    def some(self, v : hkt[f, a], /) -> hkt[f, list[a]]:
        return self.apply(self.map(lambda x, /: lambda xs, /: [x, *xs], v), self.many(v))

    def many(self, v : hkt[f, a], /) -> hkt[f, list[a]]:
        return self.alt(self.some(v), self.pure([]))


@dataclass(frozen=True)
class AlternativeIO(ApplicativeIO, Alternative[IO]):
    def empty(self, /) -> IO[a]:
        async def action() -> a:
            raise Exception
        return action

    def alt(self, m : IO[a], m_ : IO[a], /) -> IO[a]:
        async def action() -> a:
            try:
                return await m()
            except:
                return await m_()
        return action


@dataclass(frozen=True)
class AlternativeList(ApplicativeList, Alternative[list]):
    def empty(self, /) -> list[a]:
        return []

    def alt(self, xs : list[a], ys : list[a], /) -> list[a]:
        return xs + ys


@dataclass(frozen=True)
class AlternativeStream(ApplicativeStream, Alternative[Stream]):
    def empty(self, /) -> Stream[a]:
        def stream() -> Yield[a]:
            yield from []
        return stream

    def alt(self, xs : Stream[a], ys : Stream[a], /) -> Stream[a]:
        def stream() -> Yield[a]:
            yield from xs()
            yield from ys()
        return stream
