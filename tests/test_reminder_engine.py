from datetime import date, timedelta
from app.core.reminder_engine import run_reminders
from app.core.database import init_db, get_connection

def setup_test_data(exam_date):
    init_db()
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO exams (course_code, exam_date) VALUES (?, ?)",
        ("TEST101", exam_date.isoformat())
    )

    cur.execute(
        "INSERT INTO subscriptions (course_code, email) VALUES (?, ?)",
        ("TEST101", "test@example.com")
    )

    conn.commit()
    conn.close()


def test_signup_open_reminder(capsys):
    exam_date = date.today() + timedelta(days=50)
    setup_test_data(exam_date)

    run_reminders(today=date.today(), dry_run=True)

    captured = capsys.readouterr()
    assert "Signup Opened" in captured.out


def test_midpoint_reminder(capsys):
    exam_date = date.today() + timedelta(days=50)
    midpoint = date.today() + timedelta(days=18)
    setup_test_data(exam_date)

    run_reminders(today=midpoint, dry_run=True)

    captured = capsys.readouterr()
    assert "Signup Reminder" in captured.out
