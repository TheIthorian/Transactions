from typing import Callable, Union

from flask import Request as FlaskRequest, request
from marshmallow import Schema, EXCLUDE, ValidationError

from app.http.authentication import is_key_valid, is_session_id_valid
from app.http.response import Response


class Request:
    """Wrapper for the flask request object."""

    cookies: dict

    def __init__(self, request: FlaskRequest):
        self.request = request
        self.cookies = {}

    def check_api_key(self) -> bool:
        """Returns true if the request `Api-Key` header is valid."""
        key = self.request.headers.get("Api-Key")
        return is_key_valid(key)

    def check_session_id(self) -> bool:
        """Returns true if the request `session_id` cookie is valid."""
        session_id = self.request.cookies.get("session_id")
        return is_session_id_valid(session_id)

    def parse(self, schema: Schema) -> Union[dict, list]:
        """Returns the parsed request body."""
        data = self._get_data_from_request()
        return schema.load(data, unknown=EXCLUDE)

    def set_cookie(self, key, value):
        if value is not None:
            self.cookies[key] = value

    def _get_data_from_request(self) -> Union[any, None]:
        try:
            data = self.request.get_json()
        except:
            data = None

        return data


def invoke(
    fn: Callable, request_schema: Schema, response_schema: Schema, check_session_id=True
) -> tuple[any, int, dict]:
    """Validates the flask request against the input `request_schema`,
    invokes the `fn`, and outputs an object conforming to `response_schema`."""

    print(fn.__name__)

    has_input = request_schema is not None

    req = Request(request)

    if not req.check_api_key():
        return Response.authentication_error(req)

    if check_session_id and not req.check_session_id():
        return Response.authentication_error(req)

    try:
        if has_input:
            body = req.parse(request_schema)
    except ValidationError as error:
        return Response.resolve(error.messages, req, 400)

    if has_input:
        response_data = fn(body, req)
    else:
        response_data = fn(req)

    return Response.resolve(response_schema.dumps(response_data), req)


def invoke_without_auth(
    fn: Callable, request_schema: Schema, response_schema: Schema
) -> tuple[any, int, dict]:
    return invoke(fn, request_schema, response_schema, False)
