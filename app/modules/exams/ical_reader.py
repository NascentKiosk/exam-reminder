from icalendar import Calendar
from datetime import datetime

def read_ical(file_path):
    exams = []

    with open(file_path, "rb") as f:
        calendar = Calendar.from_ical(f.read())

    for component in calendar.walk():
        if component.name == "VEVENT":
            summary = str(component.get("summary", ""))

            program = None
            course = None

            # Parse structured fields from SUMMARY
            if "Program:" in summary and "Kurs.grp:" in summary:
                try:
                    program = summary.split("Program:")[1].split("Kurs.grp:")[0].strip()
                    course = summary.split("Kurs.grp:")[1].split("Sign:")[0].strip()
                except IndexError:
                    continue  # skip malformed entries

            dtstart = component.get("dtstart").dt
            exam_date = dtstart.date() if isinstance(dtstart, datetime) else dtstart

            if program and course:
                exams.append({
                    "program": program,
                    "course": course,
                    "date": exam_date
                })

    return exams
