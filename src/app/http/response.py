import json
from flask import make_response

from app.config import CONFIG


class Response:
    content_type = {"Content-Type": "application/json"}

    @classmethod
    def resolve(cls, data: any, request: "Request", code: int = 200):
        """Used by `Request` to make consistent responses."""
        if request.has_errors():
            return cls.generic_error(request)

        response = make_response()
        response.set_data(data)
        response.status_code = code
        response.content_type = cls.content_type

        for key, value in request.cookies.items():
            print(f"Setting response cookie {key}:{value}")
            response.set_cookie(key, value)

        return response

    @classmethod
    def authentication_error(cls, request: "Request"):
        """Creates an authentication error response"""
        response = make_response()

        response.set_data(json.dumps({"Error": "Authentication Error"}))
        response.status_code = 401
        response.content_type = cls.content_type
        return response

    @classmethod
    def generic_error(cls, request: "Request"):
        response = make_response()

        print(request.errors)
        response_body = {
            "errors: ": [error.to_json() for error in request.errors],
        }
        response.set_data(json.dumps(response_body))
        response.status_code = request.errors[0].code
        response.content_type = cls.content_type
        return response


def register_after_request(app):
    @app.after_request
    def after_request(response):
        # Called before response is output to web service.
        return add_cors(response)


def add_cors(response):
    response.headers["Access-Control-Allow-Origin"] = CONFIG.REQUEST_ORIGIN
    response.headers["Access-Control-Allow-Request-Headers"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, HEAD, OPTIONS, POST"
    # response.headers.add("Access-Control-Allow-Headers", "Access-Control-Allow-Headers")
    # response.headers.add("Access-Control-Allow-Headers", "Origin")
    # response.headers.add("Access-Control-Allow-Headers", "Content-Type")
    # response.headers.add(
    #     "Access-Control-Allow-Headers", "Access-Control-Request-Method"
    # )
    # response.headers.add(
    #     "Access-Control-Allow-Headers", "Access-Control-Request-Headers"
    # )
    response.headers["Access-Control-Allow-Headers"] = "Api-Key"

    return response
