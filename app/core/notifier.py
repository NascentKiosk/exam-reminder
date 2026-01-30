import smtplib
import secrets
from email.message import EmailMessage
from os import getenv
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

EMAIL_ADDRESS = getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = getenv("EMAIL_PASSWORD")

TEMPLATE_DIR = Path("app/templates")


def generate_token() -> str:
    return secrets.token_urlsafe(24)


def load_template( language: str, template_name: str, **variables) -> str:
   
    if language not in ("en", "sv"):
        language = "en"

    template_path = TEMPLATE_DIR / language / template_name
    text = template_path.read_text(encoding="utf-8")

    for key, value in variables.items():
        text = text.replace(f"{{{{ {key} }}}}", str(value))

    return text


def send_email(to: str, subject: str, body: str):
    if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
        raise RuntimeError("Email credentials not set")

    msg = EmailMessage()
    msg.set_content(body)
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to
    msg["Subject"] = subject

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)


def send_confirmation_email(
    email: str,
    language: str,
    courses: list[str],
    unsubscribe_token: str,
    base_url: str
):
    subject = (
        "Exam Reminder Subscription Confirmed"
        if language == "en"
        else "Bekräftelse: Tentapåminnelse"
    )

    unsubscribe_url = f"{base_url}/?unsubscribe={unsubscribe_token}"

    body = load_template(
        language,
        "confirmation.txt",
        courses=", ".join(courses),
        unsubscribe_url=unsubscribe_url
    )

    send_email(email, subject, body)
