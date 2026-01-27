from icalendar import Calendar
from datetime import datetime

def read_ical(file_path):
    exams = []

    with open(file_path, "rb") as f:
        calendar = Calendar.from_ical(f.read())

    for component in calendar.walk():
        if component.name == "VEVENT":
            summary = str(component.get("summary"))
            dtstart = component.get("dtstart").dt

            # Handle datetime vs date
            if isinstance(dtstart, datetime):
                exam_date = dtstart.date()
            else:
                exam_date = dtstart

            exams.append({
                "course": summary,
                "date": exam_date
            })

    return exams
