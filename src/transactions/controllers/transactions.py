from transactions.http.response import Response


def get_transactions(body: dict) -> Response:
    return [{"id": 10}]
