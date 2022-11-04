from dataclasses import dataclass
from marshmallow import Schema, fields, post_load


@dataclass
class LoginRequest:
    password: str


class LoginRequestSchema(Schema):
    password = fields.String(required=True, allow_none=False)

    @post_load
    def make_filter(self, data, **kwargs):
        return LoginRequest(**data)


class GetUserSchema(Schema):
    logged_in = fields.Boolean()
