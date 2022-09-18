from app.config import CONFIG
from app.http.response import Response, add_cors


class MockResponse:
    headers = {}


class Test_Response:
    class Test_resolve:

        data = "some data"

        def test_returns_correct_response(self):
            # Given
            code = 201

            # When
            result = Response.resolve(self.data, code)

            # Then
            assert result == (self.data, code, {"Content-Type": "application/json"})

        def test_defaults_result_code_to_200(self):
            # Given / When
            result = Response.resolve(self.data)

            # Then
            assert result == (self.data, 200, {"Content-Type": "application/json"})

    class Test_authentication_error:
        def test_returns_correct_response(self):
            # Given / When
            result = Response.authentication_error()

            # Then
            assert result == (
                {"Error": "Authentication Error"},
                401,
                {"Content-Type": "application/json"},
            )


def test_add_cors():
    # Given
    response = MockResponse()

    # When
    add_cors(response)

    # Then
    assert response.headers == {
        "Access-Control-Allow-Origin": CONFIG.REQUEST_ORIGIN,
        "Access-Control-Allow-Request-Headers": "*",
        "Access-Control-Allow-Methods": "GET, HEAD, OPTIONS, POST",
        "Access-Control-Allow-Headers": "Api-Key",
    }
