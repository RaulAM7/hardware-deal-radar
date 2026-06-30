from __future__ import annotations

import json
from decimal import Decimal

from sqlmodel import Session, select

from hardware_deal_radar.config.schemas import ScoringConfig
from hardware_deal_radar.models import DigestEntry, ListingCandidate, ScoreResult
from hardware_deal_radar.storage.models import ListingRecord


def collect_digest_candidates(session: Session, scoring: ScoringConfig) -> list[DigestEntry]:
    statement = (
        select(ListingRecord)
        .where(ListingRecord.score_total >= scoring.thresholds.digest)
        .order_by(ListingRecord.last_seen_at.desc())
        .limit(20)
    )
    records = list(session.exec(statement))
    return [
        DigestEntry(
            listing_id=record.id or 0,
            candidate=_to_candidate(record),
            score=_to_score(record),
        )
        for record in records
    ]


def _to_candidate(record: ListingRecord) -> ListingCandidate:
    return ListingCandidate(
        source=record.source,
        marketplace=record.marketplace,
        source_item_id=record.source_item_id,
        canonical_url=record.canonical_url,
        title=record.title,
        seller_username=record.seller_username,
        seller_type=record.seller_type,
        seller_feedback_score=record.seller_feedback_score,
        seller_feedback_percentage=record.seller_feedback_percentage,
        seller_country=record.seller_country,
        item_country=record.item_country,
        condition=record.condition,
        buying_options=json.loads(record.buying_options_json or "[]"),
        currency=record.currency,
        price_amount=Decimal(record.price_amount) if record.price_amount else None,
        shipping_amount=Decimal(record.shipping_amount) if record.shipping_amount else None,
        estimated_total_eur=Decimal(record.estimated_total_eur)
        if record.estimated_total_eur
        else None,
        estimated_import_cost_eur=(
            Decimal(record.estimated_import_cost_eur) if record.estimated_import_cost_eur else None
        ),
        risk_adjustment_eur=Decimal(record.risk_adjustment_eur)
        if record.risk_adjustment_eur
        else None,
        model_family=record.model_family,
        model_generation=record.model_generation,
        cpu_text=record.cpu_text,
        ram_gb=record.ram_gb,
        ssd_gb=record.ssd_gb,
        keyboard_layout=record.keyboard_layout,
        is_thinkpad=record.is_thinkpad,
        is_target_family=record.is_target_family,
        is_business_seller=record.is_business_seller,
        has_returns=record.has_returns,
        has_warranty=record.has_warranty,
        listing_status=record.listing_status,
    )


def _to_score(record: ListingRecord) -> ScoreResult:
    return ScoreResult(
        score_total=record.score_total or 0,
        score_version=record.score_version or "v1",
        positive_reasons=json.loads(record.positive_reasons_json or "[]"),
        negative_reasons=json.loads(record.negative_reasons_json or "[]"),
        risk_flags=json.loads(record.risk_flags_json or "[]"),
        unknown_fields=json.loads(record.unknown_fields_json or "[]"),
        recommendation=record.recommendation or "ignore",
    )
