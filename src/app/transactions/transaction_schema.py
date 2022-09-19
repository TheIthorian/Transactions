from dataclasses import dataclass
from marshmallow import Schema, fields, post_load

from app.tags.tag_schema import TagSchema, TagFilterSchema
from app.transactions.filter import TransactionFilter

### Get Transactions ###


class TransactionFilterSchema(Schema):
    account = fields.String(required=False, allow_none=True)
    date_from = fields.Date(required=False, allow_none=True)
    date_to = fields.Date(required=False, allow_none=True)
    min_value = fields.Integer(required=False, allow_none=True)
    max_value = fields.Integer(required=False, allow_none=True)
    tags = fields.Nested(TagFilterSchema, allow_none=True)


class GetTransactionsRequestSchema(TransactionFilterSchema):
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
    tag = fields.Nested(TagSchema)

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
    total = fields.String()

    class Meta:
        ordered = True


### Get Transaction Timeline ###


@dataclass
class TimelineRequest:
    group_by_tags: bool = False
    filter: TransactionFilter = TransactionFilter()


class GetTransactionTimelineRequestSchema(Schema):
    group_by_tags = fields.Boolean(allow_none=False, required=True)
    filter = fields.Nested(TransactionFilterSchema, allow_none=False, required=True)

    @post_load
    def make_request_dto(self, data, **kwargs):
        return TimelineRequest(
            group_by_tags=data["group_by_tags"],
            filter=TransactionFilter(**data["filter"]),
        )


class TimelineDatasetSchema(Schema):
    label = fields.String()
    data = fields.List(fields.Float())
    backgroundColor = fields.String()


class GetTransactionTimelineResponseSchema(Schema):
    labels = fields.List(fields.Date())
    datasets = fields.List(fields.Nested(TimelineDatasetSchema), many=True)

    class Meta:
        ordered = True
