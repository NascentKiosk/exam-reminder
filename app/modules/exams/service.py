from app.core.database import get_connection

def add_exam(course_name, exam_date, signup_start, signup_end, notes=""):
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

    cursor.execute("SELECT * FROM exams")
    exams = cursor.fetchall()

    conn.close()
    return exams
