# Cardy

> [!NOTE]
> This project is in alpha, significant changes and additions are expected.

Low-level card sorting utilities to compare card sorts — including calculating
edit distances, d-neighbourhoods, and d-cliques of card sorts.

It is recommended to read
[Deibel et al. (2005)](https://doi.org/10.1111/j.1468-0394.2005.00304.x)[^1]
to familiarize yourself with the metrics covered in this library.
In fact, that entie special issue of Expert Systems is excellent reading for
anyone interested in analysing card sorting data.

## Installation

```bash
pip install cardy
```

## Usage

Card sorts are represented as collections of sets of cards: `Colection[Set[T]]`
where each set represents a group.

### Edit Distance

The edit distance between two sorts can be computed with the distance function:

```python
from cardy import distance

sort1 = ({1, 2, 3}, {4, 5, 6}, {7, 8, 9})
sort2 = ({1, 2}, {3, 4}, {5, 6, 7}, {8, 9})

dist = distance(sort1, sort2)
print("Distance:", dist)  # Distance: 3
```

When comparing sorts for equality, assert an edit distance of zero:

```python
if distance(sort1, sort2) == 0:
    ...
```

### Cliques and Neighbourhoods

Cliques and neighbourhoods can be calculated using the `clique`
and `neighbourhood` functions. Given a mapping of sort IDs to card sorts:
`Mapping[K, Collection[Set[T]]]`, a neighbourhood or clique is represented as a
set of IDs: `Set[K]` of card sorts

#### Neighbourhoods

Neighbourhoods are always deterministic:

```python
from cardy import neighbourhood

probe = ({1, 2, 3, 4, 5},)
sorts = {
    0: ({1, 2, 3}, {4, 5}),
    1: ({1, 2, 3}, {4, 5}, set()),
    2: ({1, 2}, {3}, {4, 5}),
    3: ({1, 2}, {3, 4}, {5}),
    4: ({1, 2, 4}, {3, 5}),
}

two_neighbourhood = neighbourhood(2, probe, sorts)
print(f"2-neighbourhood around `{probe}`: {two_neighbourhood}")
# 2-neighbourhood around `({1, 2, 3, 4, 5},)`: {0, 1, 4}
```

#### Cliques

Cliques can be non-deterministic — even when using a greedy strategy (default):

```python
from cardy import clique

probe = ({1, 2}, {3})
sorts = {
    0: ({1}, {2}, {3}),
    1: ({2, 3}, {1}),
    2: ({1, 2, 3},),
}
one_clique = clique(1, probe, sorts)
print(f"1-clique around `{probe}`: {one_clique}")
# 1-clique around `({1, 2}, {3})`: {0, 1}
# OR
# 1-clique around `({1, 2}, {3})`: {1, 2}
```

The clique function allows for various heuristic strategies for selecting
candidate card sorts (via ID). Heuristic functions are of the form:
`(int, Mapping[K, Collection[Set[T]]]) -> K` — that is, a function that takes
a the maximum clique diameter and a key to card sort mapping of viable
candidates, and returns a key of a viable candidate based on some heuristic.

Two heuristic functions have been provided: `random_strategy` and
`greedy_strategy`. `random_strategy` will select a candidate at random.
`greedy_strategy` will select a candidate that reduces the size of the
candidate pool by the smallest amount. In the case two or more candidates
reduce the pool by the same amount, one is selected at random.

This behaviour can be changed by providing a deterministic heuristic function,
or a deterministic `Selector` which provides a select method that picks a
candidate in the case of ambiguity:

```python
from cardy import clique, Selector, greedy_strategy


class MinSelector(Selector):
    def select(self, collection):
        # selects the candidate with the smallest key in case of ties
        # for greedy strategy
        return min(collection)


probe = ({1, 2}, {3})
sorts = {
    0: ({1}, {2}, {3}),
    1: ({2, 3}, {1}),
    2: ({1, 2, 3},),
}
one_clique = clique(
    1,
    probe,
    sorts,
    strategy=lambda d, c: greedy_strategy(d, c, MinSelector())
)
print(f"1-clique around `{probe}`: {one_clique}")
# 1-clique around `({1, 2}, {3})`: {0, 1}
```

Alternatively, a seed can be passed to the base `Selector` constructor.

[^1]: Deibel, K., Anderson, R. and Anderson, R. (2005), Using edit distance
to analyze card sorts. Expert Systems, 22: 129-138.
https://doi.org/10.1111/j.1468-0394.2005.00304.x