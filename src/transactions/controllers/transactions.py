from transactions.schema.transaction_schema import TransactionFilter


def get_transactions(filter: TransactionFilter) -> dict:
    print(filter)

    data = [{"id": 10, "account": filter.account}]
    return data
