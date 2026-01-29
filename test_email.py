# from app.core.notifier import send_email

# send_email(
#     "mmbasujuma@gmail.com",
#     "Test Email",
#     "If you received this email, SMTP is working correctly."
# )

# print("Email function executed.")


# from app.modules.exams.service import get_or_create_exam

# def test_course(course_code):
#     print(f"\nTesting course: {course_code}")
#     try:
#         exam = get_or_create_exam(course_code)
#         print("SUCCESS")
#         print("Result:", exam)
#     except Exception as e:
#         print("FAILED")
#         print("Error:", e)

# if __name__ == "__main__":
#     # Use a real course code first
#     test_course("MA101C")
#     test_course("DA113H")

#     # Use a fake course to test failure
#     test_course("FAKE999")


# from app.timetable import fetch_exam_date


# courses = ["DA113H", "PYTH110", "FAKE999"]

# for c in courses:
#     try:
#         print(c, "→", fetch_exam_date(c))
#     except Exception as e:
#         print(c, "→ ERROR:", e)


# import requests

# URL = "https://schema.hkr.se/setup/jsp/Schema.jsp"

# PARAMS = {
#     "startDatum": "idag",
#     "intervallTyp": "a",
#     "intervallAntal": "1",
#     "sokMedAND": "false",
#     "sprak": "SV",
#     "resurser": ""
# }

# def fetch_html():
#     r = requests.get(URL, params=PARAMS, timeout=15)
#     r.raise_for_status()
#     return r.text


# if __name__ == "__main__":
#     html = fetch_html()
#     with open("data/live_timetable.html", "w", encoding="utf-8") as f:
#         f.write(html)

#     print("Saved live_timetable.html")

# from datetime import date, timedelta
# from app.core.reminder_engine import run_reminders

# start = date(2026, 3, 1)
# end = date(2026, 6, 30)

# current = start
# while current <= end:
#     run_reminders(today=current, dry_run=True)
#     current += timedelta(days=1)

# import sqlite3

# conn = sqlite3.connect("path_to_your_db.db")  # <- put your actual DB path here
# cur = conn.cursor()

# cur.execute("PRAGMA table_info(exams);")
# columns = cur.fetchall()

# print("Columns in exams table:")
# for col in columns:
#     print(col[1])  # column name

# conn.close()


from app.core.database import get_connection

conn = get_connection()
cur = conn.cursor()

# Insert exam
cur.execute(
    "INSERT INTO exams (course_code, exam_date) VALUES (?, ?)",
    ("TEST101", "2026-01-20")
)

# Insert subscription
cur.execute(
    "INSERT INTO subscriptions (course_code, email) VALUES (?, ?)",
    ("TEST101", "mmbasujuma@gmail.com")
)

conn.commit()
conn.close()

print("✅ Test data inserted")

