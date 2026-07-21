"""Aqui esta el unto de conflicto con email_worker.
"""
# utils/email.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List
from utils.constants import SMTP_SERVER, SMTP_PORT, EMAIL_USER, EMAIL_PASSWORD, validate_constants

for value, name in [(SMTP_SERVER, 'SMTP_SERVER'), (SMTP_PORT, 'SMTP_PORT'), (EMAIL_USER, EMAIL_USER), (EMAIL_PASSWORD, 'EMAIL_PASSWORD')]:
    validate_constants(value, name)

def send_email(
    to: List[str],
    subject: str,
    body: str,
    is_html: bool = False
):
    """Envia un mail.
    """
    msg = MIMEMultipart("alternative")
    msg["From"] = EMAIL_USER
    msg["To"] = ", ".join(to)
    msg["Subject"] = subject

    content = MIMEText(body, "html" if is_html else "plain")
    msg.attach(content)

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASSWORD)
            server.send_message(msg)
        print("✅ Email enviado correctamente")
        return True
    except Exception as e:
        print(f"❌ Error enviando email: {e}")
        return False