"""Module to fetch and form data in a useable format.

(C) 2022, TheIthorian, United Kingdom
"""
from functools import lru_cache
from dataclasses import dataclass

from app.transactions.transaction_model import Tag, TransactionsByTagLevel, Transaction
import app.database as database


def get_all_transactions() -> list[Transaction]:
    """Gets all transactions from the database."""
    transactions = database.select(
        """SELECT rowid, * FROM transactions ORDER BY date desc"""
    )
    return list(map(lambda t: Transaction.from_db(t), transactions))


def get_tags_from_transactions(transaction_list: list[Transaction]) -> list[Tag]:
    """Finds all unique tag names in a list of transactions."""
    tags = []
    for transaction in transaction_list:
        tag = transaction.tag
        if not tag.is_in(tags):
            tags.append(tag)

    return tags


def group_transactions_by_tag_level(transactions: list[Transaction]):
    """Groups all transactions by whether they have an l1, l2, or l3 tag"""
    transactions_by_tag_level = TransactionsByTagLevel(
        l1=list(
            filter(lambda t: t.tag.l1 is not None and t.tag.l1 != "", transactions)
        ),
        l2=list(
            filter(lambda t: t.tag.l1 is not None and t.tag.l2 != "", transactions)
        ),
        l3=list(
            filter(lambda t: t.tag.l3 is not None and t.tag.l3 != "", transactions)
        ),
    )

    return transactions_by_tag_level


def group_transaction_by_tag_level(
    transactions: list[Transaction],
) -> TransactionsByTagLevel:
    """Groups each transaction in `transactions` according to their tag level."""
    transactions_by_tag_level = TransactionsByTagLevel()

    for transaction in transactions:
        if transaction.tag.l1 != "":
            transactions_by_tag_level.l1.append(transaction)
        if transaction.tag.l2 != "":
            transactions_by_tag_level.l2.append(transaction)
        if transaction.tag.l3 != "":
            transactions_by_tag_level.l3.append(transaction)

    return transactions_by_tag_level


@dataclass
class TagLists:
    """Datastructure to store lists of tags, separated by tag level."""

    l1: list[str] = None
    l2: list[str] = None
    l3: list[str] = None


@lru_cache(1)
def get_all_tags() -> list[Tag]:
    """Finds all unique tags in used by any transaction."""
    query = """SELECT DISTINCT l1, l2, l3 FROM Transactions ORDER BY l1, l2, l3"""
    result = database.select(query)

    return [Tag(l1=row[0], l2=row[1], l3=row[2]) for row in result]


def get_transactions_for_tags(tag_lists: TagLists = None) -> list[Transaction]:
    """Find all transactions that have at least one tag in each of the input `tag_lists` levels.
    \n
    E.g. if `tag_lists => l1=["Income"], l2=["Investments or Shares"], l3=[]`
    then only transactions which match each of the tag levels will be returned, except l3 which will be ignored.
    """

    tag_lists = tag_lists or TagLists()

    query = "SELECT rowid, * FROM transactions "
    conditions = []  # Query consitions
    inputs = []  # Query inputs

    if tag_lists.l1 is not None:
        conditions.append(" l1 IN (%s)" % ",".join("?" for _ in tag_lists.l1))
        inputs.extend(tag_lists.l1)

    if tag_lists.l2 is not None:
        conditions.append(" l2 IN (%s)" % ",".join("?" for _ in tag_lists.l2))
        inputs.extend(tag_lists.l2)

    if tag_lists.l3 is not None:
        conditions.append(" l3 IN (%s)" % ",".join("?" for _ in tag_lists.l3))
        inputs.extend(tag_lists.l3)

    if len(conditions) != 0:
        query += " WHERE " + " AND".join(conditions)

    query += " ORDER BY date desc"

    transactions = database.select(query, inputs)
    return list(map(lambda t: Transaction.from_db(t), transactions))
