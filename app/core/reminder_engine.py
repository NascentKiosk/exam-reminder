from datetime import datetime, timedelta, date
from app.core.database import get_connection
from app.core.notifier import send_email


REG_OPEN_DAYS = 50
REG_CLOSE_DAYS = 14


def run_reminders(today: date | None = None, dry_run: bool = False):
    """
    Runs exam signup reminders.

    Args:
        today: override current date (for testing / simulation)
        dry_run: if True, do not send emails or write to DB
    """
    today = today or datetime.today().date()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            s.id,
            s.email,
            e.course_code,
            e.exam_date,
            s.notified_open,
            s.notified_mid,
            s.notified_close
        FROM subscriptions s
        JOIN exams e ON s.course_code = e.course_code
    """)

    for (
        sub_id,
        email,
        course,
        exam_date_raw,
        notified_open,
        notified_mid,
        notified_close
    ) in cur.fetchall():

        exam_date = datetime.fromisoformat(exam_date_raw).date()

        signup_open = exam_date - timedelta(days=REG_OPEN_DAYS)
        signup_close = exam_date - timedelta(days=REG_CLOSE_DAYS)
        midpoint = signup_open + (signup_close - signup_open) / 2

        # --- OPEN ---
        if today == signup_open and not notified_open:
            _notify("OPEN", course, email, today, dry_run)
            if not dry_run:
                send_email(email, "Signup Opened", f"{course} signup is now open.")
                cur.execute(
                    "UPDATE subscriptions SET notified_open=1 WHERE id=?",
                    (sub_id,)
                )

        # --- MID ---
        if today == midpoint and not notified_mid:
            _notify("MID", course, email, today, dry_run)
            if not dry_run:
                send_email(email, "Signup Reminder", f"{course} signup is ongoing.")
                cur.execute(
                    "UPDATE subscriptions SET notified_mid=1 WHERE id=?",
                    (sub_id,)
                )

        # --- CLOSING ---
        if today == signup_close - timedelta(days=3) and not notified_close:
            _notify("CLOSING", course, email, today, dry_run)
            if not dry_run:
                send_email(
                    email,
                    "Signup Closing Soon",
                    f"{course} signup closes in 3 days."
                )
                cur.execute(
                    "UPDATE subscriptions SET notified_close=1 WHERE id=?",
                    (sub_id,)
                )

    if not dry_run:
        conn.commit()
    conn.close()


def _notify(kind, course, email, today, dry_run):
    prefix = "[DRY RUN]" if dry_run else "[SEND]"
    print(f"{prefix} {today} → {kind} → {course} → {email}")
