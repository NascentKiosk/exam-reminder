# fetch_timetable.py
import requests

URL = "https://schema.hkr.se/setup/jsp/Schema.jsp"
PARAMS = {
    "startDatum": "idag",
    "intervallTyp": "a",
    "intervallAntal": "1",
    "sokMedAND": "false",
    "sprak": "SV",
    "resurser": ""
}

def fetch_html():
    response = requests.get(URL, params=PARAMS, timeout=10)
    response.raise_for_status()
    return response.text

if __name__ == "__main__":
    html = fetch_html()
    with open("timetable.html", "w", encoding="utf-8") as f:
        f.write(html)

    print("Timetable HTML saved")
