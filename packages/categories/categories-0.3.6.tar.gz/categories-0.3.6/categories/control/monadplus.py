from __future__ import annotations

from dataclasses import dataclass
from typing import TypeVar

from categories.control.alternative import Alternative, AlternativeIO, AlternativeList, AlternativeStream
from categories.control.monad import Monad, MonadIO, MonadList, MonadStream
from categories.type import IO, Stream, hkt, typeclass

__all__ = (
    'MonadPlus',
    'MonadPlusIO',
    'MonadPlusList',
    'MonadPlusStream',
)


a = TypeVar('a')

m = TypeVar('m')


@dataclass(frozen=True)
class MonadPlus(Alternative[m], Monad[m], typeclass[m]):
    '''
    Minimal complete definition
        Nothing
    '''

    def zero(self, /) -> hkt[m, a]:
        return self.empty()

    def plus(self, x : hkt[m, a], y : hkt[m, a], /) -> hkt[m, a]:
        return self.alt(x, y)


@dataclass(frozen=True)
class MonadPlusIO(AlternativeIO, MonadIO, MonadPlus[IO]): ...


@dataclass(frozen=True)
class MonadPlusList(AlternativeList, MonadList, MonadPlus[list]): ...


@dataclass(frozen=True)
class MonadPlusStream(AlternativeStream, MonadStream, MonadPlus[Stream]): ...
