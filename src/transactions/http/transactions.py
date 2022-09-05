from marshmallow import Schema, fields, post_load

import transactions.http.request as request
import transactions.controllers.transactions as transactions


class Tags(Schema):
    l1 = fields.String(required=False)
    l2 = fields.String(required=False)
    l3 = fields.String(required=False)

    @post_load
    def make_tag(self, data):
        return transactions.FilterTags(**data)


class GetTransactionsRequestSchema(Schema):
    account = fields.String(required=False, allow_none=True)
    date_from = fields.Date(required=False, allow_none=True)
    date_to = fields.Date(required=False, allow_none=True)
    min_value = fields.Float(required=False, allow_none=True)
    max_value = fields.Float(required=False, allow_none=True)
    tags = fields.Nested(Tags, many=True)

    class Meta:
        ordered = True

    @post_load
    def make_filter(self, data, **kwargs):
        return transactions.TransactionFilter(**data)


class GetTransactionsResponseSchema(Schema):
    id = fields.Integer()
    account = fields.String()
    date = fields.Date()
    current_description = fields.String()
    original_description = fields.String()
    amount = fields.Float()
    tag = Tags()


def register_routes(app):
    @app.route("/getTransactions", methods=["POST"])
    def _get_transactions():
        return request.invoke(
            transactions.get_transactions,
            GetTransactionsRequestSchema(),
            GetTransactionsResponseSchema(many=True),
        )
