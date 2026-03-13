import requests

URL = "https://schema.hkr.se/setup/jsp/Schema.jsp"

def fetch_timetable_html():
    response = requests.get(URL, timeout=10)
    response.raise_for_status()
    return response.text
