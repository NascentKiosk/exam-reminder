import sqlite3
from pathlib import Path

DB_PATH = Path("data/exams.db")

def get_connection():
    DB_PATH.parent.mkdir(exist_ok=True)
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    # Exams table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS exams (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_code TEXT NOT NULL,
        exam_date TEXT NOT NULL
    )
    """)

    # Subscriptions table (ONLY ONCE)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS subscriptions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_code TEXT NOT NULL,
        email TEXT NOT NULL,
        notified_open INTEGER DEFAULT 0,
        notified_mid INTEGER DEFAULT 0,
        notified_close INTEGER DEFAULT 0
    )
    """)
    
    conn.commit()
    conn.close()
