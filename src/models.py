"""Various data models for storing transactions.

(C) 2022, TheIthorian, United Kingdom
"""

from datetime import datetime
import json
import database


class Tag:
    L1: str
    L2: str
    L3: str

    def __init__(self, L1, L2, L3):
        self.L1 = L1
        self.L2 = L2
        self.L3 = L3

    def __repr__(self) -> str:
        return "Tag(L1: {}, L2: {}, L3: {})".format(self.L1, self.L2, self.L3)

    def __eq__(self, other):
        return self.L1 == other.L1 and self.L2 == other.L2 and self.L3 == other.L3

    def to_dict(self):
        return {"L1": self.L1, "L2": self.L2, "L3": self.L3}

    def is_in(self, existing_tags: list) -> bool:
        for tag in existing_tags:
            if self == tag:
                return True
        return False


class Transaction:
    acccount: str
    date: datetime
    current_description: str
    original_description: str
    amount: float
    tag: Tag

    def __init__(
        self,
        account: str,
        date: datetime,
        current_description: str,
        original_description: str,
        amount: int,
        tag: Tag,
    ):
        self.account = account
        self.date = date
        self.current_description = current_description
        self.original_description = original_description
        self.amount = amount
        self.tag = tag

    def __repr__(self) -> str:
        return "Transaction(acccount: {}, date: {}, current_description: {}, original_description: {}, amount: {}, tag: {})".format(
            self.account,
            self.date,
            self.current_description,
            self.original_description,
            self.amount / 100,
            self.tag,
        )

    def to_dict(self):
        tag = self.tag.to_dict()
        return {
            "account": self.account,
            "date": int(self.date.timestamp()),
            "current_description": self.current_description,
            "original_description": self.original_description,
            "amount": self.amount,
            "l1": tag["L1"],
            "l2": tag["L2"],
            "l3": tag["L3"],
        }

    def to_json(self):
        return json.dumps(self.to_dict())

    def insert(self):
        query = """INSERT INTO transactions VALUES 
            (:account, 
            :date, 
            :current_description, 
            :original_description,
            :amount,
            :l1,
            :l2,
            :l3)"""
        database.insert(query, self.to_dict())

    @staticmethod
    def from_db(row):
        return Transaction(
            account=row[0],
            date=datetime.fromtimestamp(row[1]),
            current_description=row[2],
            original_description=row[3],
            amount=row[4],
            tag=Tag(row[5], row[6], row[7]),
        )

    @staticmethod
    def from_row(row):
        return Transaction(
            row["Account"],
            datetime.strptime(row["Date"], "%Y-%m-%d"),
            row["CurrentDescription"],
            row["OriginalDescription"],
            int(float(row["Amount"]) * 100),
            Tag(row["L1Tag"], row["L2Tag"], row["L3Tag"]),
        )


class TransactionsByTagLevel:
    L1: list[Transaction]
    L2: list[Transaction]
    L3: list[Transaction]

    def __init__(self):
        self.L1 = []
        self.L2 = []
        self.L3 = []

    def __repr__(self) -> str:
        return "<TransactionsByTag L1: {}, L2: {}, L3: {}>".format(
            self.L1, self.L2, self.L3
        )
