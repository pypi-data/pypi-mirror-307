from collections.abc import Mapping

from .distance import distance
from .types import CardSort

__all__ = ("neighbourhood",)


def neighbourhood[K, T](
      d: int,
      probe: CardSort[T],
      sorts: Mapping[K, CardSort[T]],
) -> set[K]:
    """
    Returns the d-neighbourhood of the given probe sort in the sorts iterable.

    The probe sort does not need to be one of the given sorts and will not be
    included in the result if it is not.

    :param d: The max distance neighbourhood elements and the probe
    :param probe: The sort at the centre of the neighbourhood
    :param sorts: A collection of sorts to search for the neighbourhood in
    :return: The d-neighbourhood of the given probe
    """
    return {key for key, sort in sorts.items() if distance(probe, sort) <= d}
