from app.config import CONFIG
from app.http.authentication import is_key_valid, is_password_valid


class Test_is_key_valid:
    def test_returns_false_for_invalid_key(self):
        key = "Incorrect key"
        assert not is_key_valid(key)

    def test_returns_true_for_correct_key(self):
        assert is_key_valid(CONFIG.API_KEY)


class Test_is_password_valid:
    def test_returns_false_for_invalid_password(self):
        password = "Incorrect password"
        assert not is_password_valid(password)

    def test_returns_true_for_correct_key(self):
        assert is_password_valid(CONFIG.PASSWORD)
