def hello_world():
    output = {"Hello": "Hello", "World": "World"}
    return output


def status():
    return {"status": "active"}


def register_routes(app):
    app.add_url_rule("/hello-world", view_func=hello_world, methods=["GET"])
    app.add_url_rule("/health", view_func=status, methods=["GET", "POST"])
