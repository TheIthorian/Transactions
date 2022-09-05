from transactions.routes import health, transactions
from transactions.routes.error import not_found_error

# https://stackoverflow.com/questions/17129573/can-i-use-external-methods-as-route-decorators-in-python-flask
def register_routes(app):
    app.register_error_handler(404, not_found_error)
    health.register_routes(app)
    transactions.register_routes(app)
