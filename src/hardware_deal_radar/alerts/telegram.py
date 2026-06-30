from __future__ import annotations

import httpx

from hardware_deal_radar.models import AlertSendResult
from hardware_deal_radar.settings import Settings
from hardware_deal_radar.utils.time import utcnow


class TelegramAlerter:
    def __init__(self, settings: Settings, client: httpx.Client | None = None) -> None:
        self.settings = settings
        self.client = client or httpx.Client(timeout=10.0)

    def send(self, payload: str) -> AlertSendResult:
        token = (
            self.settings.TELEGRAM_BOT_TOKEN.get_secret_value()
            if self.settings.TELEGRAM_BOT_TOKEN
            else ""
        )
        chat_id = (
            self.settings.TELEGRAM_CHAT_ID.get_secret_value()
            if self.settings.TELEGRAM_CHAT_ID
            else ""
        )
        if not token or not chat_id:
            return AlertSendResult(
                status="failed",
                payload_preview=payload[:500],
                error_message="Missing Telegram credentials",
            )
        response = self.client.post(
            f"https://api.telegram.org/bot{token}/sendMessage",
            json={"chat_id": chat_id, "text": payload},
        )
        if response.status_code >= 400:
            return AlertSendResult(
                status="failed",
                payload_preview=payload[:500],
                error_message=f"Telegram send failed with status {response.status_code}",
            )
        return AlertSendResult(status="sent", payload_preview=payload[:500], sent_at=utcnow())
