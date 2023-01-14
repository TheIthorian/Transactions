import sqlite3


def migrate(conn: sqlite3.Connection):
    cur = conn.cursor()

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

    conn.commit()
