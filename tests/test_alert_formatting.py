from __future__ import annotations

from decimal import Decimal

from hardware_deal_radar.alerts.formatter import format_digest, format_telegram_alert
from hardware_deal_radar.models import DigestEntry, ListingCandidate, ScoreResult


def test_telegram_format_contains_decision_fields() -> None:
    candidate = ListingCandidate(
        marketplace="EBAY_DE",
        title="ThinkPad P14s",
        ram_gb=64,
        ssd_gb=1024,
        cpu_text="Ryzen 7 PRO 7840U",
        seller_username="seller",
        price_amount=Decimal("800"),
        shipping_amount=Decimal("20"),
        estimated_total_eur=Decimal("820"),
        item_country="DE",
        canonical_url="https://example.invalid",
    )
    score = ScoreResult(
        score_total=88,
        positive_reasons=["64GB RAM"],
        risk_flags=["keyboard_layout_risk"],
        recommendation="strong_candidate",
    )
    payload = format_telegram_alert(candidate, score)
    assert "ThinkPad P14s" in payload
    assert "Score: 88/100" in payload


def test_digest_format_handles_empty() -> None:
    payload = format_digest([], "Digest candidates: 0")
    assert "No candidates" in payload


def test_digest_format_lists_entries() -> None:
    entry = DigestEntry(
        listing_id=1,
        candidate=ListingCandidate(
            marketplace="EBAY_DE",
            title="ThinkPad P14s",
            estimated_total_eur=Decimal("899"),
            canonical_url="https://example.invalid",
        ),
        score=ScoreResult(score_total=77, recommendation="watch"),
    )
    payload = format_digest([entry], "Digest candidates: 1")
    assert "ThinkPad P14s" in payload
    assert "Score: 77/100" in payload
