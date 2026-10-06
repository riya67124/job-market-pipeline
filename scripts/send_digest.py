import os
import smtplib
import ssl
from email.message import EmailMessage
from dotenv import load_dotenv
from digest import build_digest

load_dotenv()

def send_digest():
    sender = os.getenv("EMAIL_SENDER")
    password = os.getenv("EMAIL_APP_PASSWORD")
    receiver = os.getenv("EMAIL_RECEIVER")

    subject, body = build_digest()

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = receiver
    msg.set_content(body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ssl.create_default_context()) as server:
        server.login(sender, password)
        server.send_message(msg)

    print("Digest sent to", receiver)

if __name__ == "__main__":
    send_digest()