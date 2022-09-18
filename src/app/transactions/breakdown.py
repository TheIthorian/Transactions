from typing import Tuple
from app import database
from app.transactions.transaction_model import Query, Transaction
from app.transactions.filter import TransactionFilter
from app.util.date import get_month_difference


def get_transaction_amounts_by_tag_level(
    level: int, filter: TransactionFilter
) -> list[Tuple[str, int]]:
    """Returns a tuple of `(tag_name, amount)` for the given tag level"""
    query_builder = Query()
    condition = (
        query_builder.date_from(filter.date_from)
        .date_to(filter.date_to)
        .by_tag_filter(filter.tags)
        .build()
    )
    inputs = query_builder.get_inputs()

    tag_columns = ", ".join(["l1", "l2", "l3"][0:level])
    query = f"SELECT SUM(amount) AS amount, {tag_columns} FROM transactions {condition} GROUP BY {tag_columns} ORDER BY {tag_columns}"

    result = database.select(query, inputs)
    return [(r[level], r[0]) for r in result]


def get_average_transaction_amounts_by_tag_level(
    level: int, filter: TransactionFilter
) -> list[Tuple[str, int]]:
    """Returns a tuple of `(tag_name, amount)` for the given tag level"""
    amounts = get_transaction_amounts_by_tag_level(level, filter)
    month_count = _get_month_difference(filter)

    averaged_amounts = [
        (amount[0], round(amount[1] / month_count, 0)) for amount in amounts
    ]

    return averaged_amounts


def get_total_amount(filter: TransactionFilter):
    query_builder = Query()
    condition = (
        query_builder.date_from(filter.date_from)
        .date_to(filter.date_to)
        .by_tag_filter(filter.tags)
        .build()
    )

    total = database.select(
        f"SELECT SUM(amount) as amount FROM transactions {condition}",
        query_builder.get_inputs(),
    )[0]

    return total[0]


def get_total_average_amount(filter: TransactionFilter):
    return round(get_total_amount(filter) / _get_month_difference(filter), 0)


def _get_month_difference(filter: TransactionFilter) -> int:
    earliest_date = filter.date_from or Transaction.get_earliest_transaction().date
    latest_date = filter.date_to or Transaction.get_latest_transaction().date

    return get_month_difference(latest_date, earliest_date)
