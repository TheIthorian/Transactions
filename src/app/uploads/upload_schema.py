from dataclasses import dataclass
from marshmallow import Schema, fields, post_load

from app.uploads.filter import UploadFilter


### Get Uploads ###


class UploadFilterSchema(Schema):
    date_from = fields.Date(required=False, allow_none=True)
    date_to = fields.Date(required=False, allow_none=True)


class GetUploadsRequestSchema(UploadFilterSchema):
    @post_load
    def make_filter(self, data, **kwargs):
        return UploadFilter(**data)


class GetUploadsResponseSchema(Schema):
    id = fields.Integer()
    file_name = fields.String()
    size = fields.Integer()
    date = fields.Date()
    md5 = fields.String()
    status = fields.String()

    class Meta:
        ordered = True


### Add Upload ###


class AddUploadSchema(Schema):
    pass


class AddUploadResponseSchema(GetUploadsResponseSchema):
    pass
