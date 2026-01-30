from app.core.database import get_connection

def unsubscribe(token: str):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE subscriptions
        SET active = 0
        WHERE unsubscribe_token = ?
        """,
        (token,)
    )

    conn.commit()
    conn.close()
