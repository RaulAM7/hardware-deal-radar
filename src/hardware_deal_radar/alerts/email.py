from __future__ import annotations

import smtplib
from email.message import EmailMessage

from hardware_deal_radar.models import AlertSendResult
from hardware_deal_radar.settings import Settings
from hardware_deal_radar.utils.time import utcnow


class EmailAlerter:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def send(self, payload: str, subject: str = "Hardware Deal Radar digest") -> AlertSendResult:
        if (
            not self.settings.SMTP_HOST
            or not self.settings.SMTP_FROM
            or not self.settings.DIGEST_EMAIL_TO
        ):
            return AlertSendResult(
                status="failed",
                payload_preview=payload[:500],
                error_message="Missing SMTP configuration",
            )
        message = EmailMessage()
        message["Subject"] = subject
        message["From"] = self.settings.SMTP_FROM
        message["To"] = self.settings.DIGEST_EMAIL_TO
        message.set_content(payload)
        try:
            with smtplib.SMTP(self.settings.SMTP_HOST, self.settings.SMTP_PORT, timeout=10) as smtp:
                smtp.starttls()
                if self.settings.SMTP_USERNAME and self.settings.SMTP_PASSWORD:
                    smtp.login(
                        self.settings.SMTP_USERNAME,
                        self.settings.SMTP_PASSWORD.get_secret_value(),
                    )
                smtp.send_message(message)
        except OSError as exc:
            return AlertSendResult(
                status="failed",
                payload_preview=payload[:500],
                error_message=f"Email send failed: {exc.__class__.__name__}",
            )
        return AlertSendResult(status="sent", payload_preview=payload[:500], sent_at=utcnow())
