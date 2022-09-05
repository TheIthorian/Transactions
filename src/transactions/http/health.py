def hello_world():
    output = {"Hello": "Hello", "World": "World"}
    return output


def status():
    return {"status": "active"}


def register_routes(app):
    @app.route("/hello-world", methods=["GET"])
    def _hello_world():
        return hello_world()

    @app.route("/health", methods=["GET", "POST"])
    def _health():
        return status()
