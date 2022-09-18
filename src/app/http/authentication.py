from app.config import CONFIG


def is_key_valid(key: str) -> bool:
    return key == CONFIG.API_KEY
