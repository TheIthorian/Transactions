from app.http.authentication import is_key_valid


class Test_is_key_valid:
    def returns_true(self):
        key = "Any key works"
        assert is_key_valid(key)
