from datetime import datetime, timedelta

def calculate_signup_window(exam_date_str):
    exam_date = datetime.strptime(exam_date_str, "%Y-%m-%d")
    signup_open = exam_date - timedelta(days=50)
    signup_close = exam_date - timedelta(days=14)

    return (
        signup_open.strftime("%Y-%m-%d"),
        signup_close.strftime("%Y-%m-%d")
    )
