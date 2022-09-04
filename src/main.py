from app import app
from flask import jsonify, request

from response import add_cors


@app.route("/hello-world", methods=["GET"])
def _hello_world():
    output = {"Hello": "Hello", "World": "World"}
    return output


# Called before response is output to web service.
@app.after_request
def after_request(response):
    add_cors(response)
    return response


@app.errorhandler(404)
def not_found(error=None):
    message = {
        "status": 404,
        "message": "Record not found: " + request.url,
    }
    respone = jsonify(message)
    respone.status_code = 404
    return respone


if __name__ == "__main__":
    app.run(host="0.0.0.0")
