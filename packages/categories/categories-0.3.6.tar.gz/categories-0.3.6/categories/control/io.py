from __future__ import annotations

from asyncio import gather
from typing import TypeVar

from categories.type import IO, Lambda

__all__ = (
    'pureIO',
    'bindIO',
    'seqIO',
    'failIO',
    'plusIO',
    'sequenceIO',
)


a = TypeVar('a')

b = TypeVar('b')


def pureIO(x : a, /) -> IO[a]:
    async def action() -> a:
        return x
    return action


def bindIO(m : IO[a], k : Lambda[a, IO[b]], /) -> IO[b]:
    async def action() -> b:
        match await m():
            case x:
                return await k(x)()
        assert None
    return action


def seqIO(m : IO[a], k : IO[b], /) -> IO[b]:
    async def action() -> b:
        match await m():
            case _:
                return await k()
        assert None
    return action


def failIO(x : str, /) -> IO[a]:
    async def action() -> a:
        raise Exception(x)
    return action


def plusIO(m : IO[a], m_ : IO[a], /) -> IO[a]:
    async def action() -> a:
        try:
            return await m()
        except:
            return await m_()
    return action


def sequenceIO(xs : list[IO[a]], /) -> IO[list[a]]:
    async def action() -> list[a]:
        return await gather(*[x() for x in xs])
    return action
