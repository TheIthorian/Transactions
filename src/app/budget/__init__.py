import app.http.request as request
import app.budget.budget_controller as budget
from app.budget.budget_schema import (
    GetBudgetResponseSchema,
    GetBudgetsResponseSchema,
    AddBudgetRequestSchema,
)


def register_routes(app):
    @app.route("/getBudget/<int:id>", methods=["POST", "GET"])
    def _get_budget(id):
        return request.invoke(
            lambda request: budget.get_budget(id, request),
            None,
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
