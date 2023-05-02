from dataclasses import dataclass
import datetime as dt
import json

import app.database as database
from app.util import date as date_util
from app.util.query_builder import QueryBuilder


@dataclass
class Upload:
    file_name: str
    size: int
    date: dt.date
    md5: str
    id: int = None

    def __eq__(self, other: "Upload") -> bool:
        return self.md5 == other.md5

    def to_dict(self) -> dict[str, any]:
        return {
            "id": self.id,
            "file_name": self.file_name,
            "size": self.size,
            "date": self.date,
            "md5": self.md5,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    @staticmethod
    def make(
        file_name: str = None,
        size: int = None,
        date: dt.date = None,
        md5: str = None,
        id: int = None,
    ) -> "Upload":
        return Upload(
            file_name=file_name,
            size=size,
            date=date,
            md5=md5,
            id=id,
        )

    def insert(self, conn=None) -> int:
        query = """INSERT INTO uploads (
            file_name, 
            size, 
            date, 
            md5) VALUES 
            (:file_name, 
            :size, 
            :date, 
            :md5)"""

        inputs = self.to_dict()
        self.id = database.insert(query, inputs, conn)
        return self.id

    @staticmethod
    def from_db(row):
        """To load upload from database."""
        return Upload(
            id=row[0],
            file_name=row[1],
            size=row[2],
            date=dt.date.fromtimestamp(row[3]),
            md5=row[4],
        )

    @staticmethod
    def from_row(row):
        """To load upload from csv."""
        return Upload(
            file_name=row["Filename"],
            size=row["Size"],
            date=dt.datetime.strptime(row["Date"], "%Y-%m-%d").date(),
            md5=row["Md5"],
        )

    @staticmethod
    def get_earliest_upload() -> "Upload":
        return Upload.from_db(
            database.select("SELECT rowid, * FROM Uploads ORDER BY Date LIMIT 1")[0]
        )

    @staticmethod
    def get_latest_upload() -> "Upload":
        return Upload.from_db(
            database.select("SELECT rowid, * FROM Uploads ORDER BY Date desc LIMIT 1")[
                0
            ]
        )


class Query(QueryBuilder):
    def date_from(self, date_from: dt.date) -> "Query":
        if date_from is not None:
            self._conditions.append(
                f"{self.alias}date >= Date({date_util.to_integer(date_from)})"
            )
        return self

    def date_to(self, date_to: dt.date) -> "Query":
        if date_to is not None:
            self._conditions.append(
                f"{self.alias}date <= Date({date_util.to_integer(date_to)})"
            )
        return self
