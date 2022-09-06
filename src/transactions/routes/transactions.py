import transactions.http.request as request
import transactions.controllers.transactions as transactions
from transactions.schema.transaction_schema import (
    GetAllTagsResponse,
    GetTransactionsRequestSchema,
    GetTransactionsResponseSchema,
)


def register_routes(app):
    @app.route("/getTransactions", methods=["POST"])
    def _get_transactions():
        return (
            request.invoke(
                transactions.get_transactions,
                GetTransactionsRequestSchema(),
                GetTransactionsResponseSchema(many=True),
            ),
        )

    @app.route("/getAllTags", methods=["POST"])
    def _get_all_tags():
        return request.invoke(
            transactions.get_all_tags, None, GetAllTagsResponse(many=True)
        )
