"""Module to interact with the SQLite database."""

from collections import namedtuple
import sqlite3

from app.config import CONFIG
from app.migrations import migrate


class Database:
    def __init__(self, path: str):
        self.path = path

    def connect(self):
        return sqlite3.connect(self.path)

    def init(self):
        """Creates the database."""
        print("Creating database at: ", self.path)
        con = self.connect()
        migrate(con)
        con.close()


def namedtuple_factory(cursor: sqlite3.Cursor, row: sqlite3.Row):
    """Returns sqlite rows as named tuples."""
    fields = [col[0] for col in cursor.description]
    Row = namedtuple("Row", fields)
    return Row(*row)


def clean_mock():
    if CONFIG.DATABASE_PATH == CONFIG.MOCK_DATABASE_PATH:
        delete("DELETE FROM Transactions")
        delete("DELETE FROM Session")


def connect() -> sqlite3.Connection:
    return sqlite3.connect(CONFIG.DATABASE_PATH)


def init() -> None:
    """Creates the database."""
    print("Creating database at: ", CONFIG.DATABASE_PATH)
    con = connect()
    migrate(con)
    con.close()


def print_query(query: str, inputs: dict = {}):
    if CONFIG.PRINT_QUERIES:
        print(query)
        print(inputs)
        print(CONFIG.DATABASE_PATH)


def delete(query: str, inputs: dict = {}, connection: sqlite3.Connection = None):
    print_query(query, inputs)

    auto_commit = False
    if connection is None:
        connection = connect()
        auto_commit = True

    cur = connection.cursor()
    cur.execute(query, inputs)

    if auto_commit:
        connection.commit()
        connection.close()


def insert(query: str, data: dict = {}, connection: sqlite3.Connection = None) -> int:
    """
    Runs an insert query, returning the `id`.
    Keeps the connection open if one is provided
    """
    print_query(query)

    if CONFIG.DATABASE_PATH != CONFIG.MOCK_DATABASE_PATH:
        print("Wrong db")

    auto_commit = False
    if connection is None:
        connection = connect()
        auto_commit = True

    cur = connection.cursor()
    cur.execute(query, data)
    id = cur.lastrowid

    # Keep connection alive if a connection is provided
    if auto_commit:
        connection.commit()
        connection.close()

    return id


def select(query: str, inputs: dict = None) -> list:
    print_query(query, inputs)

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
