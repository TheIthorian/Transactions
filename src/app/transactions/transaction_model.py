from dataclasses import dataclass
import datetime as dt
import json

import app.database as database
from app.util import date as date_util
from app.util.query_builder import QueryBuilder

from app.tags.tag_model import Tag, TagLists


@dataclass
class Transaction:
    """A transaction as recorded by moneydashboard."""

    account: str
    date: dt.date
    current_description: str
    original_description: str
    amount: int
    tag: Tag
    id: int = None

    def __eq__(self, other: "Transaction") -> bool:
        # Ignore tags, as they can be updated
        return (
            self.account == other.account
            and self.date == other.date
            and self.original_description == other.original_description
            and self.amount == other.amount
        )

    def to_dict(self) -> dict[str, any]:
        tag = self.tag.to_dict()  # consider using asdict for this method
        return {
            "id": self.id,
            "account": self.account,
            "date": self.date,
            "current_description": self.current_description,
            "original_description": self.original_description,
            "amount": self.amount,
            "l1": tag["l1"],
            "l2": tag["l2"],
            "l3": tag["l3"],
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    @staticmethod
    def make(
        account=None,
        date=None,
        current_description=None,
        original_description=None,
        amount=None,
        tag=None,
        id=None,
    ) -> "Transaction":
        return Transaction(
            account=account,
            date=date,
            current_description=current_description,
            original_description=original_description,
            amount=amount,
            tag=tag,
            id=id,
        )

    def insert(self, conn=None) -> int:
        query = """INSERT INTO transactions (
            account, 
            date, 
            current_description, 
            original_description, 
            amount, 
            l1, 
            l2, 
            l3) VALUES 
            (:account, 
            :date, 
            :current_description, 
            :original_description,
            :amount,
            :l1,
            :l2,
            :l3)"""

        inputs = self.to_dict()
        inputs["date"] = date_util.to_integer(self.date)
        self.id = database.insert(query, inputs, conn)
        return self.id

    @staticmethod
    def from_db(row):
        """To load transaction from database."""
        return Transaction(
            id=row[0],
            account=row[1],
            date=dt.date.fromtimestamp(row[2]),
            current_description=row[3],
            original_description=row[4],
            amount=row[5],
            tag=Tag(row[6], row[7], row[8]),
        )

    @staticmethod
    def from_row(row):
        """To load transaction from csv."""
        return Transaction(
            account=row["Account"],
            date=dt.datetime.strptime(row["Date"], "%Y-%m-%d").date(),
            current_description=row["CurrentDescription"],
            original_description=row["OriginalDescription"],
            amount=int(float(row["Amount"]) * 100),
            tag=Tag(row["L1Tag"], row["L2Tag"], row["L3Tag"]),
        )

    @staticmethod
    def get_earliest_transaction() -> "Transaction":
        return Transaction.from_db(
            database.select("SELECT rowid, * FROM Transactions ORDER BY Date LIMIT 1")[
                0
            ]
        )

    @staticmethod
    def get_latest_transaction() -> "Transaction":
        return Transaction.from_db(
            database.select(
                "SELECT rowid, * FROM Transactions ORDER BY Date desc LIMIT 1"
            )[0]
        )


class Query(QueryBuilder):
    def date_from(self, date_from: dt.date) -> "Query":
        if date_from is not None:
            self._conditions.append(f"date >= {date_util.to_integer(date_from)}")
        return self

    def date_to(self, date_to: dt.date) -> "Query":
        if date_to is not None:
            self._conditions.append(f"date <= {date_util.to_integer(date_to)}")
        return self

    def amount_from(self, amount_from: int) -> "Query":
        return self

    def amount_to(self, amount_to: int) -> "Query":
        return self

    def by_tag_list(self, tag_lists: TagLists = None) -> "Query":
        if tag_lists.l1 is not None:
            self._conditions.append(" l1 IN (%s)" % ",".join("?" for _ in tag_lists.l1))
            self._inputs.extend(tag_lists.l1)

        if tag_lists.l2 is not None:
            self._conditions.append(" l2 IN (%s)" % ",".join("?" for _ in tag_lists.l2))
            self._inputs.extend(tag_lists.l2)

        if tag_lists.l3 is not None:
            self._conditions.append(" l3 IN (%s)" % ",".join("?" for _ in tag_lists.l3))
            self._inputs.extend(tag_lists.l3)
        return self

    def by_tag_filter(self, tag_filter=None) -> "Query":
        if tag_filter is None:
            return self

        if tag_filter.l1 is not None:
            self._conditions.append(
                f"l1 IN (%s)" % ",".join("?" for _ in tag_filter.l1)
            )
            self._inputs.extend(tag_filter.l1)

        if tag_filter.l2 is not None:
            self._conditions.append(
                f"l2 IN (%s)" % ",".join("?" for _ in tag_filter.l2)
            )
            self._inputs.extend(tag_filter.l2)

        if tag_filter.l3 is not None:
            self._conditions.append(
                f"l3 IN (%s)" % ",".join("?" for _ in tag_filter.l3)
            )
            self._inputs.extend(tag_filter.l3)

        return self


@dataclass
class TransactionsByTagLevel:
    l1: list[Transaction]
    l2: list[Transaction]
    l3: list[Transaction]

    def __init__(self, l1=[], l2=[], l3=[]):
        self.l1 = l1
        self.l2 = l2
        self.l3 = l3
