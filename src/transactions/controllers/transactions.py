from transactions.http.request import Request
from transactions.schema.transaction_schema import TransactionFilter

from transactions import data


def get_transactions(filter: TransactionFilter, request: Request) -> list:
    filtered_transactions = data.get_transactions_for_tags(filter.tags)
    filtered_transactions = data.Filter.filter_by_date(
        filtered_transactions, start_date=filter.date_from, end_date=filter.date_to
    )
    filtered_transactions = data.Filter.filter_by_account(
        filtered_transactions, filter.account
    )
    filtered_transactions = data.Filter.filter_by_value(
        filtered_transactions, filter.min_value, filter.max_value
    )

    return filtered_transactions


def get_all_tags(request: Request) -> list:
    # print(data.get_all_tags.cache_info())
    return data.get_all_tags()
