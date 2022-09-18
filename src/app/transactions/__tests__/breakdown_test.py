from datetime import datetime
from app import database
from app.tags.tag_model import Tag
from app.transactions.breakdown import (
    get_average_transaction_amounts_by_tag_level,
    get_transaction_amounts_by_tag_level,
)
from app.transactions.filter import TagFilter, TransactionFilter
from app.transactions.transaction_model import Transaction

FILTER = TransactionFilter()


def make_transaction():
    account = "test account name"
    date = datetime(2022, 1, 1).date()
    current_description = "current description"
    original_description = "original description"
    amount = 0

    return Transaction(
        account=account,
        date=date,
        current_description=current_description,
        original_description=original_description,
        amount=amount,
        tag=Tag(l1="", l2="", l3=""),
    )


def setup():
    transactions = [make_transaction() for _ in range(7)]

    # Income
    transactions[0].amount = 10_000
    transactions[0].tag.l1 = "Income"

    transactions[1].amount = 10_000
    transactions[1].tag.l1 = "Income"

    # Home
    transactions[2].amount = -10_000
    transactions[2].tag.l1 = "Home"
    transactions[2].tag.l2 = "Bills"

    transactions[3].amount = -5_000
    transactions[3].tag.l1 = "Home"
    transactions[3].tag.l2 = "Other"

    # Appearance
    transactions[4].amount = -4_000
    transactions[4].tag.l1 = "Appearance"
    transactions[4].tag.l2 = "Clothes"
    transactions[4].tag.l3 = "Everyday"

    transactions[5].amount = -3_000
    transactions[5].tag.l1 = "Appearance"
    transactions[5].tag.l2 = "Clothes"
    transactions[5].tag.l3 = "Work"

    # Enjoyment
    transactions[6].amount = -2_000
    transactions[6].tag.l1 = "Enjoyment"
    transactions[6].tag.l2 = "Eating out"
    transactions[6].tag.l3 = "Everyday"

    return transactions


class Test_get_breakdown_by_tag_level:
    def test_returns_grouped_l1_tags(self):
        database.mock()

        # Given
        transactions = setup()
        for transaction in transactions:
            transaction.insert()

        # When
        result = get_transaction_amounts_by_tag_level(1, FILTER)
        database.unmock()

        # Then
        assert result == [
            ("Appearance", -7_000.0),
            ("Enjoyment", -2_000.0),
            ("Home", -15_000.0),
            ("Income", 20_000.0),
        ]

    def test_returns_grouped_l2_tags(self):
        database.mock()

        # Given
        transactions = setup()
        for transaction in transactions:
            transaction.insert()

        # When
        result = get_transaction_amounts_by_tag_level(2, FILTER)
        database.unmock()

        # Then
        assert result == [
            ("Clothes", -7_000.0),
            ("Eating out", -2_000.0),
            ("Bills", -10_000.0),
            ("Other", -5_000.0),
            ("", 20_000.0),
        ]

    def test_returns_grouped_l3_tags(self):
        database.mock()

        # Given
        transactions = setup()
        for transaction in transactions:
            transaction.insert()

        # When
        result = get_transaction_amounts_by_tag_level(3, FILTER)
        database.unmock()

        # Then
        assert result == [
            ("Everyday", -4_000.0),
            ("Work", -3_000.0),
            ("Everyday", -2_000.0),
            ("", -10_000.0),
            ("", -5_000.0),
            ("", 20_000.0),
        ]

    def test_only_sums_transactions_with_correct_tags(self):
        # Given
        transactions = setup()[0:5]
        transactions[0].amount = 10_000
        transactions[0].tag.l1 = "Income"

        transactions[1].amount = 10_000
        transactions[1].tag.l1 = "Income"

        transactions[2].amount = 5_000
        transactions[2].tag.l1 = "Appearance"
        transactions[2].tag.l2 = "Other"

        transactions[3].amount = 6_000
        transactions[3].tag.l1 = "Home"
        transactions[3].tag.l2 = "Other"

        transactions[4].amount = 3_000
        transactions[4].tag.l1 = "Home"
        transactions[4].tag.l2 = "Bills"

        filter = TransactionFilter(tags=TagFilter(l1=["Home"], l2=["Other"]))

        database.mock()
        for transaction in transactions:
            transaction.insert()

        # When
        result = get_transaction_amounts_by_tag_level(1, filter)
        database.unmock()

        # Then
        assert result == [("Home", 6_000.0)]

    def test_filters_transactions_by_date(self):
        # Given
        transactions = setup()[0:3]
        transactions[0].date = datetime(2022, 1, 10).date()
        transactions[0].amount = 10_000
        transactions[0].tag.l1 = "Income"

        transactions[1].date = datetime(2022, 1, 15).date()
        transactions[1].amount = 10_000
        transactions[1].tag.l1 = "Income"

        transactions[2].date = datetime(2022, 1, 5).date()
        transactions[2].amount = 5_000
        transactions[2].tag.l1 = "Appearance"

        filter = TransactionFilter(
            date_from=datetime(2022, 1, 8).date(), date_to=datetime(2022, 1, 13).date()
        )

        database.mock()
        for transaction in transactions:
            transaction.insert()

        # When
        result = get_transaction_amounts_by_tag_level(1, filter)
        database.unmock()

        # Then
        assert result == [("Income", 10_000.0)]


class Test_get_average_transaction_amounts_by_tag_level:
    def test_returns_average_amount_over_a_month(self):
        # Given
        database.mock()
        transactions = setup()
        for transaction in transactions:
            transaction.insert()

        # When
        result = get_average_transaction_amounts_by_tag_level(
            1,
            TransactionFilter(
                date_from=datetime(2022, 1, 1).date(),
                date_to=datetime(2022, 4, 1).date(),
            ),
        )
        database.unmock()

        print(result)

        # Then
        assert result == [
            ("Appearance", -2366.0),
            ("Enjoyment", -676.0),
            ("Home", -5069.0),
            ("Income", 6759.0),
        ]
