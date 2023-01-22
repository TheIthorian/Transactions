from dataclasses import dataclass
from datetime import date, datetime
from app import database
from app.transactions.filter import TransactionFilter
from app.transactions.transaction_model import Query


@dataclass
class TimelineMonth:
    amount: int
    month_start_date: date
    l1: str = None
    l2: str = None
    l3: str = None

    def __eq__(self, other: "TimelineMonth") -> bool:
        return (
            self.amount == other.amount
            and self.month_start_date == other.month_start_date
            and self.l1 == other.l1
            and self.l2 == other.l2
            and self.l3 == other.l3
        )


def get_transaction_timeline(
    filter: TransactionFilter, group_by_tag: bool = True
) -> list[TimelineMonth]:
    qb = (
        Query(alias="t.")
        .by_account(filter.account)
        .amount_from(filter.min_value)
        .amount_to(filter.max_value)
    )
    conditions = qb.build_conditions(query="", include_where=False)

    date_qb = Query(alias="dt.").date_from(filter.date_from).date_to(filter.date_to)
    date_conditions = date_qb.build()

    tag_qb = Query(alias="tr.").by_tag_filter(filter.tags)
    tag_conditions = tag_qb.build()

    include_l1 = group_by_tag and len(filter.tags.l1 or [])
    include_l2 = group_by_tag and len(filter.tags.l2 or [])
    include_l3 = group_by_tag and len(filter.tags.l3 or [])

    # If there is no filtering, group by l1
    if not include_l1 and not include_l2 and not include_l3:
        include_l1 = True

    l1_column = ", tags.l1" if include_l1 else ""
    l2_column = ", tags.l2" if include_l2 else ""
    l3_column = ", tags.l3" if include_l3 else ""

    tag_columns = []
    if include_l1:
        tag_columns.append("tr.l1")
    if include_l2:
        tag_columns.append("tr.l2")
    if include_l3:
        tag_columns.append("tr.l3")

    tag_join_conditions = []
    if include_l1:
        tag_join_conditions.append("t.l1 = tags.l1")
    if include_l2:
        tag_join_conditions.append("t.l2 = tags.l2")
    if include_l3:
        tag_join_conditions.append("t.l3 = tags.l3")
    tag_join_conditions.append("strftime('%Y-%m', t.date, 'unixepoch') = months.month")

    query = f"""SELECT 
            SUM(COALESCE(t.amount, 0)) as total, 
            months.month
            {l1_column}
            {l2_column}
            {l3_column}
        FROM 
        (SELECT DISTINCT {", ".join(tag_columns)} FROM transactions tr {tag_conditions}) as tags,
        (SELECT DISTINCT strftime('%Y-%m', dt.date, 'unixepoch') month from transactions dt {date_conditions}) as months
        LEFT JOIN Transactions t 
            {"ON " + " AND ".join(tag_join_conditions)}
            {conditions}
        GROUP BY 
            months.month
            {l1_column}
            {l2_column}
            {l3_column}
        ORDER BY 
            months.month
            {l1_column}
            {l2_column}
            {l3_column}"""

    print(query)

    inputs = [*date_qb.get_inputs(), *qb.get_inputs(), *tag_qb.get_inputs()]

    amounts = database.select(query, inputs)

    date_format = "%Y-%m"

    return [
        TimelineMonth(
            amount=row.total,
            month_start_date=datetime.strptime(row[1], date_format).date(),
            l1=row.l1 if include_l1 else None,
            l2=row.l2 if include_l2 else None,
            l3=row.l3 if include_l3 else None,
        )
        for row in amounts
    ]
