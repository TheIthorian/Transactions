from app.http.request import Request
from app.user.user_schema import LoginRequest
from app.http.authentication import is_password_valid


def login(input: LoginRequest, request: Request = None):
    is_password_correct = is_password_valid(input.password)
    return {"logged_in": is_password_correct}
