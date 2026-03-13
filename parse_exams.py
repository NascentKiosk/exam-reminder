from bs4 import BeautifulSoup
from datetime import datetime

def parse_exams(html):
    soup = BeautifulSoup(html, "html.parser")

    exams = []

    tables = soup.find_all("table")
    for table in tables:
        rows = table.find_all("tr")

        for row in rows:
            cells = [c.get_text(strip=True) for c in row.find_all("td")]
            if not cells:
                continue

            # This part WILL change after inspection
            if "Tentamen" in " ".join(cells):
                try:
                    course_code = cells[0]
                    exam_date = datetime.strptime(cells[1], "%Y-%m-%d").date()

                    exams.append({
                        "course_code": course_code,
                        "exam_date": exam_date
                    })
                except Exception:
                    continue

    return exams
