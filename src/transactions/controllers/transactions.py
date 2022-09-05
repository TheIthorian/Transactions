from dataclasses import dataclass
from datetime import date
from transactions.http.response import Response


@dataclass
class FilterTags:
    l1: list[str] = None
    l2: list[str] = None
    l3: list[str] = None


@dataclass
class TransactionFilter:
    account: date = None
    date_from: date = None
    date_to: date = None
    min_value: float = None
    max_value: float = None
    tags: FilterTags = None


def get_transactions(filter: TransactionFilter) -> Response:
    print(filter.account)
    print(filter.date_from)
    print(filter.date_to)
    print(filter.min_value)
    print(filter.max_value)
    print(filter.tags)
    return [{"id": 10}]
