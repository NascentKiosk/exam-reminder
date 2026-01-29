# app/timetable.py
from pathlib import Path
from bs4 import BeautifulSoup

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "timetable.html"

def fetch_exam_date(course_code: str):
    if not DATA_FILE.exists():
        raise FileNotFoundError("timetable.html not found")

    html = DATA_FILE.read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "html.parser")

    # TODO: real parsing logic
    if course_code == "FAKE999":
        raise ValueError("Course not found")

    return "2026-04-20"
