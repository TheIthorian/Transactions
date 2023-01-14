from app.config import CONFIG
from flask import make_response


class Response:
    content_type = {"Content-Type": "application/json"}

    @classmethod
    def resolve(
        cls, data: any, request: "Request", code: int = 200
    ) -> tuple[any, int, dict]:
        """Used by `Request` to make consistent responses."""
        response = make_response()
        response.data = data
        response.status_code = code
        response.content_type = cls.content_type

        for key, value in request.cookies.items():
            print(request.cookies)
            response.set_cookie(key, value)

        return response

    @classmethod
    def authentication_error(cls) -> tuple[any, int, dict]:
        """Creates an authentication error response"""
        return {"Error": "Authentication Error"}, 401, cls.content_type


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
