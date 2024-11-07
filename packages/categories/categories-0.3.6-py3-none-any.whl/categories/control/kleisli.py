from __future__ import annotations

from dataclasses import dataclass
from typing import TypeVar

from categories.control.alternative import Alternative
from categories.control.applicative import Applicative
from categories.control.arrow import Arrow
from categories.control.category import Category
from categories.control.monad import Monad
from categories.control.monadplus import MonadPlus
from categories.data.functor import Functor
from categories.type import Lambda, _, forall, hkt

__all__ = (
    'Kleisli',
    'FunctorKleisli',
    'ApplicativeKleisli',
    'AlternativeKleisli',
    'MonadKleisli',
    'MonadPlusKleisli',
    'CategoryKleisli',
    'ArrowKleisli',
)


a = TypeVar('a')

b = TypeVar('b')

c = TypeVar('c')

d = TypeVar('d')

m = TypeVar('m')


@dataclass(frozen=True)
class Kleisli(forall[m, a, b]):
    kleisli : Lambda[a, hkt[m, b]]


@dataclass(frozen=True)
class FunctorKleisli(Functor[Kleisli[m, a, _]]):
    inst : Functor[m]

    def map(self, f : Lambda[a, b], k : Kleisli[m, a, a], /) -> Kleisli[m, a, b]:
        match self, k:
            case FunctorKleisli(inst), Kleisli(g):
                return Kleisli(lambda x, /: inst.map(f, g(x)))
        assert None


@dataclass(frozen=True)
class ApplicativeKleisli(FunctorKleisli[m, a], Applicative[Kleisli[m, a, _]]):
    inst : Applicative[m]

    def pure(self, x : a, /) -> Kleisli[m, a, a]:
        match self:
            case ApplicativeKleisli(inst):
                return Kleisli(lambda _, /: inst.pure(x))
        assert None

    def apply(self, k : Kleisli[m, a, Lambda[a, b]], k_ : Kleisli[m, a, a], /) -> Kleisli[m, a, b]:
        match self, k, k_:
            case ApplicativeKleisli(inst), Kleisli(f), Kleisli(g):
                return Kleisli(lambda x, /: inst.apply(f(x), g(x)))
        assert None

    def seq(self, k : Kleisli[m, a, a], k_ : Kleisli[m, a, b], /) -> Kleisli[m, a, b]:
        match self, k, k_:
            case ApplicativeKleisli(inst), Kleisli(f), Kleisli(g):
                return Kleisli(lambda x, /: inst.seq(f(x), g(x)))
        assert None


@dataclass(frozen=True)
class AlternativeKleisli(ApplicativeKleisli[m, a], Alternative[Kleisli[m, a, _]]):
    inst : Alternative[m]

    def empty(self, /) -> Kleisli[m, a, a]:
        match self:
            case AlternativeKleisli(inst):
                return Kleisli(lambda _, /: inst.empty())
        assert None

    def alt(self, k : Kleisli[m, a, a], k_ : Kleisli[m, a, a], /) -> Kleisli[m, a, a]:
        match self, k, k_:
            case AlternativeKleisli(inst), Kleisli(f), Kleisli(g):
                return Kleisli(lambda x, /: inst.alt(f(x), g(x)))
        assert None


@dataclass(frozen=True)
class MonadKleisli(ApplicativeKleisli[m, a], Monad[Kleisli[m, a, _]]):
    inst : Monad[m]

    def bind(self, k : Kleisli[m, a, a], k_ : Lambda[a, Kleisli[m, a, b]], /) -> Kleisli[m, a, b]:
        match self, k:
            case MonadKleisli(inst), Kleisli(f):
                return Kleisli(lambda x, /: inst.bind(f(x), lambda y, /: k_(y).kleisli(x)))
        assert None


@dataclass(frozen=True)
class MonadPlusKleisli(AlternativeKleisli[m, a], MonadKleisli[m, a], MonadPlus[Kleisli[m, a, _]]):
    inst : MonadPlus[m]


@dataclass(frozen=True)
class CategoryKleisli(Category[Kleisli[m, _, _]]):
    inst : Monad[m]

    def id(self, /) -> Kleisli[m, a, a]:
        match self:
            case CategoryKleisli(inst):
                return Kleisli(inst.pure)
        assert None

    def o(self, k : Kleisli[m, b, c], k_ : Kleisli[m, a, b], /) -> Kleisli[m, a, c]:
        match self, k, k_:
            case CategoryKleisli(inst), Kleisli(f), Kleisli(g):
                return Kleisli(lambda x, /: inst.bind(g(x), f))
        assert None


@dataclass(frozen=True)
class ArrowKleisli(CategoryKleisli[m], Arrow[Kleisli[m, _, _]]):
    inst : Monad[m]

    def arrow(self, f : Lambda[b, c], /) -> Kleisli[m, b, c]:
        match self:
            case ArrowKleisli(inst):
                return Kleisli(lambda x, /: inst.pure(f(x)))
        assert None

    def first(self, k : Kleisli[m, b, c], /) -> Kleisli[m, tuple[b, d], tuple[c, d]]:
        match self, k:
            case ArrowKleisli(inst), Kleisli(f):
                def g(_ : tuple[b, d], /) -> hkt[m, tuple[c, d]]:
                    match _:
                        case (x, y):
                            return inst.bind(f(x), lambda z, /: inst.pure((z, y)))
                    assert None
                return Kleisli(g)
        assert None

    def second(self, k : Kleisli[m, b, c], /) -> Kleisli[m, tuple[d, b], tuple[d, c]]:
        match self, k:
            case ArrowKleisli(inst), Kleisli(f):
                def g(_ : tuple[d, b], /) -> hkt[m, tuple[d, c]]:
                    match _:
                        case (x, y):
                            return inst.bind(f(y), lambda z, /: inst.pure((x, z)))
                    assert None
                return Kleisli(g)
        assert None
