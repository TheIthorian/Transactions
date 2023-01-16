import app.database as database


def select_all_budgets() -> list:
    return database.select(
        "SELECT budget_id, name, total_limit FROM Budget ORDER BY Name, budget_id",
    )


def select_by_id(id) -> list:
    return database.select(
        "SELECT budget_id, name, total_limit FROM Budget WHERE budget_id = :id",
        {"id": id},
    )


def get_tags_not_used_by_budget(budget_id) -> list:
    return database.select(
        """SELECT DISTINCT T.l1 
        FROM transactions T
        WHERE T.l1 NOT IN (SELECT l1 FROM BudgetItem BI WHERE BI.budget_id = :budget_id)
        ORDER BY T.l1
        """,
        {"budget_id": budget_id},
    )
