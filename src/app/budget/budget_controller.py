from app.http.request import Request, Error
import app.database as database

from app.budget.budget_model import Budget


def get_budgets(request: Request = None):
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
        err = Error(
            "No Resource Found",
            "The budget you are looking for does not exist",
            404,
        )
        request.errors.append(err)
        return

    return Budget.from_db(budget[0])


def add_budget(budget: Budget, request: Request = None):
    budget.insert()
    return budget


def update_budget(budget: Budget, request: Request = None):
    budget.update()
