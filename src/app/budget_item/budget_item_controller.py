from app.http.request import Request, Error
import app.database as database

from app.budget_item.budget_item_model import BudgetItem
from app.budget_item.budget_item_schema import BudgetItemRequestBody
from app.budget_item.budget_item_service import (
    select_item_by_id,
    select_by_budget_id,
    budget_item_exists,
)


def get_budget_items_for_budget(budget_id: int, request: Request = None):
    budget_items = select_by_budget_id(budget_id)
    return [BudgetItem.from_db(budget_item) for budget_item in budget_items]


def get_budget_item(data: BudgetItemRequestBody, request: Request = None):
    budget_items = select_item_by_id(data.id, data.budget_id)

    if len(budget_items) == 0:
        request.errors.append(item_not_found_error())
        return

    return BudgetItem.from_db(budget_items[0])


def add_budget_item(budget_item: BudgetItem, request: Request = None):
    if budget_item_exists(budget_item.budget_id, budget_item.l1):
        request.errors.append(already_exists_error())
        return

    budget_item.insert()
    return budget_item


def update_budget_item(budget_item: BudgetItem, request: Request = None):
    budget_items = select_item_by_id(budget_item.id, budget_item.budget_id)

    if len(budget_items) == 0:
        request.errors.append(item_not_found_error())
        return

    existing_budget_item = BudgetItem.from_db(budget_items[0])
    existing_budget_item.amount = budget_item.amount
    existing_budget_item.update()
    return existing_budget_item


def already_exists_error():
    return Error(
        "Already exists",
        "The budget for this tag already exists",
        400,
    )


def item_not_found_error():
    return Error(
        "No Resource Found",
        "The budget item you are looking for does not exist",
        404,
    )
