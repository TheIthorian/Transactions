"""Functions to update latest data from moneydashboard."""

import os
from app.config import CONFIG
from app.transactions.data import get_all_transactions
from app.database import connect
from app.file_handler.reader import read_data


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
