from typing import Callable, Union

from flask import Request as FlaskRequest, request
from marshmallow import Schema, EXCLUDE, ValidationError

from app.http.authentication import is_key_valid, is_password_valid
from app.http.response import Response


class Request:
    """Wrapper for the flask request object."""

    def __init__(self, request: FlaskRequest):
        self.request = request

    def check_api_key(self) -> bool:
        """Returns true if the request `Api-Key` header is valid."""
        key = self.request.headers.get("Api-Key")
        return is_key_valid(key)

    def check_password(self) -> bool:
        """Returns true if the request `password` header is valid."""
        return is_password_valid(self.request.headers.get("password"))

    def parse(self, schema: Schema) -> Union[dict, list]:
        """Returns the parsed request body."""
        data = self._get_data_from_request()
        return schema.load(data, unknown=EXCLUDE)

    def _get_data_from_request(self) -> Union[any, None]:
        try:
            data = self.request.get_json()
        except:
            data = None

        return data


def invoke(
    fn: Callable, request_schema: Schema, response_schema: Schema, check_password=True
) -> tuple[any, int, dict]:
    """Validates the flask request against the input `request_schema`,
    invokes the `fn`, and outputs an object conforming to `response_schema`."""
    has_input = request_schema is not None

    req = Request(request)

    if not req.check_api_key():
        return Response.authentication_error()

    if check_password and not req.check_password():
        return Response.authentication_error()

    print(fn.__name__)

    try:
        if has_input:
            body = req.parse(request_schema)
    except ValidationError as error:
        return error.messages, 400

    if has_input:
        response_data = fn(body, req)
    else:
        response_data = fn(req)

    return Response.resolve(response_schema.dumps(response_data))


def invoke_without_auth(
    fn: Callable, request_schema: Schema, response_schema: Schema
) -> tuple[any, int, dict]:
    return invoke(fn, request_schema, response_schema, False)
