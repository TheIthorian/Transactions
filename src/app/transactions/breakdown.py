from typing import Tuple
from app import database
from app.transactions import data
from app.transactions.aggregate import aggregate
from app.tags.filter import filter_tags_by_l1
from app.transactions.transaction_model import TransactionsByTagLevel
from app.util.list import unique


def get_transaction_amounts_by_tag_level(level: int):
    if level == 1:
        query = """SELECT SUM(amount) AS amount, l1 FROM transactions GROUP BY l1 ORDER BY l1"""
    elif level == 2:
        query = """SELECT SUM(amount) AS amount, l1, l2 FROM transactions GROUP BY l1, l2 ORDER BY l1, l2"""
    elif level == 3:
        query = """SELECT SUM(amount) AS amount, l1, l2, l3 FROM transactions GROUP BY l1, l2, l3 ORDER BY l1, l2, l3"""

    result = database.select(query)
    return [(r[level], r[0]) for r in result]


def get_breakdown_by_tag(
    transactions_by_tag_level: TransactionsByTagLevel,
) -> Tuple[list, list, list]:
    print(transactions_by_tag_level)
    l1_data: list[Tuple] = []
    all_l1_tags = data.get_tags_from_transactions(transactions_by_tag_level.l1)
    unique_l1_tag_names = unique(map(lambda t: t.l1, all_l1_tags))
    for tag_name in unique_l1_tag_names:
        tag_amount = aggregate(
            transactions_by_tag_level.l1,
            lambda t: t.tag.l1 == tag_name,
            lambda t: t.amount,
            0,
        )
        l1_data.append((tag_name, tag_amount))

    l2_data: list[Tuple] = []  # all l2 tags, split by their l1 parent
    all_l2_tags = data.get_tags_from_transactions(transactions_by_tag_level.l2)
    for l1_tag, l1_total_amount in l1_data:
        l1_sum = 0
        unique_l2_tag_names = unique(
            map(lambda t: t.l2, filter_tags_by_l1(all_l2_tags, l1_tag))
        )
        for tag in unique_l2_tag_names:
            tag_amount = aggregate(
                transactions_by_tag_level.l2,
                lambda t: t.tag.l2 == tag and t.tag.l2 != "",
                lambda t: t.amount,
                0,
            )
            l1_sum += tag_amount
            l2_data.append((tag, tag_amount))

        l2_data.append(("None", l1_total_amount - l1_sum))

    l3_data: list[list[list]] = []  # all l3 tags, split by their l2 parent
    all_l3_tags = data.get_tags_from_transactions(transactions_by_tag_level.l3)
    for l1_tags in l2_data:
        l3_tag_data: list[list] = []

        if len(l1_tags) == 0:
            l3_tag_data = [[]]

        for l2_tag, _ in l1_tags:
            l3_tags_for_l2: list[Tuple] = []
            for l3_tag in unique(
                map(lambda t: t.l3, filter_tags_by_l2(all_l3_tags, l2_tag))
            ):
                tag_amount = aggregate(
                    transactions_by_tag_level.l3,
                    lambda t: t.tag.l3 == l3_tag and t.tag.l3 != "",
                    lambda t: t.amount,
                    0,
                )
                l3_tags_for_l2.append((l3_tag, tag_amount))

            l3_tag_data.append(l3_tags_for_l2)

        l3_data.append(l3_tag_data)

    return l1_data, l2_data, l3_data
