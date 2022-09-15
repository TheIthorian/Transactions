"""Module to fetch and form data in a useable format.

(C) 2022, TheIthorian, United Kingdom
"""
from app.tags.tag_model import TagLists
from app.transactions.transaction_model import Tag, TransactionsByTagLevel, Transaction
import app.database as database
from app.util import list as list_util


def get_all_transactions() -> list[Transaction]:
    """Gets all transactions from the database."""
    transactions = database.select(
        "SELECT rowid, * FROM transactions ORDER BY date desc"
    )
    return [Transaction.from_db(t) for t in transactions]


def get_tags_from_transactions(transaction_list: list[Transaction]) -> list[Tag]:
    """Finds all unique tag in a list of transactions."""
    return list_util.unique([transaction.tag for transaction in transaction_list])


def group_transactions_by_tag_level(transactions: list[Transaction]):
    """Groups all transactions by whether they have an l1, l2, or l3 tag"""
    transactions_by_tag_level = TransactionsByTagLevel(
        l1=list(
            filter(lambda t: t.tag.l1 is not None and t.tag.l1 != "", transactions)
        ),
        l2=list(
            filter(lambda t: t.tag.l2 is not None and t.tag.l2 != "", transactions)
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


def get_transactions_for_tags(tag_lists: TagLists = None) -> list[Transaction]:
    """Find all transactions that have at least one tag in each of the input `tag_lists` levels.
    \n
    E.g. if `tag_lists => l1=["Income"], l2=["Investments or Shares"], l3=None`
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
    return [Transaction.from_db(t) for t in transactions]
