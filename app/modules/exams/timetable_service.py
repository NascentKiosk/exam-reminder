import os
from app.modules.exams.ical_reader import read_ical, read_all_events
from app.data.programs import PROGRAM_NAME_MAP

TIMETABLE_DIR = os.path.join(os.path.dirname(__file__), "timetables")
VALID_SEMESTERS = [1, 2]


def _normalize(code: str) -> str:
    return code.strip().upper()


def list_available_programs_from_ical():
    programs = {}

    for filename in os.listdir(TIMETABLE_DIR):
        if not filename.endswith(".ics"):
            continue

        events = read_all_events(os.path.join(TIMETABLE_DIR, filename))

        for event in events:
            code = _normalize(event["program_code"])

            if code in PROGRAM_NAME_MAP and code not in programs:
                year = PROGRAM_NAME_MAP[code]["year"]
                name = PROGRAM_NAME_MAP[code]["name"]
                programs[code] = f"{name} - Year {year}"

    return programs


def load_timetable(program_code: str, semester: int):
    if semester not in VALID_SEMESTERS:
        raise ValueError("Semester must be 1 or 2")

    program_code = _normalize(program_code)

    # course_name -> latest exam dict
    course_map = {}

    for filename in os.listdir(TIMETABLE_DIR):
        if not filename.endswith(".ics"):
            continue

        exams = read_ical(os.path.join(TIMETABLE_DIR, filename))

        for exam in exams:
            if _normalize(exam["program_code"]) != program_code:
                continue

            course = exam["course"]
            exam_date = exam["exam_date"]

            # keep the latest date per course
            if (
                course not in course_map
                or exam_date > course_map[course]["exam_date"]
            ):
                course_map[course] = exam

    if not course_map:
        raise FileNotFoundError(f"No exams found for program {program_code}")

    return list(course_map.values())

