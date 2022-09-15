from datetime import datetime

from app import database
from app.tags.tag_model import Tag
from app.transactions.transaction_model import Transaction
from app.util import date as date_util

account = "test account name"
date = datetime(2022, 1, 1).date()
current_description = "current description"
original_description = "original description"
amount = 100
tag = Tag(l1="l1_tag", l2="l2_tag", l3="l3_tag")
id = None


def make_transaction():
    return Transaction(
        account=account,
        date=date,
        current_description=current_description,
        original_description=original_description,
        amount=amount,
        tag=tag,
        id=1,
    )


class Test_Transaction_eq:
    def test_transaction_equality(self):
        transaction1 = make_transaction()
        transaction2 = make_transaction()

        assert transaction1 == transaction2

        transaction1 = make_transaction()
        transaction1.date = datetime(2022, 1, 2)
        assert transaction1 != transaction2

        transaction1 = make_transaction()
        transaction1.original_description = "different desc"
        assert transaction1 != transaction2

        transaction1.amount = 101
        assert transaction1 != transaction2

        transaction1 = make_transaction()
        transaction1.current_description = "different desc"
        assert transaction1 == transaction2

        transaction1 = make_transaction()
        transaction1.tag = Tag(None, None, None)
        assert transaction1 == transaction2

        transaction1 = make_transaction()
        transaction1.id = 2
        assert transaction1 == transaction2


class Test_Transaction_to_dict:
    def test_returns_correct_dict(self):
        transaction = make_transaction()

        assert transaction.to_dict() == {
            "id": 1,
            "account": account,
            "date": date,
            "current_description": current_description,
            "original_description": original_description,
            "amount": amount,
            "l1": "l1_tag",
            "l2": "l2_tag",
            "l3": "l3_tag",
        }


class Test_insert:
    def test_inserts_correctly_to_database(self):
        database.mock()

        transaction = make_transaction()
        transaction.insert()

        transaction_rows = database.select("SELECT * FROM Transactions")

        assert len(transaction_rows) == 1
        row = transaction_rows[0]

        assert row[0] == account
        assert row[1] == date_util.to_integer(date)
        assert row[2] == current_description
        assert row[3] == original_description
        assert row[4] == amount
        assert row[5] == "l1_tag"
        assert row[6] == "l2_tag"
        assert row[7] == "l3_tag"

        database.unmock()


class Test_from_db:
    def test_creates_Transaction_from_database_row(self):

        database.mock()

        transaction = make_transaction()
        transaction.insert()

        [transaction_row] = database.select("SELECT rowid, * FROM Transactions")

        print(transaction_row)

        new_transaction = Transaction.from_db(transaction_row)

        assert new_transaction.account == transaction.account
        assert new_transaction.date == transaction.date
        assert new_transaction.current_description == transaction.current_description
        assert new_transaction.original_description == transaction.original_description
        assert new_transaction.amount == transaction.amount
        assert new_transaction.tag == transaction.tag
        assert new_transaction.id == 1  # Id is generated by rowid


class Test_from_row:
    def test_returns_Transaction_from_csv_row(self):
        csv_row = {
            "Account": account,
            "Date": "2022-01-01",
            "CurrentDescription": current_description,
            "OriginalDescription": original_description,
            "Amount": "1.0",
            "L1Tag": "l1_tag",
            "L2Tag": "l2_tag",
            "L3Tag": "l3_tag",
        }

        transaction = Transaction.from_row(csv_row)

        assert transaction.account == account
        assert transaction.date == date
        assert transaction.current_description == current_description
        assert transaction.original_description == original_description
        assert transaction.amount == amount
        assert transaction.tag == tag
        assert transaction.id == None  # Id is generated by rowid
