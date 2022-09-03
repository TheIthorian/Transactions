"""Module to fetch and form data in a useable format.

(C) 2022, TheIthorian, United Kingdom
"""

from models import Tag, TransactionsByTag, Transaction
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
    """Gets all transactions from the database"""
    transactions = database.select("""SELECT * FROM transactions ORDER BY date desc""")
    return list(map(lambda t: Transaction.from_db(t), transactions))


def get_all_tags():
    return get_tags(get_all_transactions())


def get_tags_to_transactions_map(transactions):
    transactions_by_tag = TransactionsByTag()

    for transaction in transactions:
        if transaction.tag.L1 != "":
            transactions_by_tag.L1.append(transaction)
        if transaction.tag.L2 != "":
            transactions_by_tag.L2.append(transaction)
        if transaction.tag.L3 != "":
            transactions_by_tag.L3.append(transaction)

    return transactions_by_tag


class TagLists:
    L1: list[str]
    L2: list[str]
    L3: list[str]

    def __init__(
        self, L1: list[str] = None, L2: list[str] = None, L3: list[str] = None
    ):
        self.L1 = L1
        self.L2 = L2
        self.L3 = L3


def get_transactions_for_tags(tag_lists: TagLists) -> list[Transaction]:
    query = "SELECT * FROM transactions WHERE"
    conditions = []
    inputs = []

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


class Filters:
    @staticmethod
    def filter_by_tag(transactions, L1=None, L2=None, L3=None):
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
    def filter_by_date(transactions, start_date, end_date) -> list:
        return list(
            filter(lambda t: t.date > start_date and t.date < end_date, transactions)
        )

    @staticmethod
    def filter_by_account(transactions, account: str) -> list:
        return list(filter(lambda t: t.account == account, transactions))


class Aggregates:
    def aggregate(transactions: list[Transaction], condition, agg_function, seed=0):
        summary = seed
        for transaction in transactions:
            if condition(transaction):
                summary += agg_function(transaction)

        return summary
