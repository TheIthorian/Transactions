from unittest import mock
import unittest
from app.http.request import Request
from app.http import authentication


class MockHeaders:
    headers = {"Api-Key": "Some api key", "password": "some password"}

    def get(self, key: str, default=None):
        return self.headers[key]


class MockFlaskRequest:
    headers = MockHeaders()


mock_flask_request = MockFlaskRequest()


class Test_Request(unittest.TestCase):
    def test_constructor(self):
        request = Request(mock_flask_request)
        assert request.request == mock_flask_request

    # @mock.patch("app.http.authentication.is_key_valid")
    # def test_validates_api_key(self):
    #     # Given

    #     # When
    #     request = Request(MockFlaskRequest())
    #     result = request.authenticate()

    #     # Then
    #     # assert result
