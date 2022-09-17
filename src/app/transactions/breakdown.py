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

    year_column = "strftime('%Y', datetime( t.date, 'unixepoch' ))"
    month_column = "strftime('%m', datetime( t.date, 'unixepoch' ))"

    if level == 1:
        query = f"""
        SELECT AvG(SumByDate.amount) as AverageAmount, SumByDate.l1
        FROM (SELECT
                SUM(t.amount) AS amount, 
                t.l1,
                {year_column} As year, 
                {month_column} as month
            FROM transactions t
            {condition}
            GROUP BY t.l1,
                {year_column}, 
                {month_column}
            ) AS SumByDate
        GROUP BY SumByDate.l1
        """
    elif level == 2:
        query = f"""
        SELECT AvG(SumByDate.amount) as AverageAmount, 
            SumByDate.l1, 
            SumByDate.l2
        FROM (SELECT
                SUM(t.amount) AS amount, 
                t.l1,
                t.l2,
                {year_column} As year, 
                {month_column} as month
            FROM transactions t
            {condition}
            GROUP BY t.l1,
                t.l2,
                {year_column}, 
                {month_column}
            ) AS SumByDate
        GROUP BY 
            SumByDate.l1,
            SumByDate.l2
        """
    elif level == 3:
        query = f"""
        SELECT AvG(SumByDate.amount) as AverageAmount, 
            SumByDate.l1, 
            SumByDate.l2,
            SumByDate.l3
        FROM (SELECT
                SUM(t.amount) AS amount, 
                t.l1,
                t.l2,
                t.l3,
                {year_column} As year, 
                {month_column} as month
            FROM transactions t
            {condition}
            GROUP BY t.l1,
                t.l2,
                t.l3,
                {year_column}, 
                {month_column}
            ) AS SumByDate
        GROUP BY 
            SumByDate.l1,
            SumByDate.l2,
            SumByDate.l3
        """

    result = database.select(query, inputs)
    return [(r[level], r[0]) for r in result]
