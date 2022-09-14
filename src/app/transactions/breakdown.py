from datetime import date
from typing import Tuple
from app import database
from app.util import date as date_util


def get_transaction_amounts_by_tag_level(
    level: int, date_from: date, date_to: date
) -> Tuple[str, int]:
    """Returns a tuple of `(tag_name, amount)` for the given tag level"""
    conditions = []
    if date_from is not None:
        conditions.append(f"date > {date_util.to_integer(date_from)}")

    if date_to is not None:
        conditions.append(f"date < {date_util.to_integer(date_to)}")

    condition = ""
    if len(conditions) != 0:
        condition = "WHERE " + " AND ".join(conditions)

    if level == 1:
        query = f"SELECT SUM(amount) AS amount, l1 FROM transactions {condition} GROUP BY l1 ORDER BY l1"
    elif level == 2:
        query = f"SELECT SUM(amount) AS amount, l1, l2 FROM transactions {condition} GROUP BY l1, l2 ORDER BY l1, l2"
    elif level == 3:
        query = f"SELECT SUM(amount) AS amount, l1, l2, l3 FROM transactions {condition} GROUP BY l1, l2, l3 ORDER BY l1, l2, l3"

    result = database.select(query)
    return [(r[level], r[0]) for r in result]
