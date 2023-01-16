from app.http.request import Request, Error
from app.budget.budget_model import Budget
from app.budget.budget_selector import (
    select_by_id,
    select_all_budgets,
    get_tags_not_used_by_budget,
)


def get_budgets(request: Request = None):
    budgets = select_all_budgets()
    return [Budget.from_db(budget) for budget in budgets]


def get_budget(id: int, request: Request = None):
    budgets = select_by_id(id)

    if len(budgets) == 0:
        request.errors.append(resource_not_found_error())
        return

    return Budget.from_db(budgets[0])


def add_budget(budget: Budget, request: Request = None):
    budget.insert()
    return budget


def update_budget(budget: Budget, request: Request = None):
    budgets = select_by_id(id)

    if len(budgets) == 0:
        request.errors.append(resource_not_found_error())
        return

    existing_budget = Budget.from_db(budgets[0])
    existing_budget.name = budget.name
    existing_budget.total_limit = budget.total_limit

    existing_budget.update()
    return existing_budget


def get_available_tags(id: int, request: Request = None):
    budgets = select_by_id(id)

    if len(budgets) == 0:
        request.errors.append(resource_not_found_error())
        return

    tags = get_tags_not_used_by_budget(id)
    return [{"name": row.l1} for row in tags]


def resource_not_found_error():
    return Error(
        "No Resource Found",
        "The budget you are looking for does not exist",
        404,
    )
