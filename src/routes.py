from flask import jsonify, request

from health import hello_world


def register_routes(app):
    @app.route("/hello-world", methods=["GET"])
    def _hello_world():
        return hello_world()

    @app.errorhandler(404)
    def _not_found(error=None):
        return not_found(error)


def not_found(error):
    print(error)
    message = {
        "status": 404,
        "message": "Record not found: " + request.url,
    }
    respone = jsonify(message)
    respone.status_code = 404
    return respone
