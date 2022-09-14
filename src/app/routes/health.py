from app.tags.data import get_all_tags
from app.transactions.data import (
    get_all_transactions,
    get_tags_from_transactions,
)


def hello_world():
    output = {"Hello": "Hello", "World": "World"}

    transactionss = get_all_transactions()
    tags = get_tags_from_transactions(transactionss)
    tags = get_all_tags()
    for t in tags:
        print(t)
    return tags


def status():
    return {"status": "active"}


def register_routes(app):
    app.add_url_rule("/hello-world", view_func=hello_world, methods=["GET"])
    app.add_url_rule("/health", view_func=status, methods=["GET", "POST"])
