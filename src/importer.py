"""Functions to update latest data from moneydashboard.

(C) 2022, TheIthorian, United Kingdom
"""

from data import get_all_transactions
from database import connect
from models import Transaction
from reader import read_from_file


def add_new_transactions():
    reader = read_from_file("new_Transactions.csv")

    transactions: list[Transaction] = []
    for index, row in enumerate(reader):
        if index > 0:  # Ignore header
            transactions.append(Transaction.from_row(row))

    existing_transactions = get_all_transactions()

    # Only add new transactions
    conn = connect()
    for transaction in transactions:
        if not transaction in existing_transactions:
            transaction.insert(conn)

    conn.commit()
