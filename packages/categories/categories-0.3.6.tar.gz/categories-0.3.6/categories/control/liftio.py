from __future__ import annotations

from dataclasses import dataclass
from typing import TypeVar

from categories.control.monad import Monad, MonadIO
from categories.type import IO, hkt, typeclass

__all__ = (
    'LiftIO',
    'BaseIO',
)


a = TypeVar('a')

m = TypeVar('m')


@dataclass(frozen=True)
class LiftIO(Monad[m], typeclass[m]):
    '''
    Minimal complete definition
        liftIO
    '''

    def liftIO(self, m : IO[a], /) -> hkt[m, a]: ...


@dataclass(frozen=True)
class BaseIO(MonadIO, LiftIO[IO]):
    def liftIO(self, m : IO[a], /) -> IO[a]:
        return m
