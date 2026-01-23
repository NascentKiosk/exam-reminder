from app.core.database import get_connection

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS exams (
        course_code TEXT PRIMARY KEY,
        exam_date TEXT,
        signup_open TEXT,
        signup_close TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS subscriptions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_code TEXT,
        email TEXT,
        notified_open INTEGER DEFAULT 0,
        notified_mid INTEGER DEFAULT 0,
        notified_close INTEGER DEFAULT 0
    )
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
