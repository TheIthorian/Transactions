from flask import request

from app.routes import health
from app.routes.error import make_not_found_error, make_filesize_too_large_error
from app import transactions, tags, user, budget, budget_item, uploads

# https://stackoverflow.com/questions/17129573/can-i-use-external-methods-as-route-decorators-in-python-flask
def register_routes(app):
    app.config["MAX_CONTENT_LENGTH"] = uploads.config.MAX_CONTENT_LENGTH

    app.register_error_handler(404, make_not_found_error(request))
    app.register_error_handler(413, make_filesize_too_large_error(request))
    health.register_routes(app)

    user.register_routes(app)
    transactions.register_routes(app)
    tags.register_routes(app)
    budget.register_routes(app)
    budget_item.register_routes(app)
    uploads.register_routes(app)
