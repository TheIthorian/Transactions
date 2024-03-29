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

    cur.execute(
        """CREATE TABLE IF NOT EXISTS budget
                (budget_id INTEGER PRIMARY KEY,
                name TEXT,
                total_limit INTEGER
                )"""
    )

    cur.execute(
        """CREATE TABLE IF NOT EXISTS BudgetItem
                (budget_item_id INTEGER PRIMARY KEY,
                budget_id INTEGER,
                l1 text NOT NULL,
                amount INTEGER NOT NULL,
                FOREIGN KEY(budget_id) REFERENCES Budget(budget_id)
                )"""
    )

    cur.execute(
        """CREATE TABLE IF NOT EXISTS Uploads
                (upload_id INTEGER PRIMARY KEY,
                filename TEXT NOT NULL,
                size INTEGER NOT NULL,
                date Date NOT NULL,
                md5 TEXT NOT NULL,
                status TEXT NOT NULL
                )"""
    )

    conn.commit()
