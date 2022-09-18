from urllib import request
import pytest
from app.http.request import Request
from app.http import authentication


class MockHeaders:
    headers = {"Api-Key": "Some api key"}

    def get(self, key: str, default=None):
        return self.headers[key]


class MockFlaskRequest:
    headers = MockHeaders()


mock_flask_request = MockFlaskRequest()


class Test_Request:
    def test_constructor(self):
        request = Request(mock_flask_request)
        assert request.request == mock_flask_request

    class Test_authenticate:
        calls = []

        def mock_is_key_valid(self, key):
            print(self.calls)
            self.calls.append([{"name": "mock_is_key_valid", "arguments": [key]}])
            print(self.calls)
            return True

        def test_validates_api_key(self, monkeypatch: pytest.MonkeyPatch):
            # Given

            monkeypatch.setattr(
                authentication,
                "is_key_valid",
                # lambda key: self.mock_is_key_valid(key),
                self.mock_is_key_valid,
            )

            print(self.calls)

            # When
            request = Request(MockFlaskRequest())
            result = request.authenticate()

            # Then
            # assert self.calls[0]["name"] == "mock_is_key_valids"
            # assert self.calls[0]["arguments"] == ["Some api key"]
            assert not result
