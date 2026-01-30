from app.core.database import get_connection
from app.core.notifier import generate_token


def subscribe(course_code, email, language):
    conn = get_connection()
    cur = conn.cursor()

    unsubscribe_token = generate_token()

    cur.execute(
        """
        INSERT INTO subscriptions (
            course_code,
            email,
            language,
            unsubscribe_token,
            active,
            notified_open,
            notified_mid,
            notified_close
        )
        VALUES (?, ?, ?, ?, 1, 0, 0, 0)
        """,
        (course_code, email, language, unsubscribe_token),
    )

    conn.commit()
    conn.close()

    return unsubscribe_token
