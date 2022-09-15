from datetime import datetime
from app import database
from app.tags.tag_model import Tag
from app.transactions.breakdown import (
    get_transaction_amounts_by_tag_level,
)
from app.transactions.filter import TransactionFilter
from app.transactions.transaction_model import Transaction

FILTER = TransactionFilter()


class Test_database:
    def test_select(self):
        database.mock()

        transactions = database.select("SELECT * FROM Transactions LIMIT 1")
        print(transactions)

        transaction = Transaction.make(
            account="Test Account",
            date=datetime.now(),
            current_description="Test Description",
            original_description="",
            amount=69,
            tag=Tag(l1="Test", l2="", l3=""),
        )

        transaction.insert()

        transactions = database.select("SELECT * FROM Transactions LIMIT 1")
        print(transactions)

        assert 1 == 2

        database.unmock()


class Test_get_breakdown_by_tag:
    def test_returns_grouped_l1_tags(self, mocker):
        # given
        mock_query_results = [
            [20_000, "Income"],
            [-15_000, "Home"],
            [-7_000, "Appearance"],
            [-2_000, "Enjoyment"],
        ]

        mocker.patch("app.database.select", return_value=mock_query_results)

        result = get_transaction_amounts_by_tag_level(1, FILTER)

        assert result == [
            ("Income", 20_000),
            ("Home", -15_000),
            ("Appearance", -7_000),
            ("Enjoyment", -2_000),
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
