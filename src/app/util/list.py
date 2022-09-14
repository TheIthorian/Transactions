import collections
from typing import Iterable


def unique(sequence: Iterable) -> list:
    if len(sequence) == 0:
        return []

    if isinstance(sequence[0], collections.Hashable):
        return unique_with_set(sequence)

    return unique_without_set(sequence)


def unique_with_set(sequence: Iterable) -> list:
    seen = set()
    seen_add = seen.add
    return [x for x in sequence if not (x in seen or seen_add(x))]


def unique_without_set(sequence: Iterable) -> list:
    seen = []
    return [x for x in sequence if not (x in seen or seen.append(x))]
