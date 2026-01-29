from datetime import datetime, timedelta, date
from app.core.database import get_connection
from app.core.notifier import send_email

REG_OPEN_DAYS = 50
REG_CLOSE_DAYS = 14


def run_reminders(today: date | None = None, dry_run: bool = False):
    today = today or datetime.today().date()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            s.id,
            s.email,
            s.course_code,
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
        midpoint = signup_open + timedelta(
            days=(signup_close - signup_open).days // 2
        )

        closing_warn = signup_close - timedelta(days=3)

        # OPEN
        if today == signup_open and not notified_open:
            _send(email, course, "Signup Opened", dry_run)
            _mark(cur, "notified_open", sub_id, dry_run)

        # MID
        if today == midpoint and not notified_mid:
            _send(email, course, "Signup Reminder", dry_run)
            _mark(cur, "notified_mid", sub_id, dry_run)

        # CLOSING
        if today == closing_warn and not notified_close:
            _send(email, course, "Signup Closing Soon", dry_run)
            _mark(cur, "notified_close", sub_id, dry_run)

    if not dry_run:
        conn.commit()
    conn.close()


def _send(email, course, subject, dry_run):
    if dry_run:
        print(f"[DRY RUN] {subject} → {course} → {email}")
    else:
        send_email(
            email,
            subject,
            f"Reminder: exam registration for {course}."
        )


def _mark(cur, field, sub_id, dry_run):
    if not dry_run:
        cur.execute(
            f"UPDATE subscriptions SET {field}=1 WHERE id=?",
            (sub_id,)
        )
