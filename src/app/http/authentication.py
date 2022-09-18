from app.config import CONFIG


def is_key_valid(key: str) -> bool:
    return key is not None and key == CONFIG.API_KEY
