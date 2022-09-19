import app.http.request as request
import app.transactions.transaction_controller as transactions
from app.transactions.transaction_schema import (
    GetTransactionBreakdownRequestSchema,
    GetTransactionBreakdownResponseSchema,
    GetTransactionTimelineRequestSchema,
    GetTransactionTimelineResponseSchema,
    GetTransactionsRequestSchema,
    GetTransactionsResponseSchema,
)


def register_routes(app):
    @app.route("/getTransactions", methods=["POST"])
    def _get_transactions():
        return request.invoke(
            transactions.get_transactions,
            GetTransactionsRequestSchema(),
            GetTransactionsResponseSchema(many=True),
        )

    @app.route("/getTransactionBreakdown", methods=["POST"])
    def _get_transaction_breakdown():
        return request.invoke(
            transactions.get_transaction_breakdown,
            GetTransactionBreakdownRequestSchema(),
            GetTransactionBreakdownResponseSchema(),
        )

    @app.route("/getAverageTransactionBreakdown", methods=["POST"])
    def _get_average_transaction_breakdown():
        return request.invoke(
            transactions.get_transaction_breakdown_month_average,
            GetTransactionBreakdownRequestSchema(),
            GetTransactionBreakdownResponseSchema(),
        )

    @app.route("/getTransactionTimeline", methods=["POST"])
    def _get_transaction_timeline():
        return request.invoke(
            transactions.get_transaction_timeline,
            GetTransactionTimelineRequestSchema(),
            GetTransactionTimelineResponseSchema(many=True),
        )
