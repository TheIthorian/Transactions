from app import database


def select_item_by_id(id: int, budget_id: int) -> list:
    return database.select(
        """SELECT budget_item_id, budget_id, l1, amount 
        FROM BudgetItem WHERE budget_item_id = :id 
        AND budget_id = :budget_id 
        ORDER BY l1 desc""",
        {"id": id, "budget_id": budget_id},
    )


def select_by_budget_id(budget_id: int) -> list:
    return database.select(
        "SELECT budget_item_id, budget_id, amount FROM BudgetItem WHERE budget_id = :budget_id ORDER BY 1 desc",
        {"budget_id": budget_id},
    )


def budget_item_exists(budget_id: int, l1: int) -> bool:
    existing_budget_items = database.select(
        "SELECT budget_item_id FROM BudgetItem WHERE l1 = :l1 AND budget_id = :budget_id",
        {"l1": l1, "budget_id": budget_id},
    )

    return len(existing_budget_items) > 0
