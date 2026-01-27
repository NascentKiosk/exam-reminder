# from app.core.notifier import send_email

# send_email(
#     "mmbasujuma@gmail.com",
#     "Test Email",
#     "If you received this email, SMTP is working correctly."
# )

# print("Email function executed.")


# from app.modules.exams.service import get_or_create_exam

# def test_course(course_code):
#     print(f"\nTesting course: {course_code}")
#     try:
#         exam = get_or_create_exam(course_code)
#         print("SUCCESS")
#         print("Result:", exam)
#     except Exception as e:
#         print("FAILED")
#         print("Error:", e)

# if __name__ == "__main__":
#     # Use a real course code first
#     test_course("MA101C")
#     test_course("DA113H")

#     # Use a fake course to test failure
#     test_course("FAKE999")


# from app.timetable import fetch_exam_date


# courses = ["DA113H", "PYTH110", "FAKE999"]

# for c in courses:
#     try:
#         print(c, "→", fetch_exam_date(c))
#     except Exception as e:
#         print(c, "→ ERROR:", e)


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
    r = requests.get(URL, params=PARAMS, timeout=15)
    r.raise_for_status()
    return r.text


if __name__ == "__main__":
    html = fetch_html()
    with open("data/live_timetable.html", "w", encoding="utf-8") as f:
        f.write(html)

    print("Saved live_timetable.html")
