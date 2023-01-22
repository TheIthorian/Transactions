from app.http.request import Request

from app.tags.tag_model import get_color_for_tag

from app.transactions import data
from app.transactions.breakdown import (
    get_average_transaction_amounts_by_tag_level,
    get_total_amount,
    get_total_average_amount,
    get_transaction_amounts_by_tag_level,
)
from app.transactions import timeline
from app.transactions.filter import filter_transactions
from app.transactions.transaction_model import Transaction
from app.transactions.filter import TransactionFilter
from app.transactions.transaction_schema import TimelineRequest
from app.util import list as list_util


def get_transactions(
    filter: TransactionFilter, request: Request = None
) -> list[Transaction]:
    transactions = data.get_transactions_for_tags(filter.tags)
    return filter_transactions(transactions, filter)


def get_transaction_breakdown(filter: TransactionFilter, request: Request = None):
    l1_data = get_transaction_amounts_by_tag_level(1, filter)
    l2_data = get_transaction_amounts_by_tag_level(2, filter)
    l3_data = get_transaction_amounts_by_tag_level(3, filter)
    total_amount = get_total_amount(filter)

    return _format_breakdown_output(l1_data, l2_data, l3_data, total_amount)


def get_transaction_breakdown_month_average(
    filter: TransactionFilter, request: Request = None
):
    l1_data = get_average_transaction_amounts_by_tag_level(1, filter)
    l2_data = get_average_transaction_amounts_by_tag_level(2, filter)
    l3_data = get_average_transaction_amounts_by_tag_level(3, filter)
    total_amount = get_total_average_amount(filter)

    return _format_breakdown_output(l1_data, l2_data, l3_data, total_amount)


def _format_breakdown_output(l1_data, l2_data, l3_data, total_amount):
    return {
        "labels": [t[0] for t in l1_data],
        "datasets": [
            {
                "labels": [t[0] for t in l1_data],
                "data": [t[1] / 100 for t in l1_data],
                "backgroundColor": [get_color_for_tag(t[0]) for t in l1_data],
            },
            {
                "labels": [t[0] for t in l2_data],
                "data": [t[1] / 100 for t in l2_data],
                "backgroundColor": [
                    "#096dd9" if t[0] is None or len(t[0]) > 0 else "transparent"
                    for t in l2_data
                ],
            },
            {
                "labels": [t[0] for t in l3_data],
                "data": [t[1] / 100 for t in l3_data],
                "backgroundColor": [
                    "#096dd9" if t[0] is None or len(t[0]) > 0 else "transparent"
                    for t in l3_data
                ],
            },
        ],
        "total": (total_amount or 0) / 100,
    }


def get_transaction_timeline(input: TimelineRequest, request: Request = None):
    data_sets = timeline.get_transaction_timeline(input.filter, input.group_by_tags)

    if input.group_by_tags:
        l1_tags = list_util.unique(list(map(lambda d: d.l1, data_sets)))
        l1_new_data_sets = [
            [y for y in data_sets if y.l1 == x and y.l1 is not None] for x in l1_tags
        ]

        l2_tags = list_util.unique(list(map(lambda d: d.l2, data_sets)))
        l2_new_data_sets = [
            [y for y in data_sets if y.l2 == x and y.l2 is not None] for x in l2_tags
        ]

        l3_tags = list_util.unique(list(map(lambda d: d.l3, data_sets)))
        l3_new_data_sets = [
            [y for y in data_sets if y.l3 == x and y.l3 is not None] for x in l3_tags
        ]

        all_data_sets = []
        for data_set in l1_new_data_sets:
            if len(data_set):
                all_data_sets.append(
                    {
                        "label": data_set[0].l1,
                        "data": [d.amount / 100 for d in data_set],
                        "backgroundColor": get_color_for_tag(data_set[0].l1),
                    }
                )

        for data_set in l2_new_data_sets:
            if len(data_set):
                all_data_sets.append(
                    {
                        "label": data_set[0].l2,
                        "data": [d.amount / 100 for d in data_set],
                        "backgroundColor": get_color_for_tag(data_set[0].l1),
                    }
                )

        for data_set in l3_new_data_sets:
            if len(data_set):
                all_data_sets.append(
                    {
                        "label": data_set[0].l3,
                        "data": [d.amount / 100 for d in data_set],
                        "backgroundColor": get_color_for_tag(data_set[0].l1),
                    }
                )

        return {
            "labels": list_util.unique(
                list(map(lambda d: d.month_start_date, data_sets))
            ),
            "datasets": all_data_sets,
        }

    return {
        "labels": [d.month_start_date for d in data_sets],
        "datasets": [
            {
                "label": "Total",
                "data": [d.amount / 100 for d in data_sets],
                "backgroundColor": "blue",
            }
        ],
    }
