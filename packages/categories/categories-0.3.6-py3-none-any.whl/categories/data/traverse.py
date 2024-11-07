from __future__ import annotations

from dataclasses import dataclass
from typing import TypeVar

from categories.control.applicative import Applicative
from categories.data.fold import Fold, FoldList, FoldStream
from categories.data.functor import Functor, FunctorList, FunctorStream
from categories.data.stream import nil, cons
from categories.type import Lambda, Stream, Yield, hkt, typeclass

__all__ = (
    'Traverse',
    'TraverseList',
    'TraverseStream',
)


a = TypeVar('a')

b = TypeVar('b')

f = TypeVar('f')

t = TypeVar('t')


@dataclass(frozen=True)
class Traverse(Functor[t], Fold[t], typeclass[t]):
    '''
    Minimal complete definition
        traverse | sequence
    '''

    def traverse(self, inst : Applicative[f],
                 f : Lambda[a, hkt[f, b]], xs : hkt[t, a], /) -> hkt[f, hkt[t, b]]:
        return self.sequence(inst, self.map(f, xs))

    def sequence(self, inst : Applicative[f],
                 xs : hkt[t, hkt[f, a]], /) -> hkt[f, hkt[t, a]]:
        return self.traverse(inst, lambda x, /: x, xs)


@dataclass(frozen=True)
class TraverseList(FunctorList, FoldList, Traverse[list]):
    def traverse(self, inst : Applicative[f],
                 f : Lambda[a, hkt[f, b]], xs : list[a], /) -> hkt[f, list[b]]:
        def g(x : a, xs : hkt[f, list[b]], /) -> hkt[f, list[b]]:
            return inst.binary(lambda x, xs, /: [x, *xs], f(x), xs)
        return self.foldr(g, inst.pure([]), xs)

    def sequence(self, inst : Applicative[f],
                 xs : list[hkt[f, a]], /) -> hkt[f, list[a]]:
        def f(x : hkt[f, a], xs : hkt[f, list[a]], /) -> hkt[f, list[a]]:
            return inst.binary(lambda x, xs, /: [x, *xs], x, xs)
        return self.foldr(f, inst.pure([]), xs)


@dataclass(frozen=True)
class TraverseStream(FunctorStream, FoldStream, Traverse[Stream]):
    def traverse(self, inst : Applicative[f],
                 f : Lambda[a, hkt[f, b]], xs : Stream[a], /) -> hkt[f, Stream[b]]:
        def g(x : a, xs : hkt[f, Stream[b]], /) -> hkt[f, Stream[b]]:
            return inst.binary(cons, f(x), xs)
        return self.foldr(g, inst.pure(nil), xs)

    def sequence(self, inst : Applicative[f],
                 xs : Stream[hkt[f, a]], /) -> hkt[f, Stream[a]]:
        def f(x : hkt[f, a], xs : hkt[f, Stream[a]], /) -> hkt[f, Stream[a]]:
            return inst.binary(cons, x, xs)
        return self.foldr(f, inst.pure(nil), xs)
