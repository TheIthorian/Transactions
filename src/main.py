from datetime import datetime
from models import Transaction
from reader import read_data
from data import Filter, TagLists, get_all_tags, get_transactions_for_tags, Aggregates
import database


def main():
    _, transactions = read_data()

    # Aggregates
    total_from_income = Aggregates.aggregate(
        transactions, lambda t: t.tag.L1 == "Income", lambda t: t.amount
    )
    total_from_income = Aggregates.aggregate(
        transactions, lambda t: t.tag.L1 == "Income", lambda t: t.amount
    )
    print(total_from_income / 100)

    # Queries
    data = database.select("""SELECT * FROM transactions Order by date desc LIMIT 1""")
    for row in data:
        print(Transaction.from_db(row))
        print()

    # Filters
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
        print()

    for tag in get_all_tags():
        print(tag)

    transactions = get()


if __name__ == "__main__":
    main()
