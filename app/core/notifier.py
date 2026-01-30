import smtplib
from email.message import EmailMessage
from os import getenv
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

EMAIL_ADDRESS = getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = getenv("EMAIL_PASSWORD")

TEMPLATE_DIR = Path("app/templates")


def load_template(template_name: str, **variables) -> str:
    """
    Loads an email template and replaces {{ variables }}.
    """
    template_path = TEMPLATE_DIR / template_name
    text = template_path.read_text(encoding="utf-8")

    for key, value in variables.items():
        text = text.replace(f"{{{{ {key} }}}}", str(value))

    return text


def send_email(to, subject, body):
    msg = EmailMessage()
    msg.set_content(body)
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to
    msg["Subject"] = subject

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)
