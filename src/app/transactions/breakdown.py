from typing import Tuple
from app import database
from app.transactions.transaction_model import Query
from app.transactions.filter import TransactionFilter


def get_transaction_amounts_by_tag_level(
    level: int, filter: TransactionFilter
) -> Tuple[str, int]:
    """Returns a tuple of `(tag_name, amount)` for the given tag level"""
    query_builder = Query()
    condition = (
        query_builder.date_from(filter.date_from)
        .date_to(filter.date_to)
        .by_tag_filter(filter.tags)
        .build()
    )
    inputs = query_builder.get_inputs()

    tag_columns = ", ".join(["l1", "l2", "l3"][0:level])
    query = f"SELECT SUM(amount) AS amount, {tag_columns} FROM transactions {condition} GROUP BY {tag_columns} ORDER BY {tag_columns}"

    result = database.select(query, inputs)
    return [(r[level], r[0]) for r in result]


def get_average_transaction_amounts_by_tag_level(
    level: int, filter: TransactionFilter
) -> Tuple[str, int]:
    """Returns a tuple of `(tag_name, amount)` for the given tag level"""
    query_builder = Query()
    condition = (
        query_builder.date_from(filter.date_from)
        .date_to(filter.date_to)
        .by_tag_filter(filter.tags)
        .build()
    )
    inputs = query_builder.get_inputs()

    tag_columns = ", ".join(["l1", "l2", "l3"][0:level])
    year_column = "strftime('%Y', datetime( t.date, 'unixepoch' ))"
    month_column = "strftime('%m', datetime( t.date, 'unixepoch' ))"

    query = f"""
    SELECT AvG(SumByDate.amount) as AverageAmount, 
        {tag_columns}
    FROM (SELECT
            SUM(t.amount) AS amount, 
            {tag_columns},
            {year_column} As year, 
            {month_column} as month
        FROM transactions t
        {condition}
        GROUP BY 
            {tag_columns},
            {year_column}, 
            {month_column}
        ) AS SumByDate
    GROUP BY 
        {tag_columns}
    """

    result = database.select(query, inputs)
    return [(r[level], r[0]) for r in result]
