from dataclasses import dataclass
from marshmallow import Schema, fields, post_load

from app.budget_item.budget_item_model import BudgetItem

### Common ###


class BudgetItemSchema(Schema):
    id = fields.Integer()
    budget_id = fields.Integer()
    l1 = fields.String()
    amount = fields.Integer()


### Get Budget Items ###


class GetBudgetItemsRequestSchema(Schema):
    budget_id = fields.Integer()

    @post_load
    def make(self, data, **kwargs):
        return data["budget_id"]


class GetBudgetItemsResponseSchema(Schema):
    budget_items = fields.Nested(BudgetItemSchema)


### Get Budget Item ###


@dataclass
class BudgetItemRequestBody:
    id: int
    budget_id: int


class GetBudgetItemRequestSchema(Schema):
    id = fields.Integer()
    budget_id = fields.Integer()

    @post_load
    def make(self, data, **kwargs):
        return BudgetItemRequestBody(**data)


class GetBudgetItemResponseSchema(BudgetItemSchema):
    pass


### Add Budget Items ###


class AddBudgetItemRequestSchema(Schema):
    budget_id = fields.Integer()
    l1 = fields.String()
    amount = fields.Integer()

    @post_load
    def make(self, data, **kwargs):
        return BudgetItem.make(**data)


### Add Budget Items ###


class UpdateBudgetItemRequestSchema(Schema):
    id = fields.Integer()
    budget_id = fields.Integer()
    amount = fields.Integer()

    @post_load
    def make(self, data, **kwargs):
        return BudgetItem.make(**data)
