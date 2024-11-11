from cardy import neighbourhood
from utils import test

SORTS = {
    0: ({1, 2, 3}, {4, 5}),
    1: ({1, 2, 3}, {4, 5}, set()),
    2: ({1, 2}, {3}, {4, 5}),
    3: ({1, 2}, {3, 4}, {5}),
    4: ({1, 2, 4}, {3, 5},),
}


@test
def zero_neighbourhoods_only_include_equivalent_card_sorts():
    assert neighbourhood(0, SORTS[0], SORTS) == {0, 1}
    assert neighbourhood(0, SORTS[2], SORTS) == {2}
    assert neighbourhood(0, ({1, 2, 3, 4, 5},), SORTS) == set()


@test
def neighbourhoods_are_returned_when_sorts_have_different_distances():
    assert neighbourhood(1, SORTS[0], SORTS) == {0, 1, 2}
    assert neighbourhood(2, SORTS[0], SORTS) == {0, 1, 2, 3, 4}
    assert neighbourhood(2, ({1, 2, 3, 4, 5},), SORTS) == {0, 1, 4}
    assert neighbourhood(3, ({1, 2, 3, 4, 5},), SORTS) == {0, 1, 2, 3, 4}
