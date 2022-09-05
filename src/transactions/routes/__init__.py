from flask import jsonify, request

from transactions.routes import health, transactions

# https://stackoverflow.com/questions/17129573/can-i-use-external-methods-as-route-decorators-in-python-flask
def register_routes(app):
    health.register_routes(app)
    transactions.register_routes(app)

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
