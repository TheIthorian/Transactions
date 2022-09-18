from app import database

from app.tags.data import get_all_tags
from app.tags.tag_model import Tag
from app.transactions.transaction_model import Transaction


class Test_get_all_tags:
    def test_returns_all_unique_tags(self):
        # Given
        transactions: list[Transaction] = [
            Transaction.make(tag=Tag(l1="Income", l2="", l3="")),
            Transaction.make(tag=Tag(l1="Income", l2="", l3="")),
            Transaction.make(tag=Tag(l1="Home", l2="Bills", l3="")),
            Transaction.make(tag=Tag(l1="Home", l2="Bills", l3="Other")),
            Transaction.make(tag=Tag(l1="Home", l2="Bills", l3="Other")),
            Transaction.make(tag=Tag(l1="Home", l2="Bills", l3="Other")),
        ]

        database.mock()
        for transaction in transactions:
            transaction.insert()

        # When
        result = get_all_tags()
        database.unmock()

        # Then
        assert result == [
            Tag(l1="Home", l2="Bills", l3=""),
            Tag(l1="Home", l2="Bills", l3="Other"),
            Tag(l1="Income", l2="", l3=""),
        ]
