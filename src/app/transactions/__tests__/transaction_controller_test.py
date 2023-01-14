from app import database
from app.transactions.transaction_model import Tag, Transaction
from app.transactions import transaction_controller as TC
from app.transactions.transaction_schema import TransactionFilter

from app.transactions import data, filter
from app.config import CONFIG

CONFIG.DATABASE_PATH = CONFIG.MOCK_DATABASE_PATH


calls = []


def call(*args):
    calls.append([args])


class Test_get_transaction_breakdown:
    def test_returns_grouped_tags(self, monkeypatch):
        # given
        res = []

        transactions = [
            Transaction.make(amount=2000, tag=Tag("Income", "", "")),
            Transaction.make(amount=200, tag=Tag("Home", "Bills", "")),
            Transaction.make(amount=100, tag=Tag("Home", "Bills", "Other")),
            Transaction.make(amount=800, tag=Tag("Home", "Rent", "")),
        ]

        def mock_get_transactions_for_tags(*args):
            call(args)
            return transactions

        monkeypatch.setattr(
            data,
            "get_transactions_for_tags",
            lambda _: transactions,
        )

        def mock_filter_transactions(*args):
            call(args)
            return res

        monkeypatch.setattr(
            filter,
            "filter_transactions",
            mock_filter_transactions,
        )

        result = TC.get_transactions(TransactionFilter())
        print(result)
        print(calls)

        # assert result == []
        # assert calls[1] == [transactions]
