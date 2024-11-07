from __future__ import annotations

from dataclasses import dataclass
from itertools import count
from typing import TypeVar

from categories.type import Stream, Yield, typeclass

__all__ = (
    'Bounded',
    'Enum',
    'boundedEnumFrom',
    'boundedEnumFromThen',
)


a = TypeVar('a')


@dataclass(frozen=True)
class Bounded(typeclass[a]):
    '''
    Minimal complete definition
        min, max
    '''

    def min(self, /) -> a: ...

    def max(self, /) -> a: ...


@dataclass(frozen=True)
class Enum(typeclass[a]):
    '''
    Minimal complete definition
        toEnum, fromEnum
    '''

    def succ(self, x : a, /) -> a:
        return self.toEnum(self.fromEnum(x) + 1)

    def pred(self, x : a, /) -> a:
        return self.toEnum(self.fromEnum(x) - 1)

    def toEnum(self, x : int, /) -> a: ...

    def fromEnum(self, x : a, /) -> int: ...

    def enumFrom(self, x : a, /) -> Stream[a]:
        match self.fromEnum(x):
            case x_:
                def stream() -> Yield[a]:
                    yield from map(self.toEnum, count(x_))
                return stream
        assert None

    def enumFromThen(self, x : a, y : a, /) -> Stream[a]:
        match self.fromEnum(x), self.fromEnum(y):
            case x_, y_:
                def stream() -> Yield[a]:
                    yield from map(self.toEnum, count(x_, y_ - x_))
                return stream
        assert None

    def enumFromTo(self, x : a, y : a, /) -> Stream[a]:
        match self.fromEnum(x), self.fromEnum(y):
            case x_, y_:
                def stream() -> Yield[a]:
                    yield from map(self.toEnum, range(x_, y_ + 1))
                return stream
        assert None

    def enumFromThenTo(self, x : a, y : a, z : a, /) -> Stream[a]:
        match self.fromEnum(x), self.fromEnum(y), self.fromEnum(z):
            case x_, y_, z_:
                def stream() -> Yield[a]:
                    yield from map(self.toEnum, range(x_, z_ + 1, y_ - x_))
                return stream
        assert None


def boundedEnumFrom(enum : Enum[a], bounded : Bounded[a], x : a, /) -> Stream[a]:
    match enum.fromEnum(x):
        case x_:
            def stream() -> Yield[a]:
                yield from map(enum.toEnum, range(x_, enum.fromEnum(bounded.max()) + 1))
            return stream
    assert None


def boundedEnumFromThen(enum : Enum[a], bounded : Bounded[a], x : a, y : a, /) -> Stream[a]:
    match enum.fromEnum(x), enum.fromEnum(y):
        case x_, y_ if x_ <= y_:
            match enum.fromEnum(bounded.max()):
                case z_:
                    def stream() -> Yield[a]:
                        yield from map(enum.toEnum, range(x_, z_ + 1, y_ - x_))
                    return stream
        case x_, y_:
            match enum.fromEnum(bounded.min()):
                case z_:
                    def stream() -> Yield[a]:
                        yield from map(enum.toEnum, range(x_, z_ - 1, y_ - x_))
                    return stream
    assert None
