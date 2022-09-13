from app.http.request import Request
from app.transactions.breakdown import (
    get_transaction_amounts_by_tag_level,
)
from app.transactions.filter import filter_transactions
from app.transactions.transaction_model import TAG_COLOR_MAP, Tag, Transaction
from app.transactions.transaction_schema import TransactionFilter

from app.transactions import data


def get_transactions(
    filter: TransactionFilter, request: Request = None
) -> list[Transaction]:
    transactions = data.get_transactions_for_tags(filter.tags)
    return filter_transactions(transactions, filter)


def get_transaction_breakdown(filter: TransactionFilter, request: Request = None):
    l1_data = get_transaction_amounts_by_tag_level(1)
    l2_data = get_transaction_amounts_by_tag_level(2)
    l3_data = get_transaction_amounts_by_tag_level(3)

    # return {"datasets": [l1_data, l2_data, l3_data]}

    return {
        "labels": [t[0] for t in l1_data],
        "datasets": [
            {
                "labels": [t[0] for t in l1_data],
                "data": [t[1] / 100 for t in l1_data],
                "backgroundColor": [TAG_COLOR_MAP[t[0]] for t in l1_data],
            },
            {
                "labels": [t[0] for t in l2_data],
                "data": [t[1] / 100 for t in l2_data],
                "backgroundColor": [
                    "#096dd9" if len(t[0]) > 0 else "lightgrey" for t in l2_data
                ],
            },
            {
                "labels": [t[0] for t in l3_data],
                "data": [t[1] / 100 for t in l3_data],
                "backgroundColor": [
                    "#096dd9" if len(t[0]) > 0 else "lightgrey" for t in l3_data
                ],
            },
        ],
    }


def get_all_tags(request: Request = None) -> list[Tag]:
    # print(data.get_all_tags.cache_info())
    return data.get_all_tags()
