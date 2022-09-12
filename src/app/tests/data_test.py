from datetime import datetime
from app.transactions.data import get_all_transactions, group_transactions_by_tag_level
from app.transactions.transaction_model import Tag, Transaction, TransactionsByTagLevel

# https://www.freblogg.com/pytest-functions-mocking-1


def test_get_tags_correctly_finds_tags():
    pass


def test_get_all_transactions(mocker):
    # Given
    transaction_date = datetime(2022, 9, 9)

    id = 1
    account_name = "account"
    date = int(transaction_date.timestamp())
    current_description = "current_description"
    original_description = "original_description"
    amount = 10
    l1 = "l1"
    l2 = "l2"
    l3 = "l3"

    mock_select_results = [
        [
            id,
            account_name,
            date,
            current_description,
            original_description,
            amount,
            l1,
            l2,
            l3,
        ]
    ]

    mocker.patch("app.database.select", return_value=mock_select_results)

    expected_transactions = Transaction(
        id=1,
        account=account_name,
        date=transaction_date.date(),
        current_description=current_description,
        original_description=original_description,
        amount=amount,
        tag=Tag(l1, l2, l3),
    )

    # When
    result = get_all_transactions()
    print(result)
    print(expected_transactions)

    # Then
    assert result[0] == expected_transactions


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
