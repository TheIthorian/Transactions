from app.http.request import Request
from app.user.user_schema import LoginRequest
from app.http.authentication import is_password_valid
from app.user.user_session import make_user_session


def login(input: LoginRequest, request: Request = None):
    is_password_correct = is_password_valid(input.password)

    session_id = ""
    if is_password_correct:
        session_id = make_user_session()
        request.set_cookie("session_id", session_id)

    return {"logged_in": is_password_correct}
