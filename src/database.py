"""Module to interact with the SQLite database.

(C) 2022, TheIthorian, United Kingdom
"""

from collections import namedtuple
import sqlite3


def namedtuple_factory(cursor: sqlite3.Cursor, row: sqlite3.Row):
    """Returns sqlite rows as named tuples."""
    fields = [col[0] for col in cursor.description]
    Row = namedtuple("Row", fields)
    return Row(*row)


def connect() -> sqlite3.Connection:
    return sqlite3.connect("transactions.db")


def init() -> None:
    """Creates the database."""
    con = connect()
    cur = con.cursor()

    cur.execute(
        """CREATE TABLE IF NOT EXISTS TABLE_NAME transactions
               (account text, 
               date integer, 
               current_description text, 
               original_description text, 
               amount real,
               l1 text,
               l2 text,
               l3 text
               )"""
    )

    con.commit()
    con.close()


def insert(
    query: str, data: dict, connection: sqlite3.Connection = None
) -> sqlite3.Connection:
    """Runs an insert query, returning the `connection` if one is provided."""

    auto_commit = False
    if connection is None:
        connection = connect()
        auto_commit = True

    cur = connection.cursor()
    cur.execute(query, data)

    if auto_commit:
        connection.commit()
        connection.close()
    else:
        return connection


def select(query: str, inputs: dict = None) -> list:
    connection = connect()
    connection.row_factory = namedtuple_factory
    cur = connection.cursor()
    if inputs is None:
        cur.execute(query)
    else:
        cur.execute(query, inputs)

    data = cur.fetchall()
    cur.close()

    return data


if __name__ == "__main__":
    init()
