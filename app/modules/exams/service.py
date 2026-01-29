# from app.core.database import get_connection
# from datetime import datetime, timedelta


# def calculate_signup_dates(exam_date_str):
#     exam_date = datetime.strptime(exam_date_str, "%Y-%m-%d")
#     signup_start = exam_date - timedelta(days=50)
#     signup_end = exam_date - timedelta(days=14)
#     return (
#         signup_start.strftime("%Y-%m-%d"),
#         signup_end.strftime("%Y-%m-%d")
#     )


# def add_exam(course_name, exam_date, notes=""):
#     signup_start, signup_end = calculate_signup_dates(exam_date)

#     conn = get_connection()
#     cursor = conn.cursor()

#     cursor.execute("""
#         INSERT INTO exams (course_name, exam_date, signup_start, signup_end, notes)
#         VALUES (?, ?, ?, ?, ?)
#     """, (course_name, exam_date, signup_start, signup_end, notes))

#     conn.commit()
#     conn.close()

# def get_all_exams():
#     conn = get_connection()
#     cursor = conn.cursor()

#     cursor.execute("""
#         SELECT course_name, exam_date, signup_start, signup_end, notes
#         FROM exams
#         ORDER BY exam_date
#     """)

#     exams = cursor.fetchall()

#     conn.close()

#     return exams


from app.core.database import get_connection
from datetime import datetime, timedelta
from app.modules.scraper.hkr_scraper import fetch_exam_date


# --------------------------------------------------
# Date calculation logic
# --------------------------------------------------

def calculate_signup_dates(exam_date_str):
    exam_date = datetime.strptime(exam_date_str, "%Y-%m-%d")
    signup_start = exam_date - timedelta(days=50)
    signup_end = exam_date - timedelta(days=14)

    return (
        signup_start.strftime("%Y-%m-%d"),
        signup_end.strftime("%Y-%m-%d")
    )


# --------------------------------------------------
# Database write operations
# --------------------------------------------------

def add_exam(course_name, exam_date, notes=""):
    signup_start, signup_end = calculate_signup_dates(exam_date)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO exams (course_name, exam_date, signup_start, signup_end, notes)
        VALUES (?, ?, ?, ?, ?)
    """, (course_name.upper(), exam_date, signup_start, signup_end, notes))

    conn.commit()
    conn.close()


# --------------------------------------------------
# Database read operations
# --------------------------------------------------

def get_exam_by_course(course_name):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT course_name, exam_date, signup_start, signup_end, notes
        FROM exams
        WHERE course_name = ?
    """, (course_name.upper(),))

    exam = cursor.fetchone()
    conn.close()

    return exam


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


# --------------------------------------------------
# Orchestration logic (CACHE-ASIDE PATTERN)
# --------------------------------------------------

def get_or_create_exam(course_name):
    """
    Returns exam data for a course.
    - If exam exists in DB → use it
    - If not → scrape HKR, store it, then return it
    """

    # 1. Check database first
    exam = get_exam_by_course(course_name)
    if exam:
        return exam

    # 2. Not in DB → scrape external source
    exam_date = fetch_exam_date(course_name)

    # 3. Save scraped data
    add_exam(course_name, exam_date)

    # 4. Fetch again from DB (guaranteed to exist now)
    return get_exam_by_course(course_name)
