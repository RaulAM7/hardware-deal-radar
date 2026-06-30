from __future__ import annotations

from decimal import Decimal

from sqlmodel import Session, select

from hardware_deal_radar.models import AlertDecision, AlertSendResult
from hardware_deal_radar.storage.models import AlertRecord


class AlertsRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def has_strong_alert(self, listing_id: int) -> bool:
        statement = select(AlertRecord).where(
            AlertRecord.listing_id == listing_id,
            AlertRecord.alert_type == "strong",
            AlertRecord.status.in_(["sent", "simulated"]),
        )
        return self.session.exec(statement).first() is not None

    def record_alert(
        self,
        listing_id: int,
        run_id: int | None,
        decision: AlertDecision,
        send_result: AlertSendResult,
        score_total: int,
        estimated_total_eur: Decimal | None,
    ) -> AlertRecord:
        return self.record_event(
            listing_id=listing_id,
            run_id=run_id,
            alert_type=decision.alert_type,
            channel=decision.channel,
            threshold=decision.threshold,
            send_result=send_result,
            score_total=score_total,
            estimated_total_eur=estimated_total_eur,
        )

    def record_event(
        self,
        listing_id: int,
        run_id: int | None,
        alert_type: str,
        channel: str,
        threshold: int | None,
        send_result: AlertSendResult,
        score_total: int,
        estimated_total_eur: Decimal | None,
    ) -> AlertRecord:
        record = AlertRecord(
            listing_id=listing_id,
            run_id=run_id,
            alert_type=alert_type,
            channel=channel,
            threshold=threshold,
            score_at_send=score_total,
            price_at_send=str(estimated_total_eur) if estimated_total_eur is not None else None,
            status=send_result.status,
            sent_at=send_result.sent_at,
            error_message=send_result.error_message,
            payload_preview=send_result.payload_preview,
        )
        self.session.add(record)
        self.session.commit()
        self.session.refresh(record)
        return record
