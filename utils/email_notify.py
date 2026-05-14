"""
Email notification stub (extend with Flask-Mail or your SMTP provider).

Example production setup:
- Set MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD in the environment
- Send on contact form submit or after resume analysis
"""
from __future__ import annotations

import os
import smtplib
from email.message import EmailMessage


def send_simple_email(to_addr: str, subject: str, body: str) -> bool:
    """
    Send a plain-text email if SMTP env vars are configured; otherwise no-op.

    Env vars (all optional):
        SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, MAIL_FROM
    """
    host = os.getenv("SMTP_HOST")
    port = int(os.getenv("SMTP_PORT", "587"))
    user = os.getenv("SMTP_USER")
    password = os.getenv("SMTP_PASSWORD")
    mail_from = os.getenv("MAIL_FROM", user or "no-reply@localhost")

    if not all([host, user, password]):
        return False

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = mail_from
    msg["To"] = to_addr
    msg.set_content(body)

    try:
        with smtplib.SMTP(host, port, timeout=20) as smtp:
            smtp.starttls()
            smtp.login(user, password)
            smtp.send_message(msg)
        return True
    except Exception:
        return False
