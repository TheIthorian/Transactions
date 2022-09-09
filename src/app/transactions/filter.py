from app.transactions.transaction_model import Transaction
from app.transactions.transaction_schema import TransactionFilter
from app.transactions import data


def filter_transactions(transactions: list[Transaction], filter: TransactionFilter):
    filtered_transactions = data.Filter.filter_by_date(
        transactions, start_date=filter.date_from, end_date=filter.date_to
    )
    filtered_transactions = data.Filter.filter_by_account(
        filtered_transactions, filter.account
    )
    filtered_transactions = data.Filter.filter_by_value(
        filtered_transactions, filter.min_value, filter.max_value
    )

    return filtered_transactions
