from typing import Tuple
from app import database
from app.transactions.transaction_model import QueryBuilder
from app.util import date as date_util
from app.transactions.filter import TransactionFilter


def get_transaction_amounts_by_tag_level(
    level: int, filter: TransactionFilter
) -> Tuple[str, int]:
    """Returns a tuple of `(tag_name, amount)` for the given tag level"""
    query_builder = QueryBuilder()
    condition = (
        query_builder.date_from(date_util.to_integer(filter.date_from))
        .date_to(date_util.to_integer(filter.date_to))
        .by_tag_filter(filter.tags)
        .build()
    )
    inputs = query_builder.get_inputs()

    print(condition)

    if level == 1:
        query = f"SELECT SUM(amount) AS amount, l1 FROM transactions {condition} GROUP BY l1 ORDER BY l1"
    elif level == 2:
        query = f"SELECT SUM(amount) AS amount, l1, l2 FROM transactions {condition} GROUP BY l1, l2 ORDER BY l1, l2"
    elif level == 3:
        query = f"SELECT SUM(amount) AS amount, l1, l2, l3 FROM transactions {condition} GROUP BY l1, l2, l3 ORDER BY l1, l2, l3"

    result = database.select(query, inputs)
    return [(r[level], r[0]) for r in result]
