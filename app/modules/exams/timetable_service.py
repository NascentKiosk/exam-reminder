import os
from app.modules.exams.ical_reader import read_ical
from app.data.programs import PROGRAM_NAME_MAP

TIMETABLE_DIR = os.path.join(os.path.dirname(__file__), "timetables")

VALID_YEARS = [1, 2, 3]
VALID_SEMESTERS = [1, 2]

def list_available_programs_from_ical():
    """
    Returns:
        dict { program_code: display_name } for each year
        e.g. { "TBSE1": "Bachelor Programme in Software Development - Year 1", ... }
    """
    programs = {}

    for filename in os.listdir(TIMETABLE_DIR):
        if not filename.endswith(".ics"):
            continue

        exams = read_ical(os.path.join(TIMETABLE_DIR, filename))
        for exam in exams:
            code = exam["program_code"]
            if code in PROGRAM_NAME_MAP:
                year = PROGRAM_NAME_MAP[code]["year"]
                display_name = f"{PROGRAM_NAME_MAP[code]['name']} - Year {year}"
                # Only add if not already added
                if code not in programs:
                    programs[code] = display_name

    return programs



def load_timetable(program_code: str, year: int, semester: int):
    if year not in VALID_YEARS:
        raise ValueError("Year must be between 1 and 3")
    if semester not in VALID_SEMESTERS:
        raise ValueError("Semester must be 1 or 2")

    courses = []

    for filename in os.listdir(TIMETABLE_DIR):
        if not filename.endswith(".ics"):
            continue

        exams = read_ical(os.path.join(TIMETABLE_DIR, filename))
        for exam in exams:
            # Check both program code and year
            if exam["program_code"] == program_code and PROGRAM_NAME_MAP[program_code]["year"] == year:
                courses.append(exam)

    if not courses:
        raise FileNotFoundError("No courses found for selected program/year")

    return courses

