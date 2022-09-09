from dataclasses import dataclass
from datetime import date
from marshmallow import Schema, fields, post_load

### Get Transactions ###


@dataclass
class TagFilter:
    l1: list[str] = None
    l2: list[str] = None
    l3: list[str] = None


class TagFilterSchema(Schema):
    l1 = fields.List(fields.String(required=False))
    l2 = fields.List(fields.String(required=False))
    l3 = fields.List(fields.String(required=False))

    @post_load
    def make_tag(self, data, **kwargs):
        return TagFilter(**data)


@dataclass
class TransactionFilter:
    account: date = None
    date_from: date = None
    date_to: date = None
    min_value: int = None
    max_value: int = None
    tags: TagFilter = None


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


class Tag(Schema):
    l1 = fields.String()
    l2 = fields.String()
    l3 = fields.String()
    color = fields.String()

    class Meta:
        ordered = True


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


GetTransactionBreakdownRequestSchema = GetTransactionsRequestSchema


class DatasetSchema(Schema):
    label = fields.String()
    data = fields.List(fields.Float())
    color = fields.List(fields.String())


class GetTransactionBreakdownResponseSchema(Schema):
    labels = fields.List(fields.String())
    datasets = fields.List(fields.Nested(DatasetSchema))


### Get All Tags ###


class GetAllTagsResponse(Schema):
    l1 = fields.String()
    l2 = fields.String()
    l3 = fields.String()
    color = fields.String()

    class Meta:
        ordered = True
