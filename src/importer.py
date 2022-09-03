"""Functions to update latest data from moneydashboard.

(C) 2022, TheIthorian, United Kingdom
"""

from data import get_all_transactions
from database import connect
from models import Transaction
from reader import read_data


def add_new_transactions():
    _, transactions = read_data("new_Transactions.csv")

    existing_transactions = get_all_transactions()

    # Only add new transactions
    conn = connect()
    for transaction in transactions:
        if not transaction in existing_transactions:
            transaction.insert(conn)

    conn.commit()
