from transactions.http.response import Response
from transactions.schema.transaction_schema import TransactionFilter


def get_transactions(filter: TransactionFilter) -> dict:
    print(filter.account)
    print(filter.date_from)
    print(filter.date_to)
    print(filter.min_value)
    print(filter.max_value)
    print(filter.tags)

    data = [{"id": 10, "account": filter.account}]
    return data
