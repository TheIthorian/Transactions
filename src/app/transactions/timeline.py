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

    def __eq__(self, other: "TimelineMonth") -> bool:
        return (
            self.amount == other.amount
            and self.month_start_date == other.month_start_date
            and self.l1 == other.l1
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

    l1_column = ", tags.l1" if group_by_tag else ""

    query = f"""SELECT 
            SUM(COALESCE(t.amount, 0)) as total, 
            months.month
            {l1_column}
        FROM 
        (SELECT DISTINCT tr.l1 FROM transactions tr {tag_conditions}) as tags,
        (SELECT DISTINCT strftime('%Y-%m', dt.date, 'unixepoch') month from transactions dt {date_conditions}) as months
        LEFT JOIN Transactions t 
            ON t.l1 = tags.l1 
            AND strftime('%Y-%m', t.date, 'unixepoch') = months.month
            {conditions}
        GROUP BY 
            months.month
            {l1_column}
        ORDER BY 
            months.month
            {l1_column}"""

    inputs = [*date_qb.get_inputs(), *qb.get_inputs(), *tag_qb.get_inputs()]

    amounts = database.select(query, inputs)

    date_format = "%Y-%m"
    return [
        TimelineMonth(
            amount=row[0],
            month_start_date=datetime.strptime(row[1], date_format).date(),
            l1=row[2] if group_by_tag else None,
        )
        for row in amounts
    ]
