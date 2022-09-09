from typing import Tuple
from app.http.request import Request
from app.transactions.transaction_model import Tag, Transaction
from app.transactions.transaction_schema import TransactionFilter

from app.transactions import data


def get_transactions(
    filter: TransactionFilter, request: Request = None
) -> list[Transaction]:
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


def get_transaction_breakdown(filter: TransactionFilter, request: Request = None):
    def get_l1_tag_amounts(*args) -> list[Tuple[Tag, int]]:
        pass

    def get_l2_tag_amounts(*args) -> list[Tuple[Tag, int]]:
        pass

    def get_l3_tag_amounts(*args) -> list[Tuple[Tag, int]]:
        pass

    transactions = get_transactions(filter)

    print(filter)
    # [(tag1, total amount), (tag2, total amount)]
    l1_data = get_l1_tag_amounts(transactions)

    # [(tag1.1, total amount), (tag2.1, total amount)]
    l2_data = get_l2_tag_amounts(transactions)

    # [(tag1.1.1, total amount), (tag2.1.1, total amount)]
    l3_data = get_l3_tag_amounts(transactions)

    # total_number_of_tags = len(l1_data) + len(l2_data) + len(l3_data)

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
