from collections.abc import Callable, Collection, Mapping, Set

__all__ = ("CardSort", "CliqueHeuristic")

type CardSort[T] = Collection[Set[T]]
type CliqueHeuristic[K, T] = \
    Callable[[int, Mapping[K, CardSort[T]]], K]
