import app.http.request as request
import app.budget_item.budget_item_controller as budget_item
from app.budget_item.budget_item_schema import (
    GetBudgetItemsRequestSchema,
    GetBudgetItemsResponseSchema,
    GetBudgetItemResponseSchema,
    GetBudgetItemRequestSchema,
    AddBudgetItemRequestSchema,
    UpdateBudgetItemRequestSchema,
)


def register_routes(app):
    @app.route("/getBudgetItems", methods=["POST"])
    def _get_budget_items():
        return request.invoke(
            budget_item.get_budget_items_for_budget,
            GetBudgetItemsRequestSchema(),
            GetBudgetItemsResponseSchema(many=True),
        )

    @app.route("/getBudgetItem", methods=["POST"])
    def _get_budget_item():
        return request.invoke(
            budget_item.get_budget_item,
            GetBudgetItemRequestSchema(),
            GetBudgetItemResponseSchema(),
        )

    @app.route("/addBudgetItem", methods=["POST"])
    def _add_budget_item():
        return request.invoke(
            budget_item.add_budget_item,
            AddBudgetItemRequestSchema(),
            GetBudgetItemResponseSchema(),
        )

    @app.route("/updateBudgetItem", methods=["POST"])
    def _update_budget_item():
        return request.invoke(
            budget_item.update_budget_item,
            UpdateBudgetItemRequestSchema(),
            GetBudgetItemResponseSchema(),
        )
