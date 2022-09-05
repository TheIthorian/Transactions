"""Module to fetch and form data in a useable format.

(C) 2022, TheIthorian, United Kingdom
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Callable, TypeVar

from transactions.models.transactions import Tag, TransactionsByTagLevel, Transaction
import transactions.database as database


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


class Filter:
    """Collection of filter functions."""

    @staticmethod
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

    @staticmethod
    def filter_by_date(
        transactions: list[Transaction],
        start_date: datetime = None,
        end_date: datetime = None,
    ) -> list[Transaction]:
        """Returns the transactions which occurred within `star_date` and `end_date`."""
        return list(
            filter(
                lambda t: (start_date is None or t.date > start_date)
                and (end_date is None or t.date < end_date),
                transactions,
            )
        )

    @staticmethod
    def filter_by_account(transactions: list[Transaction], account: str = None) -> list:
        """Returns the transactions which belong to the input `account` name."""
        return list(
            filter(lambda t: account is None or t.account == account, transactions)
        )

    @staticmethod
    def filter_by_value(
        transactions: list[Transaction], min_value: int = None, max_value: int = None
    ) -> list:
        """Returns the transactions which have their value within the given range."""
        return list(
            filter(
                lambda t: (min_value is None or t.amount > min_value)
                and (max_value is None or t.amount < max_value),
                transactions,
            )
        )


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
