from __future__ import annotations

from decimal import Decimal

from hardware_deal_radar.models import ScoreResult, UpsertResult
from hardware_deal_radar.pipeline.alert_decision import decide_alert


def test_strong_alert_sent_once() -> None:
    decision = decide_alert(
        ScoreResult(score_total=90, recommendation="strong_candidate"),
        UpsertResult(listing_id=1, is_new=True),
        strong_threshold=80,
        digest_threshold=60,
        has_previous_strong_alert=False,
    )
    assert decision.should_send is True
    assert decision.channel == "telegram"


def test_price_drop_realerts() -> None:
    decision = decide_alert(
        ScoreResult(score_total=88, recommendation="strong_candidate"),
        UpsertResult(
            listing_id=1,
            is_new=False,
            previous_estimated_total_eur=Decimal("900"),
            current_estimated_total_eur=Decimal("850"),
        ),
        strong_threshold=80,
        digest_threshold=60,
        has_previous_strong_alert=True,
    )
    assert decision.should_send is True
