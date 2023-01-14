from dataclasses import dataclass
from marshmallow import Schema, fields, post_load


class BudgetItemSchema(Schema):
    id = fields.Integer()
    budget_id = fields.Integer()
    l1 = fields.String()
    amount = fields.Integer()
