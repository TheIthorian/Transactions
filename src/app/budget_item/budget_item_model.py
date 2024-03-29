from dataclasses import dataclass, asdict
import json
import app.database as database
from app.tags.tag_model import get_color_for_tag


@dataclass
class BudgetItem:
    id: int
    budget_id: int
    l1: str
    amount: int
    spent: int = 0
    tag_color: str = None

    def __post_init__(self):
        self.tag_color = get_color_for_tag(self.l1)

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
        return self

    def update(self, conn=None) -> "BudgetItem":
        query = """UPDATE BudgetItem SET amount = :amount WHERE budget_item_id = :id AND budget_id = :budget_id"""

        inputs = self.to_dict()
        database.update(query, inputs, conn)
        return self

    def delete(self, conn=None):
        query = """DELETE FROM BudgetItem WHERE budget_item_id = :id AND budget_id = :budget_id"""

        inputs = self.to_dict()
        database.update(query, inputs, conn)
        return self

    def set_spent(self, spent_by_tag: dict):
        self.spent = spent_by_tag[self.l1] if self.l1 in spent_by_tag else 0

    @staticmethod
    def from_db(row):
        """To load transaction from database."""
        return BudgetItem(
            id=row.budget_item_id, budget_id=row.budget_id, l1=row.l1, amount=row.amount
        )
