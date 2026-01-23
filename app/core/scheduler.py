from datetime import datetime
from app.core.notifier import send_email
from app.modules.exams.service import get_all_exams
from app.modules.subscriptions.service import get_subscriptions

def run_daily_notifications():
    today = datetime.today().strftime("%Y-%m-%d")

    for exam in get_all_exams():
        for sub in get_subscriptions(exam["course_code"]):
            if today == exam["signup_start"]:
                send_email(
                    sub["email"],
                    f"Signup Open – {exam['course_code']}",
                    "Registration is now open."
                )
