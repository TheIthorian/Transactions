from datetime import datetime
from transactions.data import get_all_transactions
from transactions.models import Tag, Transaction

# https://www.freblogg.com/pytest-functions-mocking-1


def test_get_tags_correctly_finds_tags():
    pass


def test_get_all_transactions(mocker):
    # Given
    id = 1
    account_name = "account"
    date = int(datetime.now().timestamp())
    current_description = "current_description"
    original_description = "original_description"
    amount = 10
    l1 = "L1"
    l2 = "L2"
    l3 = "L3"

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

    mocker.patch("transactions.database.select", return_value=mock_select_results)

    expected_transaction = Transaction(
        id=1,
        account=account_name,
        date=datetime.fromtimestamp(date),
        current_description=current_description,
        original_description=original_description,
        amount=amount,
        tag=Tag(l1, l2, l3),
    )

    # When
    result = get_all_transactions()
    print(result)
    print(expected_transaction)

    # Then
    assert result == [expected_transaction]
