from datetime import datetime

from app import database
from app.tags.tag_model import Tag
from app.transactions.filter import TagFilter, TransactionFilter
from app.transactions.timeline import TimelineMonth, get_transaction_timeline
from app.transactions.transaction_model import Transaction
from app.config import CONFIG

CONFIG.DATABASE_PATH = CONFIG.MOCK_DATABASE_PATH
database.init()


def setup():
    return [
        Transaction.make(
            date=datetime(2022, 2, 10), amount=10_000, tag=Tag(l1="Income")
        ),
        Transaction.make(
            date=datetime(2022, 2, 10), amount=-2_000, tag=Tag(l1="Bills")
        ),
        Transaction.make(
            date=datetime(2022, 3, 10), amount=10_000, tag=Tag(l1="Income")
        ),
        Transaction.make(date=datetime(2022, 3, 1), amount=-2_000, tag=Tag(l1="Bills")),
        Transaction.make(date=datetime(2022, 3, 1), amount=-4_000, tag=Tag(l1="Bills")),
    ]


class Test_get_transaction_timeline:
    def test_returns_total_over_each_month(self):
        # Given
        transactions = setup()
        for transaction in transactions:
            transaction.insert()

        # When
        result = get_transaction_timeline(TransactionFilter())
        database.clean_mock()

        # Then
        assert result == [
            TimelineMonth(
                amount=-2_000.0,
                month_start_date=datetime(2022, 2, 1).date(),
                l1="Bills",
            ),
            TimelineMonth(
                amount=10_000.0,
                month_start_date=datetime(2022, 2, 1).date(),
                l1="Income",
            ),
            TimelineMonth(
                amount=-6_000.0,
                month_start_date=datetime(2022, 3, 1).date(),
                l1="Bills",
            ),
            TimelineMonth(
                amount=10_000.0,
                month_start_date=datetime(2022, 3, 1).date(),
                l1="Income",
            ),
        ]

    def test_filters_transactions_by_tag(self):
        # Given
        transactions = setup()
        for transaction in transactions:
            transaction.insert()

        # When
        result = get_transaction_timeline(
            TransactionFilter(tags=TagFilter(l1=["Income"]))
        )
        print(result)
        database.clean_mock()

        # Then
        assert result == [
            TimelineMonth(
                amount=10_000.0,
                month_start_date=datetime(2022, 2, 1).date(),
                l1="Income",
            ),
            TimelineMonth(
                amount=10_000.0,
                month_start_date=datetime(2022, 3, 1).date(),
                l1="Income",
            ),
        ]

    def test_filters_transactions_by_date(self):
        # Given
        transactions = setup()
        for transaction in transactions:
            transaction.insert()

        # When
        result = get_transaction_timeline(
            TransactionFilter(date_from=datetime(2022, 3, 1).date())
        )
        print(result)
        database.clean_mock()

        # Then
        assert result == [
            TimelineMonth(
                amount=-6_000.0,
                month_start_date=datetime(2022, 3, 1).date(),
                l1="Bills",
            ),
            TimelineMonth(
                amount=10_000.0,
                month_start_date=datetime(2022, 3, 1).date(),
                l1="Income",
            ),
        ]

    def test_returns_total_over_each_month_without_grouping_by_tag(self):
        # Given
        transactions = setup()
        for transaction in transactions:
            transaction.insert()

        # When
        result = get_transaction_timeline(TransactionFilter(), False)
        database.clean_mock()

        # Then
        assert result == [
            TimelineMonth(
                amount=8_000.0,
                month_start_date=datetime(2022, 2, 1).date(),
                l1=None,
            ),
            TimelineMonth(
                amount=4_000.0,
                month_start_date=datetime(2022, 3, 1).date(),
                l1=None,
            ),
        ]
