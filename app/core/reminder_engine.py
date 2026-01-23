from datetime import datetime
from app.core.database import get_connection
from app.core.notifier import send_email

def run_reminders():
    today = datetime.today().strftime("%Y-%m-%d")
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    SELECT s.id, s.email, e.course_code, e.signup_open, e.signup_close,
           s.notified_open, s.notified_mid, s.notified_close
    FROM subscriptions s
    JOIN exams e ON s.course_code = e.course_code
    """)

    for row in cur.fetchall():
        sub_id, email, course, open_d, close_d, no, nm, nc = row

        if today == open_d and not no:
            send_email(email, "Signup Opened", f"{course} signup is now open.")
            cur.execute("UPDATE subscriptions SET notified_open=1 WHERE id=?", (sub_id,))

        mid = (datetime.fromisoformat(open_d) + 
               (datetime.fromisoformat(close_d) - datetime.fromisoformat(open_d)) / 2).strftime("%Y-%m-%d")

        if today == mid and not nm:
            send_email(email, "Signup Reminder", f"{course} signup is ongoing.")
            cur.execute("UPDATE subscriptions SET notified_mid=1 WHERE id=?", (sub_id,))

        if today == close_d and not nc:
            send_email(email, "Signup Closing Soon", f"{course} signup closes in 3 days.")
            cur.execute("UPDATE subscriptions SET notified_close=1 WHERE id=?", (sub_id,))

    conn.commit()
    conn.close()
