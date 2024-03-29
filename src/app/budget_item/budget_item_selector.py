from app import database


def select_item_by_id(id: int, budget_id: int) -> list:
    return database.select(
        """SELECT budget_item_id, budget_id, l1, amount 
        FROM BudgetItem WHERE budget_item_id = :id 
        AND budget_id = :budget_id 
        ORDER BY l1""",
        {"id": id, "budget_id": budget_id},
    )


def select_by_budget_id(budget_id: int) -> list:
    return database.select(
        "SELECT budget_item_id, budget_id, l1, amount FROM BudgetItem WHERE budget_id = :budget_id ORDER BY l1",
        {"budget_id": budget_id},
    )


def budget_item_exists(budget_id: int, l1: int) -> bool:
    existing_budget_items = database.select(
        "SELECT budget_item_id FROM BudgetItem WHERE l1 = :l1 AND budget_id = :budget_id",
        {"l1": l1, "budget_id": budget_id},
    )

    return len(existing_budget_items) > 0


def select_spent_for_budget(month_start: int):
    print(month_start)
    return database.select(
        """SELECT sum(T.amount) / 100 as amount, l1 FROM transactions T 
        WHERE T.date > :month_start
        GROUP BY T.l1""",
        {"month_start": month_start},
    )
