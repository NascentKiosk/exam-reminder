from app.core.notifier import send_email

send_email(
    "mmbasujuma@gmail.com",
    "Test Email",
    "If you received this email, SMTP is working correctly."
)

print("Email function executed.")
