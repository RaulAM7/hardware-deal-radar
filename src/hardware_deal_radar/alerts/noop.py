from __future__ import annotations

from hardware_deal_radar.models import AlertSendResult
from hardware_deal_radar.utils.time import utcnow


class NoopAlerter:
    def send(self, payload: str) -> AlertSendResult:
        return AlertSendResult(status="simulated", payload_preview=payload[:500], sent_at=utcnow())
