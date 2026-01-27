from bs4 import BeautifulSoup
from datetime import datetime

def parse_exams(html: str):
    soup = BeautifulSoup(html, "html.parser")
    exams = []

    for row in soup.find_all("tr"):
        cells = [td.get_text(strip=True) for td in row.find_all("td")]

        # Defensive: ignore noise
        if len(cells) < 2:
            continue

        course = cells[0]
        date_text = cells[1]

        # Only keep rows that look like course + date
        try:
            exam_date = datetime.strptime(date_text, "%Y-%m-%d").date()
        except ValueError:
            continue

        exams.append({
            "course_code": course,
            "exam_date": exam_date
        })

    return exams
