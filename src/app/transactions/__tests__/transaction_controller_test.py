from app.transactions.transaction_model import Tag, Transaction
from app.transactions import transaction_controller as TC
from app.transactions.transaction_schema import TransactionFilter


class Test_get_transaction_breakdown:
    def test_returns_grouped_tags(self, mocker):
        return
        # given
        transactions = [
            Transaction.make(amount=2000, tag=Tag("Income", "", "")),
            Transaction.make(amount=200, tag=Tag("Home", "Bills", "")),
            Transaction.make(amount=100, tag=Tag("Home", "Bills", "Other")),
            Transaction.make(amount=800, tag=Tag("Home", "Rent", "")),
        ]

        mocker.patch(
            "app.transactions.data.get_transactions_for_tags",
            return_value=transactions,
        )

        result = TC.get_transaction_breakdown(TransactionFilter())

        result["datasets"][0] == [("Income", 2000), ("Home", 1100)]
        result["datasets"][1] == [
            ("None", 2000),
            ("Bills", 300),
            ("Rent", 800),
            ("None", 0),
        ]
        # assert result["datasets"][2] == [("None", 2000), ("None") ("Other", 100)]
        # [2000, 0, ]
