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
    status: str
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
            "status": self.status,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    @staticmethod
    def make(
        file_name: str = None,
        size: int = None,
        date: dt.date = None,
        md5: str = None,
        status: str = None,
        id: int = None,
    ) -> "Upload":
        return Upload(
            file_name=file_name,
            size=size,
            date=date,
            md5=md5,
            status=status,
            id=id,
        )

    def insert(self, conn=None) -> int:
        query = """INSERT INTO uploads (
            filename, 
            size, 
            date, 
            md5,
            status) VALUES 
            (:file_name, 
            :size, 
            :date, 
            :md5,
            :status)"""

        inputs = self.to_dict()
        self.id = database.insert(query, inputs, conn)
        return self.id

    def update(self, conn=None) -> "Upload":
        query = """UPDATE uploads SET
            filename=:file_name, 
            size=:size, 
            date=:date, 
            md5=:md5,
            status=:status
            WHERE upload_id = :id"""

        inputs = self.to_dict()
        database.update(query, inputs, conn)
        return self

    @staticmethod
    def from_db(row):
        """To load upload from database."""
        return Upload(
            id=row[0],
            file_name=row[1],
            size=row[2],
            date=dt.datetime.strptime(row[3], "%Y-%m-%d %H:%M:%S.%f"),
            md5=row[4],
            status=row[5],
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
