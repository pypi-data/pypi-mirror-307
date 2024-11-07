from __future__ import annotations

from dataclasses import dataclass

__all__ = (
    'Nat',
    'Zero',
    'Succ',
)


@dataclass(frozen=True)
class Zero: ...


@dataclass(frozen=True)
class Succ: n : Nat


Nat = Zero | Succ
