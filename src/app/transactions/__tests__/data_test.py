from datetime import datetime
from app import database
from app.transactions.data import (
    get_all_transactions,
    get_tags_from_transactions,
    group_transactions_by_tag_level,
)
from app.transactions.transaction_model import Tag, Transaction, TransactionsByTagLevel

# https://www.freblogg.com/pytest-functions-mocking-1


def test_get_tags_correctly_finds_tags():
    pass


class Test_get_all_transactions:
    def test_returns_all_transactions(self):
        # Given
        database.mock()
        transaction_date = datetime(2022, 9, 9)

        transaction = Transaction(
            account="account",
            date=transaction_date.date(),
            current_description="current_description",
            original_description="original_description",
            amount=10,
            tag=Tag("l1", "l2", "l3"),
        )

        transaction.insert()

        # When
        result = get_all_transactions()
        database.unmock()

        # Then
        assert len(result) == 1

        result_transaction = result[0]
        assert result_transaction == transaction
        assert result_transaction.id == 1
        assert result_transaction.account == transaction.account
        assert result_transaction.date == transaction.date
        assert result_transaction.current_description == transaction.current_description
        assert (
            result_transaction.original_description == transaction.original_description
        )
        assert result_transaction.amount == transaction.amount
        assert result_transaction.tag == transaction.tag


class Test_get_tags_from_transactions:
    def test_returns_unique_tags(self):
        # Given
        transactions = [
            Transaction.make(tag=Tag("Income", "", "")),
            Transaction.make(tag=Tag("Income", "", "")),
            Transaction.make(tag=Tag("Home", "Bills", "Other")),
            Transaction.make(tag=Tag("Home", "Bills", "Rent")),
            Transaction.make(tag=Tag("Home", "Bills", "")),
            Transaction.make(tag=Tag("Home", "Bills", "")),
            Transaction.make(tag=Tag("Enjoyment", "Dining", "")),
            Transaction.make(tag=Tag("Enjoyment", "Dining", "Other")),
            Transaction.make(tag=Tag("Enjoyment", "Dining", "Other")),
        ]

        # When
        result = get_tags_from_transactions(transactions)

        # Then
        assert result == [
            Tag("Income", "", ""),
            Tag("Home", "Bills", "Other"),
            Tag("Home", "Bills", "Rent"),
            Tag("Home", "Bills", ""),
            Tag("Enjoyment", "Dining", ""),
            Tag("Enjoyment", "Dining", "Other"),
        ]


class Test_group_transactions_by_tag_level:
    def test_returns_grouped_tags(self):
        # given
        transactions = [
            Transaction.make(amount=2000, tag=Tag("Income", "", "")),
            Transaction.make(amount=200, tag=Tag("Home", "Bills", "")),
            Transaction.make(amount=800, tag=Tag("Home", "Rent", "")),
        ]

        expected_result = TransactionsByTagLevel(
            l1=[transactions[0], transactions[1], transactions[2]],
            l2=[transactions[1], transactions[2]],
        )

        result = group_transactions_by_tag_level(transactions)

        assert expected_result == result
