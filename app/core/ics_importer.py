from ics import Calendar
from datetime import timedelta
from app.core.database import get_connection

REG_OPEN_DAYS = 50
REG_CLOSE_DAYS = 14

def import_ics(path):
    with open(path, "r", encoding="utf-8") as f:
        calendar = Calendar(f.read())

    conn = get_connection()
    cur = conn.cursor()

    for event in calendar.events:
        course = event.name
        exam_date = event.begin.date()

        cur.execute(
            "INSERT OR IGNORE INTO exams (course_code, exam_date) VALUES (?, ?)",
            (course, exam_date.isoformat())
        )

    conn.commit()
    conn.close()
