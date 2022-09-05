from transactions.http.request import Request
from transactions.schema.transaction_schema import TransactionFilter

from transactions.data import get_transactions_for_tags, Filter


def get_transactions(filter: TransactionFilter, request: Request) -> list:
    filtered_transactions = get_transactions_for_tags(filter.tags)
    filtered_transactions = Filter.filter_by_date(
        filtered_transactions, start_date=filter.date_from, end_date=filter.date_to
    )
    filtered_transactions = Filter.filter_by_account(
        filtered_transactions, filter.account
    )
    filtered_transactions = Filter.filter_by_value(
        filtered_transactions, filter.min_value, filter.max_value
    )

    return filtered_transactions
