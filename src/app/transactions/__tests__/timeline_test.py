from datetime import datetime

from app import database
from app.tags.tag_model import Tag
from app.transactions.filter import TransactionFilter
from app.transactions.timeline import get_transaction_timeline
from app.transactions.transaction_model import Transaction


class Test_get_transaction_timeline:
    def test_returns_total_out_and_in_over_each_month(self):
        # Given
        database.mock()

        transactions = [
            Transaction.make(
                date=datetime(2022, 2, 10), amount=10_000, tag=Tag(l1="Income")
            ),
            Transaction.make(
                date=datetime(2022, 2, 10), amount=-2_000, tag=Tag(l1="Bills")
            ),
            Transaction.make(
                date=datetime(2022, 2, 10), amount=10_000, tag=Tag(l1="Income")
            ),
            Transaction.make(
                date=datetime(2022, 3, 1), amount=-2_000, tag=Tag(l1="Bills")
            ),
            Transaction.make(
                date=datetime(2022, 3, 1), amount=-4_000, tag=Tag(l1="Bills")
            ),
        ]

        for transaction in transactions:
            transaction.insert()

        result = get_transaction_timeline(TransactionFilter())

        assert result == []

        database.unmock()
