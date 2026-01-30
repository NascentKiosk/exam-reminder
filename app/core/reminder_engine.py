from datetime import datetime, timedelta, date

from app.core.database import get_connection, init_db
from app.core.notifier import send_email, load_template


REG_OPEN_DAYS = 50
REG_CLOSE_DAYS = 14


def run_reminders(today: date | None = None, dry_run: bool = False):
    init_db()

    today = today or datetime.today().date()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            s.id,
            s.email,
            s.course_code,
            s.language,
            e.exam_date,
            s.notified_open,
            s.notified_mid,
            s.notified_close
        FROM subscriptions s
        JOIN exams e ON s.course_code = e.course_code
        WHERE s.active = 1
    """)

    for (
        sub_id,
        email,
        course,
        language,
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

        # --- SIGNUP OPEN ---
        if today == signup_open and not notified_open:
            _send(
                email=email,
                course=course,
                language=language,
                subject="Signup Opened",
                template_name="signup_open.txt",
                exam_date=exam_date,
                dry_run=dry_run
            )
            _mark(cur, "notified_open", sub_id, dry_run)

        # --- MID REMINDER ---
        if today == midpoint and not notified_mid:
            _send(
                email=email,
                course=course,
                language=language,
                subject="Signup Reminder",
                template_name="signup_mid.txt",
                exam_date=exam_date,
                dry_run=dry_run
            )
            _mark(cur, "notified_mid", sub_id, dry_run)

        # --- CLOSING WARNING ---
        if today == closing_warn and not notified_close:
            _send(
                email=email,
                course=course,
                language=language,
                subject="Signup Closing Soon",
                template_name="signup_closing.txt",
                exam_date=exam_date,
                dry_run=dry_run
            )
            _mark(cur, "notified_close", sub_id, dry_run)

    if not dry_run:
        conn.commit()

    conn.close()


def _send(
    *,
    email: str,
    course: str,
    language: str,
    subject: str,
    template_name: str,
    exam_date: date,
    dry_run: bool
):
    body = load_template(
        language=language,
        template_name=template_name,
        course=course,
        exam_date=exam_date
    )

    if dry_run:
        print(f"[DRY RUN] {subject} → {course} → {email}")
    else:
        send_email(email, subject, body)


def _mark(cur, field: str, sub_id: int, dry_run: bool):
    if not dry_run:
        cur.execute(
            f"UPDATE subscriptions SET {field} = 1 WHERE id = ?",
            (sub_id,)
        )
