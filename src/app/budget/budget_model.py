from dataclasses import dataclass, asdict
import json
import app.database as database


@dataclass
class Budget:
    id: int
    name: str
    total_limit: int

    def __eq__(self, other: "Budget") -> bool:
        return self.name == other.name

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    @staticmethod
    def make(id: int = None, name: str = None, total_limit: int = None) -> "Budget":
        return Budget(id=id, name=name, total_limit=total_limit)

    def insert(self, conn=None) -> int:
        query = (
            """INSERT INTO budget (name, total_limit) VALUES (:name, :total_limit)"""
        )

        inputs = self.to_dict()
        self.id = database.insert(query, inputs, conn)
        return self.id

    def update(self, conn=None):
        query = """UPDATE budget SET name = :name, total_limit = :total_limit WHERE budget_id = :id"""

        inputs = self.to_dict()
        self.id = database.update(query, inputs, conn)
        return self.id

    @staticmethod
    def from_db(row):
        """To load transaction from database."""
        return Budget(
            id=row[0],
            name=row[1],
            total_limit=row[2] / 100,
        )
