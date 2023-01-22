from app.transactions.data import get_all_transactions
from app.transactions.transaction_model import Transaction

from app.database import connect


def insert_transactions(transactions: list[Transaction]):
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
