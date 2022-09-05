class Response:
    @staticmethod
    def authentication_error():
        return {"Error": "Authentication Error"}


def register_after_request(app):
    # Called before response is output to web service.
    @app.after_request
    def after_request(response):
        add_cors(response)
        return response


def add_cors(response):
    response.headers.set("Access-Control-Allow-Origin", "*")
    response.headers["Access-Control-Allow-Request-Headers"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, HEAD, OPTIONS, POST"
    response.headers.add("Access-Control-Allow-Headers", "Access-Control-Allow-Headers")
    response.headers.add("Access-Control-Allow-Headers", "Origin")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type")
    response.headers.add(
        "Access-Control-Allow-Headers", "Access-Control-Request-Method"
    )
    response.headers.add(
        "Access-Control-Allow-Headers", "Access-Control-Request-Headers"
    )
    response.headers.add("Access-Control-Allow-Headers", "apikey")