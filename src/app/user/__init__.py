import app.http.request as request
from app.user.user_schema import GetUserSchema, LoginRequestSchema
from app.user import user_controller as user


def register_routes(app):
    @app.route("/login", methods=["POST"])
    def _login():
        return request.invoke_without_auth(
            user.login,
            LoginRequestSchema(),
            GetUserSchema(),
        )
