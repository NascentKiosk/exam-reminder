import requests
from bs4 import BeautifulSoup
from datetime import datetime

def fetch_exam_date(course_code):
    url = "https://schema.hkr.se/setup/jsp/Schema.jsp"
    params = {
        "resurser": course_code,
        "sprak": "SV"
    }

    r = requests.get(url, params=params, timeout=10)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")

    # ⚠️ fragile but acceptable for student project
    rows = soup.find_all("tr")
    for row in rows:
        text = row.get_text()
        if "Examination" in text:
            date_str = text.split()[0]
            return datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y-%m-%d")

    raise ValueError("Exam date not found")
