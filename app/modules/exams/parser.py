from bs4 import BeautifulSoup
from datetime import datetime

def parse_exams(html):
    soup = BeautifulSoup(html, "html.parser")
    exams = []

    tables = soup.find_all("table")

    for table in tables:
        rows = table.find_all("tr")

        for row in rows:
            cols = row.find_all("td")
            if len(cols) < 3:
                continue

            text = row.get_text().lower()

            if "exam" in text:
                try:
                    course = cols[0].get_text(strip=True)
                    date_str = cols[1].get_text(strip=True)

                    exam_date = datetime.strptime(date_str, "%Y-%m-%d")

                    exams.append({
                        "course_code": course,
                        "exam_date": exam_date.strftime("%Y-%m-%d")
                    })
                except Exception:
                    continue

    return exams
