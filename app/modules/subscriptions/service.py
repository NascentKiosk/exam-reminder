import sqlite3
from app.core.database import get_connection

def subscribe(course_code, email):
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
        INSERT INTO subscriptions (course_code, email)
        VALUES (?, ?)
        """, (course_code.upper(), email))

        conn.commit()

    except sqlite3.IntegrityError:
        raise ValueError("You are already subscribed to this course.")

    finally:
        conn.close()
