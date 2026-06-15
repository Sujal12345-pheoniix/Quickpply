import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import logging

from app.config import settings

logger = logging.getLogger("app.email_service")

async def send_email(
    to_email: str,
    subject: str,
    body: str,
    attachment_bytes: bytes = None,
    attachment_filename: str = "resume.pdf"
) -> bool:
    """
    Sends an email using the SMTP settings configured in settings.
    If SMTP credentials are not configured, simulates the send in logs.
    """
    if not settings.SMTP_HOST or not settings.SMTP_USERNAME or not settings.SMTP_PASSWORD:
        logger.warning(
            f"SMTP is not fully configured (SMTP_HOST, SMTP_USERNAME, SMTP_PASSWORD missing). "
            f"Simulating email to: {to_email}\nSubject: {subject}\nBody:\n{body[:200]}..."
        )
        # Return True to simulate successful email in development mode
        return True

    try:
        msg = MIMEMultipart()
        msg["From"] = settings.SMTP_FROM or settings.SMTP_USERNAME
        msg["To"] = to_email
        msg["Subject"] = subject

        # Attach body
        msg.attach(MIMEText(body, "plain"))

        # Attach file if provided
        if attachment_bytes:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment_bytes)
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename={attachment_filename}",
            )
            msg.attach(part)

        # Connect and send
        # If port is 587, we typically use TLS; if 465, SSL. Otherwise simple SMTP.
        if settings.SMTP_PORT == 465:
            server = smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT)
        else:
            server = smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT)
            server.ehlo()
            server.starttls()
            server.ehlo()

        server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
        server.sendmail(msg["From"], to_email, msg.as_string())
        server.close()
        
        logger.info(f"Successfully sent email to {to_email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send email to {to_email}: {e}")
        return False
