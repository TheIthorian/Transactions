from dataclasses import dataclass
from marshmallow import Schema, fields, post_load

from app.budget_item.budget_item_model import BudgetItem

### Common ###


class BudgetItemSchema(Schema):
    id = fields.Integer()
    budget_id = fields.Integer()
    l1 = fields.String()
    amount = fields.Integer()
    tag_color = fields.String()
    spent = fields.Float()

    class Meta:
        ordered = True


### Get Budget Items ###


@dataclass
class GetBudgetItemsRequestBody:
    budget_id: int


class GetBudgetItemsRequestSchema(Schema):
    budget_id = fields.Integer(required=True)

    @post_load
    def make(self, data, **kwargs):
        return GetBudgetItemsRequestBody(**data)


class GetBudgetItemsResponseSchema(BudgetItemSchema):
    pass


### Get Budget Item ###


@dataclass
class BudgetItemRequestBody:
    id: int
    budget_id: int


class GetBudgetItemRequestSchema(Schema):
    id = fields.Integer(required=True)
    budget_id = fields.Integer(required=True)

    @post_load
    def make(self, data, **kwargs):
        return BudgetItemRequestBody(**data)


class GetBudgetItemResponseSchema(BudgetItemSchema):
    pass


### Add Budget Items ###


class AddBudgetItemRequestSchema(Schema):
    budget_id = fields.Integer(required=True)
    l1 = fields.String(required=True)
    amount = fields.Integer()

    @post_load
    def make(self, data, **kwargs):
        return BudgetItem.make(**data)


### Add Budget Items ###


class UpdateBudgetItemRequestSchema(Schema):
    id = fields.Integer(required=True)
    budget_id = fields.Integer(required=True)
    amount = fields.Integer()

    @post_load
    def make(self, data, **kwargs):
        return BudgetItem.make(**data)
