from typing import Tuple
from app import database
from app.transactions import data
from app.transactions.aggregate import aggregate
from app.tags.filter import filter_tags_by_l1
from app.transactions.transaction_model import TransactionsByTagLevel
from app.util.list import unique


def get_transaction_amounts_by_tag_level(level: int) -> Tuple[str, int]:
    """Returns a tuple of `(tag_name, amount)` for the given tag level"""
    if level == 1:
        query = """SELECT SUM(amount) AS amount, l1 FROM transactions GROUP BY l1 ORDER BY l1"""
    elif level == 2:
        query = """SELECT SUM(amount) AS amount, l1, l2 FROM transactions GROUP BY l1, l2 ORDER BY l1, l2"""
    elif level == 3:
        query = """SELECT SUM(amount) AS amount, l1, l2, l3 FROM transactions GROUP BY l1, l2, l3 ORDER BY l1, l2, l3"""

    result = database.select(query)
    return [(r[level], r[0]) for r in result]
