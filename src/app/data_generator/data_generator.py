from datetime import date, datetime, timedelta
from random import randint, randrange

import app.database as database
from app.tags.tag_model import Tag
from app.transactions.transaction_model import Transaction
from app.config import CONFIG
from app.data_generator.constants import LOREM_IPSUM

MIN_TRANSACTION_DATE = datetime.strptime("2016-01-01", "%Y-%m-%d")
MAX_TRANSACTION_DATE = datetime.strptime("2022-01-01", "%Y-%m-%d")

MIN_TRANSACTION_AMOUNT = 50
MAX_TRANSACTION_AMOUNT = 50_000


L1_TAGS = ["Income", "Bills", "Savings", "Enjoyment"]
L2_TAGS = ["Regular", "Other", ""]
L3_TAGS = ["Unknown", ""]


def generate_data(transaction_count: int):
    """
    generates and inserts `transaction_count` number of transactions with random data.
    """
    print(f"Generating {transaction_count} transactions...")

    account_name = "Demo account"
    transactions = [
        generate_transaction(account_name) for _ in range(transaction_count)
    ]

    insert_transactions(transactions)


def insert_transactions(transactions: list[Transaction]):
    db = database.Database(CONFIG.DEMO_DATABASE_PATH)
    db.init()
    conn = db.connect()

    print(f"Inserting {len(transactions)} transactions...")
    for transaction in transactions:
        transaction.insert(conn)

    conn.commit()
    conn.close()


def generate_transaction(account_name: str) -> Transaction:
    """
    returns a transaction with random data
    """
    return Transaction.make(
        account=account_name,
        date=generate_date(MIN_TRANSACTION_DATE, MAX_TRANSACTION_DATE),
        original_description=generate_description(),
        amount=generate_amount(MIN_TRANSACTION_AMOUNT, MAX_TRANSACTION_AMOUNT),
        tag=generate_tag(),
    )


def generate_date(start: datetime, end: datetime) -> date:
    """
    returns a random date between two datetime objects.
    """
    delta = end - start
    delta_seconds = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(delta_seconds)
    return (start + timedelta(seconds=random_second)).date()


def generate_description() -> str:
    """
    returns a random sample of lorem ipsum
    """
    lorem_list = LOREM_IPSUM.split(" ")
    lorem_len = len(lorem_list)

    start = randint(0, lorem_len - 2)
    end = randint(start, lorem_len - 1)

    return " ".join(lorem_list[start:end])


def generate_amount(min: int, max: int) -> int:
    """
    Returns a random transaction amount between the provided `min` and `max` values
    """
    return randint(min, max)


def generate_tag() -> Tag:
    """
    Returns a random tag
    """
    return Tag(
        l1=rand_element(L1_TAGS), l2=rand_element(L2_TAGS), l3=rand_element(L3_TAGS)
    )


def rand_element(list: list):
    """
    Returns a random element of a given list
    """
    return list[randint(0, len(list) - 1)]
