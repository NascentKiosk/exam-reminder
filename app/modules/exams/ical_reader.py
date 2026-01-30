from icalendar import Calendar
from datetime import datetime


def _normalize_program(code: str) -> str:
    return code.strip().upper()


def read_ical(file_path):
    exams = []

    with open(file_path, "rb") as f:
        calendar = Calendar.from_ical(f.read())
for component in calendar.walk("VEVENT"):
    summary = str(component.get("SUMMARY", "")).lower()

    # ✅ ONLY keep real exams
    if "teori" not in summary and "theory" not in summary:
        continue

    try:
        raw_program = summary.split("program:")[1].split("kurs.grp:")[0]
        program_code = _normalize_program(raw_program.split()[0])

        course = summary.split("kurs.grp:")[1].split("sign:")[0].strip()
    except (IndexError, ValueError):
        continue

    dtstart = component.get("DTSTART").dt
    exam_date = dtstart.date() if isinstance(dtstart, datetime) else dtstart

    exams.append({
        "program_code": program_code,
        "course": course,
        "exam_date": exam_date,
        "summary": summary,
    })

    

    return exams


def read_all_events(file_path):
    events = []

    with open(file_path, "rb") as f:
        calendar = Calendar.from_ical(f.read())

    for component in calendar.walk("VEVENT"):
        summary = str(component.get("SUMMARY", ""))

        try:
            raw_program = summary.split("Program:")[1].split("Kurs.grp:")[0]
            program_code = _normalize_program(raw_program.split()[0])

            course = summary.split("Kurs.grp:")[1].split("Sign:")[0].strip()
        except (IndexError, ValueError):
            continue

        events.append({
            "program_code": program_code,
            "course": course,
            "summary": summary,
        })

    return events
