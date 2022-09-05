from marshmallow import Schema, fields

import transactions.http.request as request
import transactions.controllers.transactions as transactions


class Tags(Schema):
    l1 = fields.String(required=False)
    l2 = fields.String(required=False)
    l3 = fields.String(required=False)


class GetTransactionsRequestSchema(Schema):
    date_from = fields.Date(required=False, allow_none=True)
    date_to = fields.Date(required=False, allow_none=True)
    min_value = fields.Float(required=False, allow_none=True)
    max_value = fields.Float(required=False, allow_none=True)
    tags = fields.Nested(Tags, many=True)

    class Meta:
        ordered = True


class GetTransactionsResponseSchema(Schema):
    id = fields.Integer()
    account = fields.String()
    date = fields.Date()
    current_description = fields.String()
    original_description = fields.String()
    amount = fields.Float()
    tag = Tags()


def register_routes(app):
    # app.add_url_rule("/getTransactions", methods=['POST'])
    @app.route("/getTransactions", methods=["POST"])
    def _get_transactions():
        return request.invoke(
            transactions.get_transactions,
            GetTransactionsRequestSchema(),
            GetTransactionsResponseSchema(many=True),
        )
