from marshmallow import Schema, fields, post_load

from app.tags.tag_schema import Tag, TagFilterSchema
from app.transactions.filter import TransactionFilter

### Get Transactions ###


class GetTransactionsRequestSchema(Schema):
    account = fields.String(required=False, allow_none=True)
    date_from = fields.Date(required=False, allow_none=True)
    date_to = fields.Date(required=False, allow_none=True)
    min_value = fields.Integer(required=False, allow_none=True)
    max_value = fields.Integer(required=False, allow_none=True)
    tags = fields.Nested(TagFilterSchema, allow_none=True)

    @post_load
    def make_filter(self, data, **kwargs):
        return TransactionFilter(**data)


class GetTransactionsResponseSchema(Schema):
    id = fields.Integer()
    account = fields.String()
    date = fields.Date()
    current_description = fields.String()
    original_description = fields.String()
    amount = fields.Integer()
    tag = fields.Nested(Tag)

    class Meta:
        ordered = True


### Get Transaction Breakdown ###


class GetTransactionBreakdownRequestSchema(GetTransactionsRequestSchema):
    pass


class DatasetSchema(Schema):
    labels = fields.List(fields.String())
    data = fields.List(fields.Float())
    backgroundColor = fields.List(fields.String())


class GetTransactionBreakdownResponseSchema(Schema):
    labels = fields.List(fields.String())
    datasets = fields.List(fields.Nested(DatasetSchema))
