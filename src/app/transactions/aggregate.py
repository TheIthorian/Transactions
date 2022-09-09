"""Collection of aggregate functions."""

from typing import Callable, TypeVar

from app.transactions.transaction_model import Transaction


T = TypeVar("T")


def aggregate(
    transactions: list[Transaction],
    condition: Callable,
    agg_function: Callable,
    seed: T = 0,
) -> T:
    summary = seed
    for transaction in transactions:
        if condition(transaction):
            summary += agg_function(transaction)

    return summary
