from __future__ import annotations

from decimal import Decimal

from hardware_deal_radar.models import AlertDecision, ScoreResult, UpsertResult


def decide_alert(
    score: ScoreResult,
    upsert_result: UpsertResult,
    strong_threshold: int,
    digest_threshold: int,
    has_previous_strong_alert: bool,
) -> AlertDecision:
    if score.recommendation == "reject":
        return AlertDecision(
            should_send=False,
            include_in_digest=False,
            channel="none",
            alert_type="ignore",
            reason="recommendation reject",
            status="skipped",
        )

    if score.score_total >= strong_threshold:
        if not has_previous_strong_alert:
            return AlertDecision(
                should_send=True,
                include_in_digest=True,
                channel="telegram",
                alert_type="strong",
                threshold=strong_threshold,
                reason="strong threshold reached",
                status="pending",
            )
        if _significant_change(upsert_result):
            return AlertDecision(
                should_send=True,
                include_in_digest=True,
                channel="telegram",
                alert_type="strong",
                threshold=strong_threshold,
                reason="significant change after prior strong alert",
                status="pending",
            )
        return AlertDecision(
            should_send=False,
            include_in_digest=True,
            channel="telegram",
            alert_type="strong",
            threshold=strong_threshold,
            reason="duplicate strong alert suppressed",
            status="skipped",
        )

    if score.score_total >= digest_threshold:
        return AlertDecision(
            should_send=False,
            include_in_digest=True,
            channel="email",
            alert_type="digest",
            threshold=digest_threshold,
            reason="digest threshold reached",
            status="pending",
        )

    return AlertDecision(
        should_send=False,
        include_in_digest=False,
        channel="none",
        alert_type="ignore",
        reason="below digest threshold",
        status="skipped",
    )


def _significant_change(result: UpsertResult) -> bool:
    if result.is_new:
        return True
    score_delta = (result.current_score_total or 0) - (result.previous_score_total or 0)
    if score_delta >= 5:
        return True
    current_total = result.current_estimated_total_eur
    previous_total = result.previous_estimated_total_eur
    if current_total is not None and previous_total is not None:
        if previous_total - current_total >= Decimal("20.00"):
            return True
    return any(
        field in result.changed_fields for field in {"condition", "price", "shipping", "returns"}
    )
