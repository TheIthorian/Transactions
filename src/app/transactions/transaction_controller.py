from app.http.request import Request
from app.transactions.breakdown import get_breakdown_by_tag
from app.transactions.filter import filter_transactions
from app.transactions.transaction_model import Tag, Transaction
from app.transactions.transaction_schema import TransactionFilter

from app.transactions import data


def get_transactions(
    filter: TransactionFilter, request: Request = None
) -> list[Transaction]:
    transactions = data.get_transactions_for_tags(filter.tags)
    return filter_transactions(transactions, filter)


def get_transaction_breakdown(filter: TransactionFilter, request: Request = None):
    transactions = data.get_transactions_for_tags(filter.tags)
    transactions_by_tag_level = data.group_transactions_by_tag_level(transactions)
    [l1_data, l2_data] = get_breakdown_by_tag(transactions_by_tag_level)

    print()
    print(l1_data, end="\n\n")
    print(l2_data, end="\n\n")

    l1_dataset = []
    x = """
    # add each l1 tag
        # pad other indeces
    """

    l2_dataset = [[]]
    y = """ 
    # add a list of tags for each l1 tag
        # between each group, add the difference between the sum of the group and the total for the corresponding l1
    # 
    """

    l3_dataset = [[[]]]
    z = """
    # For each l2 group, do the same as above
    """

    return {"datasets": [l1_data, l2_data]}

    return {
        "labels": [],
        "datasets": [
            {
                "label": "Amount per Tag",
                "data": [100, 0, 0, 0, 0, 10, 0, 0, 0, 0, 0, 0],
                "backgroundColor": ["rgba(255, 99, 132, 0.2)"],
            },
            {
                "label": "Amount per Tag",
                "data": [0, 20, 30, 0, 0, 0, 0, 0, 5, 5, 0, 0],
                "backgroundColor": [
                    "rgba(255, 99, 132, 0.2)",
                ],
            },
            {
                "label": "Amount per Tag",
                "data": [0, 0, 0, 5, 25, 0, 0, 0, 0, 0, 0, 5, 5],
                "backgroundColor": [
                    "rgba(255, 99, 132, 0.2)",
                ],
            },
        ],
    }


def get_all_tags(request: Request = None) -> list[Tag]:
    # print(data.get_all_tags.cache_info())
    return data.get_all_tags()
