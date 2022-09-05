from transactions.http.request import Request
from transactions.schema.transaction_schema import TransactionFilter


def get_transactions(filter: TransactionFilter, request: Request) -> dict:
    print(filter)

    data = [{"id": 10, "account": filter.account}]
    return data
