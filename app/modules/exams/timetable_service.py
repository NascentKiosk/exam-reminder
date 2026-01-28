import os
from app.modules.exams.ical_reader import read_ical

TIMETABLE_DIR = os.path.join(os.path.dirname(__file__), "timetables")

VALID_YEARS = [1, 2, 3]
VALID_SEMESTERS = [1, 2]

def list_available_programs_from_ical():
    programs = set()

    for filename in os.listdir(TIMETABLE_DIR):
        if filename.endswith(".ics"):
            exams = read_ical(os.path.join(TIMETABLE_DIR, filename))
            for exam in exams:
                programs.add(exam["program"])

    return sorted(programs)

def load_timetable(program: str, year: int, semester: int):
    # Backend validation (important)
    if year not in VALID_YEARS:
        raise ValueError("Year must be between 1 and 3")

    if semester not in VALID_SEMESTERS:
        raise ValueError("Semester must be 1 or 2")

    courses = []

    for filename in os.listdir(TIMETABLE_DIR):
        if filename.endswith(".ics"):
            exams = read_ical(os.path.join(TIMETABLE_DIR, filename))
            for exam in exams:
                if exam["program"] == program:
                    courses.append(exam)

    if not courses:
        raise FileNotFoundError(f"No courses found for program {program}")

    return courses
