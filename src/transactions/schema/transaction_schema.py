from dataclasses import dataclass
from datetime import date
from marshmallow import Schema, fields, post_load


class Tags(Schema):
    l1 = fields.String(required=False)
    l2 = fields.String(required=False)
    l3 = fields.String(required=False)

    @post_load
    def make_tag(self, data):
        return FilterTags(**data)


class GetTransactionsRequestSchema(Schema):
    account = fields.String(required=False, allow_none=True)
    date_from = fields.Date(required=False, allow_none=True)
    date_to = fields.Date(required=False, allow_none=True)
    min_value = fields.Integer(required=False, allow_none=True)
    max_value = fields.Integer(required=False, allow_none=True)
    tags = fields.Nested(Tags, many=True)

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
    tag = Tags()

    class Meta:
        ordered = True


@dataclass
class FilterTags:
    l1: list[str] = None
    l2: list[str] = None
    l3: list[str] = None


@dataclass
class TransactionFilter:
    account: date = None
    date_from: date = None
    date_to: date = None
    min_value: int = None
    max_value: int = None
    tags: FilterTags = None
