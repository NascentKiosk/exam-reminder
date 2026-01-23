import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[2] / "data" / "exams.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS exams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_name TEXT NOT NULL,
            exam_date TEXT NOT NULL,
            signup_start TEXT NOT NULL,
            signup_end TEXT NOT NULL,
            notes TEXT,
            notified_signup_start INTEGER DEFAULT 0,
            notified_signup_end INTEGER DEFAULT 0,
            notified_exam INTEGER DEFAULT 0
        )
    """)

    conn.commit()
    conn.close()
