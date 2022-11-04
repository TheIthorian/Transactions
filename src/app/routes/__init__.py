from flask import request

from app.routes import health
from app.routes.error import make_not_found_error
from app import transactions, tags, user

# https://stackoverflow.com/questions/17129573/can-i-use-external-methods-as-route-decorators-in-python-flask
def register_routes(app):
    app.register_error_handler(404, make_not_found_error(request))
    health.register_routes(app)

    user.register_routes(app)
    transactions.register_routes(app)
    tags.register_routes(app)
