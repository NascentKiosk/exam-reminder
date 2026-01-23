from app.modules.exams.service import get_all_exams

def show_dashboard():
    exams = get_all_exams()

    if not exams:
        print("No exams found.")
        return

    for exam in exams:
        print("-" * 40)
        print(f"Course: {exam[1]}")
        print(f"Exam date: {exam[2]}")
        print(f"Signup opens: {exam[3]}")
        print(f"Signup closes: {exam[4]}")
