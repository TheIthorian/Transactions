"""Functions to update latest data from moneydashboard.

(C) 2022, TheIthorian, United Kingdom
"""

import os
from transactions.config import CONFIG
from transactions.data import get_all_transactions
from transactions.database import connect
from transactions.reader import read_data


def add_new_transactions():
    file_path = os.path.join(CONFIG.ROOT_DIR, "new_Transactions.csv")

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
