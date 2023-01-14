from app.config import CONFIG
from app import database


def is_key_valid(key: str) -> bool:
    return key is not None and key == CONFIG.API_KEY


def is_password_valid(password: str) -> bool:
    return password == CONFIG.PASSWORD


def is_session_id_valid(session_id: str) -> bool:
    found_session_id = get_session_id()
    return session_id is not None and session_id == found_session_id


def get_session_id():
    result = database.select(
        "SELECT session_id FROM Session WHERE valid_until_date > date()"
    )

    if len(result):
        return result[0].session_id
    return None
