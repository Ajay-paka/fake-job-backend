import sqlite3
import os

DB_PATH = os.getenv("DB_PATH", "jobs.db")


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT,
            score INTEGER,
            risk TEXT,
            created_at TEXT
        )
    """)

    conn.commit()
    conn.close()