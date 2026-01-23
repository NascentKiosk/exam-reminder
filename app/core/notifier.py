import smtplib
from email.message import EmailMessage
from os import getenv
from dotenv import load_dotenv

load_dotenv()

EMAIL_ADDRESS = getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = getenv("EMAIL_PASSWORD")

#print("DEBUG EMAIL_ADDRESS:", EMAIL_ADDRESS)
#print("DEBUG EMAIL_PASSWORD:", "SET" if EMAIL_PASSWORD else "NOT SET")

def send_email(to, subject, body):
    msg = EmailMessage()
    msg.set_content(body)
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to
    msg["Subject"] = subject

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)
