from marshmallow import Schema, fields, post_load
from dataclasses import dataclass


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


class Tag(Schema):
    l1 = fields.String()
    l2 = fields.String()
    l3 = fields.String()
    color = fields.String()

    class Meta:
        ordered = True


### Get All Tags ###


class GetAllTagsResponse(Schema):
    l1 = fields.String()
    l2 = fields.String()
    l3 = fields.String()
    color = fields.String()

    class Meta:
        ordered = True
