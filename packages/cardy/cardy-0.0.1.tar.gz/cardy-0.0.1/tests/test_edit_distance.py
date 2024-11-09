from cardy import edit_distance
from utils import test


@test
def empty_card_sorts_have_a_distance_of_zero():
    assert edit_distance((), ()) == 0


@test
def equivalent_card_sorts_have_an_edit_distance_of_zero():
    assert edit_distance(({1},), ({1},)) == 0
    assert edit_distance(({1}, {2}), ({1}, {2})) == 0
    assert edit_distance(({2}, {1}), ({1}, {2})) == 0
    assert edit_distance(
        ({1, 2, 3}, {4}, {5, 6}),
        ({4}, {1, 2, 3}, {5, 6}),
    ) == 0


@test
def empty_groups_are_ignored_when_computing_distances():
    assert edit_distance(({1}, {2}, set()), ({1}, {2})) == 0
    assert edit_distance(({1}, {2}), ({1}, set(), {2})) == 0


@test
def single_card_displacements_have_an_edit_distance_of_one():
    assert edit_distance(({1, 2}, {3}), ({1}, {2, 3})) == 1
    assert edit_distance(({1}, {2}, {3}), ({1}, {2, 3})) == 1
    assert edit_distance(({1}, {2, 3}), ({1, 2, 3},)) == 1


@test
def distance_between_card_sorts():
    assert edit_distance(
        ({1, 2, 3}, {4, 5, 6}, {7, 8, 9}),
        ({1, 2}, {3, 4}, {5, 6, 7}, {8, 9}),
    ) == 3
