from datetime import datetime
from app import database
from app.tags.tag_model import Tag
from app.transactions.breakdown import (
    get_transaction_amounts_by_tag_level,
)
from app.transactions.filter import TransactionFilter
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
    transactions[5].tag.l2 = "Work"

    # Enjoyment
    transactions[6].amount = -2_000
    transactions[6].tag.l1 = "Enjoyment"
    transactions[6].tag.l2 = "Eating out"
    transactions[6].tag.l2 = "Everyday"

    return transactions


class Test_get_breakdown_by_tag:
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

    def test_returns_grouped_l2_tags(self, mocker):
        # given
        mock_query_results = [
            [20_000, "Income", ""],
            [-10_000, "Home", "Bills"],
            [-5_000, "Home", "Other"],
            [-7_000, "Appearance", "Clothes"],
            [-2_000, "Enjoyment", "Eating Out"],
        ]

        mocker.patch("app.database.select", return_value=mock_query_results)

        result = get_transaction_amounts_by_tag_level(2, FILTER)

        assert result == [
            ("", 20_000),
            ("Bills", -10_000),
            ("Other", -5_000),
            ("Clothes", -7_000),
            ("Eating Out", -2_000),
        ]

    def test_returns_grouped_l3_tags(self, mocker):
        # given
        mock_query_results = [
            [20_000, "Income", "", ""],
            [-10_000, "Home", "Bills", ""],
            [-5_000, "Home", "Other", ""],
            [-4_000, "Appearance", "Clothes", "Everyday"],
            [-3_000, "Appearance", "Clothes", "Work"],
            [-2_000, "Enjoyment", "Eating Out", "Everyday"],
        ]

        mocker.patch("app.database.select", return_value=mock_query_results)

        result = get_transaction_amounts_by_tag_level(3, FILTER)

        assert result == [
            ("", 20_000),
            ("", -10_000),
            ("", -5_000),
            ("Everyday", -4_000),
            ("Work", -3_000),
            ("Everyday", -2_000),
        ]
