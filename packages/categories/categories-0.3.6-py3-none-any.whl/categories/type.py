from __future__ import annotations

from builtins import frozenset as Set
from collections.abc import Awaitable as Action, Callable as Expr, Iterator as Yield
from types import MappingProxyType as Map
from typing import Annotated as hkt, Any as _, Generic as forall, NoReturn as Void, Protocol as typeclass, Concatenate as Cons, ParamSpec, TypeVar

__all__ = (
    'Action',
    'Cons',
    'Expr',
    'Fix',
    'IO',
    'Lambda',
    'Map',
    'Null',
    'Set',
    'Stream',
    'Void',
    'Yield',
    '_',
    'forall',
    'hkt',
    'typeclass',
)


a = TypeVar('a')

b = TypeVar('b')

x = ParamSpec('x')

y = TypeVar('y')


Fix = Expr[Cons[Expr[x, y], x], y]

IO = Expr[[], Action[a]]

Lambda = Expr[[a], b]

Null = Expr[[], a]

Stream = Expr[[], Yield[a]]
