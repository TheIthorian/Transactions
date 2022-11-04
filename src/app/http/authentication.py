from app.config import CONFIG


def is_key_valid(key: str) -> bool:
    return key is not None and key == CONFIG.API_KEY


def is_password_valid(password: str) -> bool:
    return password == CONFIG.PASSWORD
