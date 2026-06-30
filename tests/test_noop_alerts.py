from __future__ import annotations

from hardware_deal_radar.alerts.noop import NoopAlerter


def test_noop_alert_is_simulated() -> None:
    result = NoopAlerter().send("payload")
    assert result.status == "simulated"
    assert result.payload_preview == "payload"
