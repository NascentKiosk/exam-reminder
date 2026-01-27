import os
from app.modules.exams.ical_reader import read_ical

TIMETABLE_DIR = os.path.join(os.path.dirname(__file__), "timetables")

def load_timetable(program: str, year: int, semester: int):
    """
    Loads the timetable for a program/year/semester.
    Returns a list of courses with their exam dates.
    """
    filename = f"{program}_{year}_Sem{semester}.ics"
    path = os.path.join(TIMETABLE_DIR, filename)

    if not os.path.exists(path):
        raise FileNotFoundError(f"No timetable found for {program} Year {year} Semester {semester}")

    exams = read_ical(path)
    return exams

def list_available_programs_from_ical():
    """
    Scan all iCal files and extract the programs from the events inside each file.
    Returns a unique sorted list of programs.
    Assumes program code is part of the SUMMARY field: e.g., "CS101 Final Exam"
    """
    programs = set()

    for filename in os.listdir(TIMETABLE_DIR):
        if filename.endswith(".ics"):
            path = os.path.join(TIMETABLE_DIR, filename)
            exams = read_ical(path)  # returns list of dicts {"course":..., "date":...}
            for exam in exams:
                course_name = exam["course"]  # e.g., "CS101 Final Exam"
                # Extract program code: take letters at start of course name
                program_code = "".join([c for c in course_name if c.isalpha()])
                programs.add(program_code.upper())

    return sorted(list(programs))
