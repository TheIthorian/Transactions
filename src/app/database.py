"""Module to interact with the SQLite database.

(C) 2022, TheIthorian, United Kingdom
"""

from collections import namedtuple
import sqlite3

from app.config import CONFIG


class _State:
    use_mock: bool = False

    def path(self):
        if state["use_mock"]:
            return CONFIG.MOCK_DATABASE_PATH
        return CONFIG.DATABASE_PATH


state = _State()


def namedtuple_factory(cursor: sqlite3.Cursor, row: sqlite3.Row):
    """Returns sqlite rows as named tuples."""
    fields = [col[0] for col in cursor.description]
    Row = namedtuple("Row", fields)
    return Row(*row)


def mock():
    state.use_mock = True
    init()


def unmock():
    state.use_mock = False


def connect() -> sqlite3.Connection:
    print("Connecting to database", state.path())
    return sqlite3.connect(state.path())


def init() -> None:
    """Creates the database."""
    print("Creating database at: ", state.path())
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

    con.commit()
    con.close()


def insert(query: str, data: dict, connection: sqlite3.Connection = None) -> int:
    """Runs an insert query, returning the `connection` if one is provided."""

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
