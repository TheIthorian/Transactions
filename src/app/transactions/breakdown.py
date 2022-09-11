from typing import Tuple
from app.transactions import data
from app.transactions.aggregate import aggregate
from app.transactions.filter import filter_tags_by_l1, filter_tags_by_l2
from app.transactions.transaction_model import TransactionsByTagLevel
from app.util.list import unique


def get_breakdown_by_tag(
    transactions_by_tag_level: TransactionsByTagLevel,
) -> Tuple[list, list, list]:
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

    l2_data: list[list] = []  # all l2 tags, split by their l1 parent
    all_l2_tags = data.get_tags_from_transactions(transactions_by_tag_level.l2)
    for l1_tag in unique_l1_tag_names:
        l2_tags_for_l1: list[Tuple] = []
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
            l2_tags_for_l1.append((tag, tag_amount))

        l2_data.append(l2_tags_for_l1)

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
