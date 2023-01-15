from marshmallow import Schema, fields, post_load
from ..budget_item.budget_item_schema import BudgetItemSchema
from ..budget.budget_model import Budget

# class GetBudgetsRequestSchema(Schema):


class GetBudgetResponseSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    total_limit = fields.Float()
    budget_items = fields.Nested(BudgetItemSchema)

    class Meta:
        ordered = True


class GetBudgetsResponseSchema(GetBudgetResponseSchema):
    pass


class AddBudgetRequestSchema(Schema):
    name = fields.String(required=False, allow_none=True)
    total_limit = fields.Float(required=False, allow_none=True)

    @post_load
    def make_budget(self, data, **kwargs):
        return Budget(**data, id=None)
