"""Module to fetch and form data in a useable format.

(C) 2022, TheIthorian, United Kingdom
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Callable, TypeVar
from models import Tag, TransactionsByTagLevel, Transaction
import database


def get_tags(transaction_list: list[Transaction]) -> list[Tag]:
    """Finds all unique tag names in a list of transactions."""
    tags = []
    for transaction in transaction_list:
        tag = transaction.tag
        if not tag.is_in(tags):
            tags.append(tag)

    return tags


def get_all_transactions() -> list[Transaction]:
    """Gets all transactions from the database."""
    transactions = database.select(
        """SELECT rowid, * FROM transactions ORDER BY date desc"""
    )
    return list(map(lambda t: Transaction.from_db(t), transactions))


def get_all_tags() -> list[Tag]:
    """Finds all unique tags in used by any transaction."""
    return get_tags(get_all_transactions())


def group_transaction_by_tag_level(
    transactions: list[Transaction],
) -> TransactionsByTagLevel:
    """Groups each transaction in `transactions` according to their tag level."""
    transactions_by_tag_level = TransactionsByTagLevel()

    for transaction in transactions:
        if transaction.tag.L1 != "":
            transactions_by_tag_level.L1.append(transaction)
        if transaction.tag.L2 != "":
            transactions_by_tag_level.L2.append(transaction)
        if transaction.tag.L3 != "":
            transactions_by_tag_level.L3.append(transaction)

    return transactions_by_tag_level


@dataclass
class TagLists:
    """Datastructure to store lists of tags, separated by tag level."""

    L1: list[str] = None
    L2: list[str] = None
    L3: list[str] = None


def get_transactions_for_tags(tag_lists: TagLists) -> list[Transaction]:
    """Find all transactions that have at least one tag in each of the input `tag_lists` levels.
    \n
    E.g. if `tag_lists => L1=["Income"], L2=["Investments or Shares"], L3=[]`
    then only transactions which match each of the tag levels will be returned, except L3 which will be ignored.
    """

    query = "SELECT rowid, * FROM transactions WHERE"
    conditions = []  # Query consitions
    inputs = []  # Query inputs

    if tag_lists.L1 is not None:
        conditions.append(" l1 IN (%s)" % ",".join("?" for _ in tag_lists.L1))
        inputs.extend(tag_lists.L1)

    if tag_lists.L2 is not None:
        conditions.append(" l2 IN (%s)" % ",".join("?" for _ in tag_lists.L2))
        inputs.extend(tag_lists.L2)

    if tag_lists.L3 is not None:
        conditions.append(" l3 IN (%s)" % ",".join("?" for _ in tag_lists.L3))
        inputs.extend(tag_lists.L3)

    query += " AND".join(conditions) + " ORDER BY date desc"

    transactions = database.select(query, inputs)
    return list(map(lambda t: Transaction.from_db(t), transactions))


class Filter:
    """Collection of filter functions."""

    @staticmethod
    def filter_by_tag(
        transactions: list[Transaction], L1: Tag = None, L2: Tag = None, L3: Tag = None
    ) -> list[Transaction]:
        filter_L1 = lambda _: True
        filter_L2 = lambda _: True
        filter_L3 = lambda _: True

        if L1 is not None:
            filter_L1 = lambda t: t.tag.L1 == L1
        if L2 is not None:
            filter_L2 = lambda t: t.tag.L2 == L2
        if L3 is not None:
            filter_L3 = lambda t: t.tag.L3 == L3

        _filter = lambda t: filter_L1(t) and filter_L2(t) and filter_L3(t)

        return list(filter(_filter, transactions))

    @staticmethod
    def filter_by_date(
        transactions: Transaction, start_date: datetime, end_date: datetime
    ) -> list[Transaction]:
        """Returns the transactions which occurred within `star_date` and `end_date`."""
        return list(
            filter(lambda t: t.date > start_date and t.date < end_date, transactions)
        )

    @staticmethod
    def filter_by_account(transactions, account: str) -> list:
        """Returns the transactions which belong to the input `account` name."""
        return list(filter(lambda t: t.account == account, transactions))


class Aggregate:
    """Collection of aggregate functions."""

    T = TypeVar("T")

    @staticmethod
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
