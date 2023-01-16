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
