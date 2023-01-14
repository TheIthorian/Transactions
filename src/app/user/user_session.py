from secrets import token_hex
from app import database


def make_user_session() -> str:
    """Replaces the user session with a new one."""

    # Check if session already exists
    query = f"SELECT session_id from Session"
    result = database.select(query)
    if len(result) > 0:
        delete_sessions()

    session_id = token_hex()
    insert_session(session_id)
    return session_id


def delete_sessions():
    database.delete("DELETE FROM Session")


def insert_session(session_id: str):
    print(session_id)
    database.insert(
        f"INSERT INTO Session VALUES ('{session_id}', date(), date('now', '+1 day'))"
    )
