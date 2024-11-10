from munkres import Munkres, make_cost_matrix

from .types import CardSort

__all__ = ("distance",)


def distance[T](sort1: CardSort[T], sort2: CardSort[T]) -> int:
    """Computes the edit distance between the two given card sorts."""
    if not sort1 and not sort2:
        return 0

    weights = [
        [len(group1 & group2) for group2 in sort2]
        for group1 in sort1
    ]
    cost_matrix = make_cost_matrix(weights)
    total = sum([
        weights[row][col]
        for row, col in Munkres().compute(cost_matrix)
    ])
    return sum(len(g) for g in sort1) - total
