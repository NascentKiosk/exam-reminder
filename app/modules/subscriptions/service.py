from app.core.database import get_connection


def subscribe(course_code, email, language, unsubscribe_token):
    conn = get_connection()
    cur = conn.cursor()

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


def get_subscriptions(active_only: bool = True):
    """
    Returns all subscriptions.
    Used by reminder engine.
    """
    conn = get_connection()
    cur = conn.cursor()

    if active_only:
        cur.execute(
            """
            SELECT
                id,
                course_code,
                email,
                language,
                unsubscribe_token,
                notified_open,
                notified_mid,
                notified_close
            FROM subscriptions
            WHERE active = 1
            """
        )
    else:
        cur.execute(
            """
            SELECT
                id,
                course_code,
                email,
                language,
                unsubscribe_token,
                notified_open,
                notified_mid,
                notified_close,
                active
            FROM subscriptions
            """
        )

    rows = cur.fetchall()
    conn.close()
    return rows
