"""Functions to update latest data from moneydashboard.

(C) 2022, TheIthorian, United Kingdom
"""

import os

from .data import get_all_transactions
from .database import connect
from .reader import read_data


def add_new_transactions():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(dir_path, "..", "..", "new_Transactions.csv")

    _, transactions = read_data(file_path)

    existing_transactions = get_all_transactions()

    # Only add new transactions
    conn = connect()
    count = 0
    for transaction in transactions:
        if not transaction in existing_transactions:
            transaction.insert(conn)
            count += 1

    conn.commit()
    print(f"{count} new transactions added")


if __name__ == "__main__":
    add_new_transactions()