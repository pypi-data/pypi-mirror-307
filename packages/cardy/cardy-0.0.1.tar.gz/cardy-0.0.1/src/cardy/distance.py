from collections.abc import Set

from munkres import Munkres, make_cost_matrix


__all__ = ("CardSort", "edit_distance")


type CardSort = tuple[Set[int], ...]


def edit_distance(sort1: CardSort, sort2: CardSort) -> int:
    if not sort1 and not sort2:
        return 0

    matching_weights = [[] for _ in range(len(sort1))]
    for i, group1 in enumerate(sort1):
        for group2 in sort2:
            intersection = len(group1 & group2)
            matching_weights[i].append(intersection)

    cost_matrix = make_cost_matrix(matching_weights)

    running_sum = 0
    for row, col in Munkres().compute(cost_matrix):
        running_sum += matching_weights[row][col]

    return sum(len(g) for g in sort1) - running_sum
