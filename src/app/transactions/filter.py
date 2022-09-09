"""Collection of filter functions."""

from datetime import date
from app.transactions.transaction_model import Tag, Transaction
from app.transactions.transaction_schema import TransactionFilter


def filter_transactions(transactions: list[Transaction], filter: TransactionFilter):
    filtered_transactions = filter_by_date(
        transactions, start_date=filter.date_from, end_date=filter.date_to
    )
    filtered_transactions = filter_by_account(filtered_transactions, filter.account)
    filtered_transactions = filter_by_value(
        filtered_transactions, filter.min_value, filter.max_value
    )

    return filtered_transactions


def filter_tags_by_l1(tags: list[Tag], l1_value: str):
    return list(filter(lambda t: t.l1 == l1_value, tags))


def filter_tags_by_l2(tags: list[Tag], l2_value: str):
    return list(filter(lambda t: t.l2 == l2_value, tags))


def filter_tags_by_l3(tags: list[Tag], l3_value: str):
    return list(filter(lambda t: t.l3 == l3_value, tags))


def filter_by_tag(
    transactions: list[Transaction], l1: Tag = None, l2: Tag = None, l3: Tag = None
) -> list[Transaction]:
    filter_L1 = lambda _: True
    filter_L2 = lambda _: True
    filter_L3 = lambda _: True

    if l1 is not None:
        filter_L1 = lambda t: t.tag.l1 == l1
    if l2 is not None:
        filter_L2 = lambda t: t.tag.l2 == l2
    if l3 is not None:
        filter_L3 = lambda t: t.tag.l3 == l3

    _filter = lambda t: filter_L1(t) and filter_L2(t) and filter_L3(t)

    return list(filter(_filter, transactions))


def filter_by_date(
    transactions: list[Transaction],
    start_date: date = None,
    end_date: date = None,
) -> list[Transaction]:
    """Returns the transactions which occurred within `star_date` and `end_date`."""
    return list(
        filter(
            lambda t: (start_date is None or t.date >= start_date)
            and (end_date is None or t.date <= end_date),
            transactions,
        )
    )


def filter_by_account(transactions: list[Transaction], account: str = None) -> list:
    """Returns the transactions which belong to the input `account` name."""
    return list(filter(lambda t: account is None or t.account == account, transactions))


def filter_by_value(
    transactions: list[Transaction], min_value: int = None, max_value: int = None
) -> list:
    """Returns the transactions which have their value within the given range."""
    return list(
        filter(
            lambda t: (min_value is None or t.amount >= min_value)
            and (max_value is None or t.amount <= max_value),
            transactions,
        )
    )
