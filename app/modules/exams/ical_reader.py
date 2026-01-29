from icalendar import Calendar
from datetime import datetime

def read_ical(file_path):
    exams = []

    with open(file_path, "rb") as f:
        calendar = Calendar.from_ical(f.read())

    for component in calendar.walk():
        if component.name != "VEVENT":
            continue

        summary = str(component.get("summary", ""))

        try:
            raw_program = summary.split("Program:")[1].split("Kurs.grp:")[0].strip()
            program_code = raw_program.split()[0]  # TBSE3

            course = summary.split("Kurs.grp:")[1].split("Sign:")[0].strip()
        except (IndexError, ValueError):
            continue  # Skip malformed entries

        dtstart = component.get("dtstart").dt
        exam_date = dtstart.date() if isinstance(dtstart, datetime) else dtstart

        exams.append({
            "program_code": program_code,
            "course": course,
            "date": exam_date
        })

    return exams
