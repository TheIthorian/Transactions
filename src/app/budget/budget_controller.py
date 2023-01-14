from app.http.request import Request, Error
import app.database as database

from app.budget.budget_model import Budget


def get_budgets():
    budgets = database.select(
        "SELECT budget_id, name, total_limit FROM Budget ORDER BY Name desc",
    )
    return [Budget.from_db(budget) for budget in budgets]


def get_budget(id: int, request: Request = None):
    budget = database.select(
        "SELECT budget_id, name, total_limit FROM Budget WHERE budget_id = :id",
        {"id": id},
    )

    if len(budget) == 0:
        request.errors.append(
            Error(
                "No Resource Found",
                "The budget you are looking for does not exist",
                404,
            )
        )
        return

    return Budget.from_db(budget)


def add_budget(budget: Budget, request: Request = None):
    budget.total_limit = budget.total_limit * 100
    budget.insert()
    return budget


def update_budget(budget: Budget, request: Request = None):
    budget.update()
