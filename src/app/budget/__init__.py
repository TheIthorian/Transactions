import app.http.request as request
import app.budget.budget_controller as budget
from app.budget.budget_schema import (
    GetBudgetRequestSchema,
    GetBudgetResponseSchema,
    GetBudgetsResponseSchema,
    AddBudgetRequestSchema,
    UpdateBudgetRequestSchema,
)


def register_routes(app):
    @app.route("/getBudget", methods=["POST"])
    def _get_budget():
        return request.invoke(
            budget.get_budget,
            GetBudgetRequestSchema(),
            GetBudgetResponseSchema(),
        )

    @app.route("/getBudgets", methods=["POST", "GET"])
    def _get_budgets():
        return request.invoke(
            budget.get_budgets,
            None,
            GetBudgetsResponseSchema(many=True),
        )

    @app.route("/addBudget", methods=["POST"])
    def _add_budget():
        return request.invoke(
            budget.add_budget,
            AddBudgetRequestSchema(),
            GetBudgetResponseSchema(),
        )

    @app.route("/updateBudget", methods=["POST"])
    def _update_budget():
        return request.invoke(
            budget.update_budget,
            UpdateBudgetRequestSchema(),
            GetBudgetResponseSchema(),
        )
