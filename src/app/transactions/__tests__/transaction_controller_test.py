from app.transactions.transaction_model import Tag, Transaction, TransactionsByTagLevel
from app.transactions import transaction_controller as TC
from app.transactions.transaction_schema import TransactionFilter


def test_get_transaction_breakdown_returns_grouped_tags(
    mocker,
):

    # given
    transactions = [
        Transaction.make(amount=2000, tag=Tag("Income", "", "")),
        Transaction.make(amount=200, tag=Tag("Home", "Bills", "")),
        Transaction.make(amount=800, tag=Tag("Home", "Rent", "")),
    ]

    mocker.patch(
        "app.data.get_transactions_for_tags",
        return_value=TransactionsByTagLevel(
            l1=[transactions[0], transactions[1], transactions[2]],
            l2=[transactions[1], transactions[2]],
        ),
    )

    result = TC.get_transaction_breakdown(TransactionFilter())

    assert result["datasets"][0] == [tuple("Income", 2000), tuple("Home", 1000)]
    assert result["datasets"][2] == [[], [tuple("Bills", 200), tuple("Rent", 800)]]
