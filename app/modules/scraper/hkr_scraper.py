import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re


EXAM_KEYWORDS = [
    "tentamen",
    "examination",
    "exam",
    "skrivning"
]


def fetch_exam_date(course_code):
    """
    Attempts to fetch an exam date for a course from HKR schema.
    Best-effort scraping. Falls back to manual entry if not found.
    """

    url = "https://schema.hkr.se/setup/jsp/Schema.jsp"
    params = {
        "resurser": course_code,
        "sprak": "SV"
    }

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    rows = soup.find_all("tr")

    for row in rows:
        text = row.get_text(" ").lower()

        # Check if row looks like an exam
        if any(keyword in text for keyword in EXAM_KEYWORDS):

            # Look for YYYY-MM-DD pattern anywhere in row
            match = re.search(r"\d{4}-\d{2}-\d{2}", text)
            if match:
                exam_date = match.group()
                # Validate date format
                datetime.strptime(exam_date, "%Y-%m-%d")
                return exam_date

    raise ValueError(
        f"Could not automatically find exam date for course '{course_code}'. "
        "HKR schema does not reliably expose exam dates."
    )
