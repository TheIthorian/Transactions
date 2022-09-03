from datetime import datetime
from models import Transaction
from reader import read_data
from data import (
    Filter,
    TagLists,
    get_all_tags,
    get_all_transactions,
    get_tags,
    get_transactions_for_tags,
    Aggregate,
    group_transaction_by_tag_level,
)
import database


def aggregate(transactions: list[Transaction]):
    # Aggregate
    total_from_income = Aggregate.aggregate(
        transactions, lambda t: t.tag.L1 == "Income", lambda t: t.amount
    )
    total_from_income = Aggregate.aggregate(
        transactions, lambda t: t.tag.L1 == "Income", lambda t: t.amount
    )
    print("Aggregate: ", total_from_income / 100)


def queries():
    # Queries
    print("\nQueries: ")
    data = database.select("""SELECT * FROM transactions Order by date desc LIMIT 1""")
    for row in data:
        print(Transaction.from_db(row))


def filters():
    # Filters
    print("\nFilter: ")
    tag_lists = TagLists(["Income"], ["Investments or Shares"], ["Interest income"])
    transactions = get_transactions_for_tags(tag_lists)
    transactions = Filter.filter_by_date(
        transactions,
        datetime.strptime("2019-01-01", "%Y-%m-%d"),
        datetime.strptime("2020-01-01", "%Y-%m-%d"),
    )
    transactions = Filter.filter_by_account(transactions, "123 STUDENT CURRENT ACCOUNT")
    for transaction in transactions:
        print(transaction)


def misc():
    # Misc functions
    print("\nMisc Functions:")
    print("\nget_all_tags:")
    for tag in get_all_tags():
        print(tag)

    print("\nget_all_tags(first 10 transactions)")
    for tag in get_tags(get_all_transactions()[0:10]):
        print(tag)

    print("\ngroup_transaction_by_tag_level(first 10 transactions)")
    groups = group_transaction_by_tag_level(get_all_transactions()[0:10])
    print("L1: ", [transaction.original_description for transaction in groups.L1])
    print("L2: ", [transaction.original_description for transaction in groups.L2])
    print("L3: ", [transaction.original_description for transaction in groups.L3])


def examples():
    """Function to demonstrate functionality."""

    _, transactions = read_data("Transactions.csv")
    aggregate(transactions)
    queries()
    filters()
    misc()
