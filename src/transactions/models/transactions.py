"""Various data models for storing transactions.

(C) 2022, TheIthorian, United Kingdom
"""

from dataclasses import dataclass
from datetime import date, datetime
import json

import transactions.database as database


TAG_COLOR_MAP = {
    "Insurance": "xxx",
    "Transfers": "xxx",
    "Appearance": "xxx",
    "Bills": "xxx",
    "Unknown": "xxx",
    "Transport": "xxx",
    "Family": "xxx",
    "Enjoyment": "xxx",
    "Home": "xxx",
    "Savings": "xxx",
    "Repayments": "xxx",
    "One-off or Other": "xxx",
    "Income": "xxx",
}


@dataclass
class Tag:
    """In moneydashboard, a transaction can have up to 3 levels of tags. Increasing levels are more specific."""

    l1: str
    l2: str
    l3: str
    color: str = None

    def __repr__(self) -> str:
        return "<Tag l1: {}, l2: {}, l3: {}>".format(self.l1, self.l2, self.l3)

    def __eq__(self, other):
        return self.l1 == other.l1 and self.l2 == other.l2 and self.l3 == other.l3

    def to_dict(self):
        return {"l1": self.l1, "l2": self.l2, "l3": self.l3}

    def is_in(self, other_tags: list) -> bool:
        """Returns True if the current tag is in a lsit of `other_tags`."""
        for tag in other_tags:
            if self == tag:
                return True
        return False

    def set_color(self):
        self.color = TAG_COLOR_MAP[self.l1] if self.l1 is not None else ""


@dataclass
class Transaction:
    """A transaction as recorded by moneydashboard."""

    account: str
    date: date
    current_description: str
    original_description: str
    amount: int
    tag: Tag
    id: int = None

    def __repr__(self) -> str:
        return "Transaction(id: {}, acccount: {}, date: {}, current_description: {}, original_description: {}, amount: {}, tag: {})".format(
            self.id,
            self.account,
            self.date,
            self.current_description,
            self.original_description,
            self.amount / 100,
            self.tag,
        )

    def __eq__(self, other: "Transaction") -> bool:
        # Ignore tags, as they can be updated
        return (
            self.account == other.account
            and self.date == other.date
            and self.original_description == other.original_description
            and self.amount == other.amount
        )

    def to_dict(self) -> dict[str, any]:
        tag = self.tag.to_dict()
        return {
            "id": self.id,
            "account": self.account,
            "date": int(self.date.strftime()),
            "current_description": self.current_description,
            "original_description": self.original_description,
            "amount": self.amount,
            "l1": tag["l1"],
            "l2": tag["l2"],
            "l3": tag["l3"],
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

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

        self.id = database.insert(query, self.to_dict(), conn)
        return self.id

    @staticmethod
    def from_db(row):
        """To load transaction from database."""
        return Transaction(
            id=row[0],
            account=row[1],
            date=date.fromtimestamp(row[2]),
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
            date=datetime.strptime(row["Date"], "%Y-%m-%d").date(),
            current_description=row["CurrentDescription"],
            original_description=row["OriginalDescription"],
            amount=int(float(row["Amount"]) * 100),
            tag=Tag(row["L1Tag"], row["L2Tag"], row["L3Tag"]),
        )


@dataclass
class TransactionsByTagLevel:
    l1: list[Transaction]
    l2: list[Transaction]
    l3: list[Transaction]

    def __init__(self):
        self.l1 = []
        self.l2 = []
        self.l3 = []

    def __repr__(self) -> str:
        return "<TransactionsByTag l1: {}, l2: {}, l3: {}>".format(
            self.l1, self.l2, self.l3
        )
