from typing import Iterable


def unique(sequence: Iterable) -> list:
    seen = set()
    seen_add = seen.add
    return [x for x in sequence if not (x in seen or seen_add(x))]
