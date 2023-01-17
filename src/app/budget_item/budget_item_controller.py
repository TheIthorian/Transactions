from app.http.request import Request, Error
from datetime import datetime, date

from app.util import date as date_util

from app.budget_item.budget_item_schema import GetBudgetItemsRequestBody
from app.budget_item.budget_item_model import BudgetItem
from app.budget_item.budget_item_schema import BudgetItemRequestBody
from app.budget_item.budget_item_selector import (
    select_item_by_id,
    select_by_budget_id,
    budget_item_exists,
    select_spent_for_budget,
)


def get_budget_items_for_budget(
    data: GetBudgetItemsRequestBody, request: Request = None
):
    budget_items = select_by_budget_id(data.budget_id)
    budget_items = [BudgetItem.from_db(budget_item) for budget_item in budget_items]
    spent_by_tag = get_spent_by_tag(datetime.today().date())
    for item in budget_items:
        item.set_spent(spent_by_tag)

    return budget_items


def get_budget_item(data: BudgetItemRequestBody, request: Request = None):
    budget_items = select_item_by_id(data.id, data.budget_id)

    if len(budget_items) == 0:
        request.errors.append(item_not_found_error())
        return

    budget_item = BudgetItem.from_db(budget_items[0])
    budget_item.set_spent(get_spent_by_tag(datetime.today().date()))
    return budget_item


def add_budget_item(budget_item: BudgetItem, request: Request = None):
    if budget_item_exists(budget_item.budget_id, budget_item.l1):
        request.errors.append(already_exists_error())
        return

    budget_item.insert().set_spent(get_spent_by_tag(datetime.today().date()))
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


def delete_budget_item(budget_item: BudgetItem, request: Request = None):
    budget_items = select_item_by_id(budget_item.id, budget_item.budget_id)

    if len(budget_items) == 0:
        request.errors.append(item_not_found_error())
        return

    BudgetItem.from_db(budget_items[0]).delete()


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


def get_spent_by_tag(date: date):
    month_start = date.replace(day=1)
    spents_for_tags = select_spent_for_budget(date_util.to_integer(month_start))

    spent_by_tag = {}
    for row in spents_for_tags:
        spent_by_tag[row.l1] = row.amount

    return spent_by_tag
