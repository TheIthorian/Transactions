"""Various data models for storing transactions.

(C) 2022, TheIthorian, United Kingdom
"""

from dataclasses import asdict, dataclass
from datetime import date, datetime
import json

import app.database as database


TAG_COLOR_MAP = {
    "Insurance": "orange",
    "Transfers": "cyan",
    "Appearance": "cyan",
    "Bills": "green",
    "Unknown": "gray",
    "Transport": "blue",
    "Family": "purple",
    "Enjoyment": "magenta",
    "Home": "green",
    "Savings": "magenta",
    "Repayments": "cyan",
    "One-off or Other": "geekblue",
    "Income": "lime",
}


@dataclass
class Tag:
    """In moneydashboard, a transaction can have up to 3 levels of tags. Increasing levels are more specific."""

    l1: str
    l2: str
    l3: str
    color: str = None

    def __init__(self, l1, l2, l3):
        self.l1 = l1
        self.l2 = l2
        self.l3 = l3
        self.color = TAG_COLOR_MAP[self.l1] if self.l1 in TAG_COLOR_MAP else None

    def __eq__(self, other: "Tag"):
        return self.l1 == other.l1 and self.l2 == other.l2 and self.l3 == other.l3

    def to_dict(self):
        return asdict(self)

    def is_in(self, other_tags: list) -> bool:
        """Returns True if the current tag is in a lsit of `other_tags`."""
        for tag in other_tags:
            if self == tag:
                return True
        return False


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
            # "date": int(self.date.strftime()),
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

    def __init__(self, l1=[], l2=[], l3=[]):
        self.l1 = l1
        self.l2 = l2
        self.l3 = l3
