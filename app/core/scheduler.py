from datetime import datetime
from app.modules.exams.service import get_all_exams


def show_countdowns():
    exams = get_all_exams()
    today = datetime.today()

    if not exams:
        print("No exams found.")
        return

    for exam in exams:
        course, exam_date, signup_start, signup_end, notes = exam

        exam_dt = datetime.strptime(exam_date, "%Y-%m-%d")
        days_left = (exam_dt - today).days

        print("\n-----------------------------")
        print(f"Course: {course}")
        print(f"Exam Date: {exam_date} ({days_left} days left)")
        print(f"Signup opens: {signup_start}")
        print(f"Signup closes: {signup_end}")
        if notes:
            print(f"Notes: {notes}")
