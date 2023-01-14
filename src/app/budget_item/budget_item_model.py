from dataclasses import dataclass, asdict
import json
import app.database as database


@dataclass
class BudgetItem:
    id: int
    budget_id: int
    l1: str
    amount: int

    def __eq__(self, other: "BudgetItem") -> bool:
        return self.budget_id == other.budget_id and self.l1 == other.l1

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    @staticmethod
    def make(
        id: int = None, budget_id: int = None, l1: str = None, amount: int = None
    ) -> "BudgetItem":
        return BudgetItem(id=id, budget_id=budget_id, l1=l1, amount=amount)

    def insert(self, conn=None) -> int:
        query = """INSERT INTO BudgetItem (budget_id, l1, amount) VALUES (:budget_id, :l1, :amount)"""

        inputs = self.to_dict()
        self.id = database.insert(query, inputs, conn)
        return self.id

    @staticmethod
    def from_db(row):
        """To load transaction from database."""
        return BudgetItem(
            id=row[0],
            name=row[1],
            l1=row[2],
            amount=row[3],
        )
