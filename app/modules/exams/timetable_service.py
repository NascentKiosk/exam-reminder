import os
from app.modules.exams.ical_reader import read_ical
from app.data.programs import PROGRAM_NAME_MAP

TIMETABLE_DIR = os.path.join(os.path.dirname(__file__), "timetables")
VALID_SEMESTERS = [1, 2]


def _normalize(code: str) -> str:
    return code.strip().upper()


def list_available_programs_from_ical():
    """
    ONLY list programs that actually have theory exams.
    This guarantees load_timetable will never fail.
    """
    programs = {}

    for filename in os.listdir(TIMETABLE_DIR):
        if not filename.endswith(".ics"):
            continue

        exams = read_ical(os.path.join(TIMETABLE_DIR, filename))

        for exam in exams:
            code = _normalize(exam["program_code"])

            if code in PROGRAM_NAME_MAP and code not in programs:
                meta = PROGRAM_NAME_MAP[code]
                programs[code] = f"{meta['name']} - Year {meta['year']}"

    return programs


def load_timetable(program_code: str, semester: int):
    if semester not in VALID_SEMESTERS:
        raise ValueError("Semester must be 1 or 2")

    program_code = _normalize(program_code)
    courses = []

    for filename in os.listdir(TIMETABLE_DIR):
        if not filename.endswith(".ics"):
            continue

        exams = read_ical(os.path.join(TIMETABLE_DIR, filename))

        for exam in exams:
            if _normalize(exam["program_code"]) == program_code:
                courses.append(exam)

    if not courses:
        raise FileNotFoundError(f"No theory exams found for program {program_code}")

    return courses
