from datetime import datetime
from app.modules.exams.service import get_all_exams

def days_until(date_str):
    target = datetime.strptime(date_str, "%Y-%m-%d")
    today = datetime.now()
    return (target - today).days

def show_countdowns():
    exams = get_all_exams()

    if not exams:
        print("No exams found.")
        return

    for exam in exams:
        course = exam[1]
        exam_date = exam[2]
        signup_start = exam[3]
        signup_end = exam[4]

        print("\n---------------------------")
        print(f"Course: {course}")
        print(f"Days until signup opens: {days_until(signup_start)}")
        print(f"Days until signup closes: {days_until(signup_end)}")
        print(f"Days until exam: {days_until(exam_date)}")
