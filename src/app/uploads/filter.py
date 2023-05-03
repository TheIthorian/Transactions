from dataclasses import dataclass
from datetime import date
from app.uploads.upload_model import Query


@dataclass
class UploadFilter:
    date_from: date = None
    date_to: date = None

    def build_query(self) -> Query:
        qb = Query().date_from(self.date_from).date_to(self.date_to)
        return qb
