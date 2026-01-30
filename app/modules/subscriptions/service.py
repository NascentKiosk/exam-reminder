from app.core.database import get_connection

def subscribe(course_code, email, language, unsubscribe_token):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO subscriptions (
            course_code,
            email,
            language,
            unsubscribe_token
        )
        VALUES (?, ?, ?, ?)
    """, (course_code, email, language, unsubscribe_token))

    conn.commit()
    conn.close()
