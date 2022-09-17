"""Module to show usage examples of existing functions.

(C) 2022, TheIthorian, United Kingdom
"""

from datetime import datetime
import os
from app.config import CONFIG

from app.transactions.transaction_model import Transaction
from app.file_handler.reader import read_data

from app.tags.data import get_all_tags

from app.transactions.data import (
    TagLists,
    get_all_transactions,
    get_tags_from_transactions,
    get_transactions_for_tags,
    group_transactions_by_tag_level,
)
from app.transactions import filter
from app.transactions.aggregate import aggregate
import app.database as database


def aggregate_example(transactions: list[Transaction]):
    # Aggregate
    total_from_income = aggregate(
        transactions, lambda t: t.tag.l1 == "Income", lambda t: t.amount
    )
    print("Aggregate: ", total_from_income / 100)


def queries():
    # Queries
    print("\nQueries: ")
    data = database.select(
        """SELECT rowid, * FROM transactions Order by date desc LIMIT 1"""
    )
    for row in data:
        print(Transaction.from_db(row))


def filters():
    # Filters
    print("\nFilter: ")
    tag_lists = TagLists(["Income"], ["Investments or Shares"], ["Interest income"])
    transactions = get_transactions_for_tags(tag_lists)
    transactions = filter.filter_by_date(
        transactions,
        datetime.strptime("2019-01-01", "%Y-%m-%d").date(),
        datetime.strptime("2020-01-01", "%Y-%m-%d").date(),
    )
    transactions = filter.filter_by_account(transactions, "123 STUDENT CURRENT ACCOUNT")
    for transaction in transactions:
        print(transaction)


def misc():
    # Misc functions
    print("\nMisc Functions:")
    print("\nget_all_tags:")
    for tag in get_all_tags():
        print(tag)

    print("\nget_all_tags(first 10 transactions)")
    for tag in get_tags_from_transactions(get_all_transactions()[0:10]):
        print(tag)

    print("\ngroup_transactions_by_tag_level(first 10 transactions)")
    groups = group_transactions_by_tag_level(get_all_transactions()[0:10])
    print("l1: ", [transaction.original_description for transaction in groups.l1])
    print("l2: ", [transaction.original_description for transaction in groups.l2])
    print("l3: ", [transaction.original_description for transaction in groups.l3])


def examples():
    """Function to demonstrate functionality."""
    file_path = os.path.join(CONFIG.ROOT_DIR, "Transactions.csv")

    _, transactions = read_data(file_path)
    aggregate_example(transactions)
    queries()
    filters()
    misc()


if __name__ == "__main__":
    examples()
