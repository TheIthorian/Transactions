"""Module to interact with the SQLite database."""

from collections import namedtuple
import os
import sqlite3

from app.config import CONFIG


class _State:
    use_mock: bool = False
    print_query: bool = False

    def path(self):
        if _state.use_mock:
            return CONFIG.MOCK_DATABASE_PATH
        if CONFIG.DEMO:
            return CONFIG.DEMO_DATABASE_PATH

        return CONFIG.DATABASE_PATH


_state = _State()


class Database:
    def __init__(self, path: str):
        self.path = path

    def connect(self):
        return sqlite3.connect(self.path)

    def init(self):
        """Creates the database."""
        print("Creating database at: ", self.path)
        con = self.connect()
        cur = con.cursor()

        cur.execute(
            """CREATE TABLE IF NOT EXISTS transactions
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


def namedtuple_factory(cursor: sqlite3.Cursor, row: sqlite3.Row):
    """Returns sqlite rows as named tuples."""
    fields = [col[0] for col in cursor.description]
    Row = namedtuple("Row", fields)
    return Row(*row)


def mock():
    _state.use_mock = True
    _state.print_query = CONFIG.PRINT_QUERIES_IN_TESTS
    init()


def unmock():
    if _state.use_mock:
        delete("DELETE FROM Transactions")

    try:
        os.remove(CONFIG.MOCK_DATABASE_PATH)
    except PermissionError as e:
        print(e)

    _state.use_mock = False
    _state.print_query = False


def connect() -> sqlite3.Connection:
    return sqlite3.connect(_state.path())


def init() -> None:
    """Creates the database."""
    print("Creating database at: ", _state.path())
    con = connect()
    cur = con.cursor()

    cur.execute(
        """CREATE TABLE IF NOT EXISTS transactions
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

    cur.execute(
        """CREATE TABLE IF NOT EXISTS session
                (session_id text NOT NULL,
                last_accessed_date date NOT NULL,
                valid_until_date date NOT NULL
                )"""
    )

    con.commit()
    con.close()


def delete(query: str, inputs: dict = {}, connection: sqlite3.Connection = None):
    if _state.print_query:
        print(query)

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

    if _state.print_query:
        print(query)
        print(data)

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
    if _state.print_query:
        print(query)
        print(inputs)

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
