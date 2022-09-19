from dataclasses import dataclass
from datetime import date, datetime
from app import database
from app.transactions.filter import TransactionFilter


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
    qb = filter.build_query()
    conditions = qb.build()
    month_column = "strftime('%Y-%m', t.date, 'unixepoch')"
    l1_column = ", t.l1" if group_by_tag else ""

    query = f"""SELECT SUM(t.amount) as total, {month_column} AS Month {l1_column}
        FROM Transactions t 
        {conditions}
        GROUP BY 
            {month_column} {l1_column}
        ORDER BY 
            {month_column} {l1_column}
        """

    amounts = database.select(query, qb.get_inputs())

    date_format = "%Y-%m"
    return [
        TimelineMonth(
            amount=row[0],
            month_start_date=datetime.strptime(row[1], date_format).date(),
            l1=row[2] if group_by_tag else None,
        )
        for row in amounts
    ]
