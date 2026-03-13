from app.core.database import get_connection
from datetime import datetime, timedelta


def calculate_signup_dates(exam_date_str):
    exam_date = datetime.strptime(exam_date_str, "%Y-%m-%d")
    signup_start = exam_date - timedelta(days=50)
    signup_end = exam_date - timedelta(days=14)
    return (
        signup_start.strftime("%Y-%m-%d"),
        signup_end.strftime("%Y-%m-%d")
    )


def add_exam(course_name, exam_date, notes=""):
    signup_start, signup_end = calculate_signup_dates(exam_date)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO exams (course_name, exam_date, signup_start, signup_end, notes)
        VALUES (?, ?, ?, ?, ?)
    """, (course_name, exam_date, signup_start, signup_end, notes))

    conn.commit()
    conn.close()

def get_all_exams():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT course_name, exam_date, signup_start, signup_end, notes
        FROM exams
        ORDER BY exam_date
    """)

    exams = cursor.fetchall()

    conn.close()

    return exams
