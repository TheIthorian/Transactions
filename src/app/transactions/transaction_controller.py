from typing import Tuple
from app.http.request import Request
from app.transactions.aggregate import aggregate
from app.transactions.filter import filter_tags_by_l1, filter_transactions
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

    l1_data: list[Tuple(str, int)] = []
    l1_tags = data.get_tags_from_transactions(transactions_by_tag_level.l1)
    unique_l1_tag_names = set(map(lambda t: t.l1, l1_tags))
    for tag_name in unique_l1_tag_names:
        tag_amount = aggregate(
            transactions_by_tag_level.l1,
            lambda t: t.tag.l1 == tag_name,
            lambda t: t.amount,
            0,
        )
        l1_data.append(tuple([tag_name, tag_amount]))

    l2_data: list[set] = []  # all l2 tags, split by their l1 parent
    l2_tags = data.get_tags_from_transactions(transactions_by_tag_level.l2)
    for l1_tag in unique_l1_tag_names:
        l2_tags_for_l1 = set()
        unique_l2_tag_names = set(
            map(lambda t: t.l2, filter_tags_by_l1(l2_tags, l1_tag))
        )
        for tag in unique_l2_tag_names:
            tag_amount = aggregate(
                transactions_by_tag_level.l2,
                lambda t: t.tag.l2 == tag and t.tag.l2 != "",
                lambda t: t.amount,
                0,
            )
            l2_tags_for_l1.add(tuple([tag, tag_amount]))

        l2_data.append(l2_tags_for_l1)

    # l3_data: list[set] = []
    # l3_tags = data.get_tags_from_transactions(transactions_by_tag_level.l3)
    # for l1_tag in l2_tags:
    #     l3_tags_for_l2 = set()
    #     for tag in filter_tags_by_l1(l3_tags, l1_tag):
    #         tag_amount = aggregate(
    #             transactions_by_tag_level.l3,
    #             lambda t: t.tag.l3 == tag.l3,
    #             lambda t: t.amount,
    #             0,
    #         )
    #         l3_tags_for_l2.add(tuple([tag.l3, tag_amount]))
    #     l3_data.append(l3_tags_for_l2)

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
