from __future__ import annotations

import json
from decimal import Decimal

from sqlmodel import Session, select

from hardware_deal_radar.models import ListingCandidate, ScoreResult, UpsertResult
from hardware_deal_radar.storage.models import ListingRecord, PriceHistoryRecord
from hardware_deal_radar.utils.text import normalized_title
from hardware_deal_radar.utils.time import utcnow


class ListingsRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def upsert_listing(
        self,
        candidate: ListingCandidate,
        score: ScoreResult,
        run_id: int,
    ) -> UpsertResult:
        existing = self._find_existing(candidate)
        now = utcnow()
        if existing is None:
            record = self._record_from_candidate(candidate, score, now, now)
            self.session.add(record)
            self.session.commit()
            self.session.refresh(record)
            self._record_price_history(record.id, run_id, candidate, now)
            return UpsertResult(
                listing_id=record.id or 0,
                is_new=True,
                changed_fields=set(),
                current_score_total=score.score_total,
                current_estimated_total_eur=_to_decimal(record.estimated_total_eur),
            )

        previous_score = existing.score_total
        previous_total = _to_decimal(existing.estimated_total_eur)
        changed_fields = self._apply_candidate(existing, candidate, score, now)
        self.session.add(existing)
        self.session.commit()
        self.session.refresh(existing)
        if {"price", "shipping", "estimated_total_eur"} & changed_fields:
            self._record_price_history(existing.id or 0, run_id, candidate, now)
        return UpsertResult(
            listing_id=existing.id or 0,
            is_new=False,
            changed_fields=changed_fields,
            previous_score_total=previous_score,
            previous_estimated_total_eur=previous_total,
            current_score_total=existing.score_total,
            current_estimated_total_eur=_to_decimal(existing.estimated_total_eur),
        )

    def list_recent(self, limit: int = 20) -> list[ListingRecord]:
        statement = select(ListingRecord).order_by(ListingRecord.last_seen_at.desc()).limit(limit)
        return list(self.session.exec(statement))

    def get_listing(self, listing_id: int) -> ListingRecord | None:
        return self.session.get(ListingRecord, listing_id)

    def _find_existing(self, candidate: ListingCandidate) -> ListingRecord | None:
        if candidate.source_item_id:
            statement = select(ListingRecord).where(
                ListingRecord.source == candidate.source,
                ListingRecord.marketplace == candidate.marketplace,
                ListingRecord.source_item_id == candidate.source_item_id,
            )
            record = self.session.exec(statement).first()
            if record:
                return record
        if candidate.canonical_url:
            statement = select(ListingRecord).where(
                ListingRecord.canonical_url == candidate.canonical_url
            )
            record = self.session.exec(statement).first()
            if record:
                return record
        statement = select(ListingRecord).where(
            ListingRecord.marketplace == candidate.marketplace,
            ListingRecord.seller_username == candidate.seller_username,
            ListingRecord.normalized_title == normalized_title(candidate.title),
            ListingRecord.price_amount == _decimal_to_str(candidate.price_amount),
        )
        return self.session.exec(statement).first()

    def _record_from_candidate(
        self,
        candidate: ListingCandidate,
        score: ScoreResult,
        first_seen,
        last_seen,
    ) -> ListingRecord:
        return ListingRecord(
            source=candidate.source,
            marketplace=candidate.marketplace,
            source_item_id=candidate.source_item_id,
            canonical_url=candidate.canonical_url,
            normalized_title=normalized_title(candidate.title),
            title=candidate.title,
            seller_username=candidate.seller_username,
            seller_type=candidate.seller_type,
            seller_feedback_score=candidate.seller_feedback_score,
            seller_feedback_percentage=candidate.seller_feedback_percentage,
            seller_country=candidate.seller_country,
            item_country=candidate.item_country,
            condition=candidate.condition,
            buying_options_json=json.dumps(candidate.buying_options),
            currency=candidate.currency,
            price_amount=_decimal_to_str(candidate.price_amount),
            shipping_amount=_decimal_to_str(candidate.shipping_amount),
            estimated_total_eur=_decimal_to_str(candidate.estimated_total_eur),
            estimated_import_cost_eur=_decimal_to_str(candidate.estimated_import_cost_eur),
            risk_adjustment_eur=_decimal_to_str(candidate.risk_adjustment_eur),
            model_family=candidate.model_family,
            model_generation=candidate.model_generation,
            cpu_text=candidate.cpu_text,
            ram_gb=candidate.ram_gb,
            ssd_gb=candidate.ssd_gb,
            keyboard_layout=candidate.keyboard_layout,
            is_thinkpad=candidate.is_thinkpad,
            is_target_family=candidate.is_target_family,
            is_business_seller=candidate.is_business_seller,
            has_returns=candidate.has_returns,
            has_warranty=candidate.has_warranty,
            listing_status=candidate.listing_status,
            score_total=score.score_total,
            score_version=score.score_version,
            positive_reasons_json=json.dumps(score.positive_reasons),
            negative_reasons_json=json.dumps(score.negative_reasons),
            risk_flags_json=json.dumps(score.risk_flags),
            unknown_fields_json=json.dumps(score.unknown_fields),
            recommendation=score.recommendation,
            first_seen_at=first_seen,
            last_seen_at=last_seen,
            last_changed_at=last_seen,
            raw_payload_json=json.dumps(candidate.raw_payload, default=str),
        )

    def _apply_candidate(
        self,
        record: ListingRecord,
        candidate: ListingCandidate,
        score: ScoreResult,
        observed_at,
    ) -> set[str]:
        changed: set[str] = set()
        fields = {
            "title": candidate.title,
            "seller_username": candidate.seller_username,
            "seller_type": candidate.seller_type,
            "seller_feedback_score": candidate.seller_feedback_score,
            "seller_feedback_percentage": candidate.seller_feedback_percentage,
            "seller_country": candidate.seller_country,
            "item_country": candidate.item_country,
            "condition": candidate.condition,
            "currency": candidate.currency,
            "price_amount": _decimal_to_str(candidate.price_amount),
            "shipping_amount": _decimal_to_str(candidate.shipping_amount),
            "estimated_total_eur": _decimal_to_str(candidate.estimated_total_eur),
            "estimated_import_cost_eur": _decimal_to_str(candidate.estimated_import_cost_eur),
            "risk_adjustment_eur": _decimal_to_str(candidate.risk_adjustment_eur),
            "model_family": candidate.model_family,
            "model_generation": candidate.model_generation,
            "cpu_text": candidate.cpu_text,
            "ram_gb": candidate.ram_gb,
            "ssd_gb": candidate.ssd_gb,
            "keyboard_layout": candidate.keyboard_layout,
            "is_thinkpad": candidate.is_thinkpad,
            "is_target_family": candidate.is_target_family,
            "is_business_seller": candidate.is_business_seller,
            "has_returns": candidate.has_returns,
            "has_warranty": candidate.has_warranty,
            "listing_status": candidate.listing_status,
            "score_total": score.score_total,
            "score_version": score.score_version,
            "recommendation": score.recommendation,
            "buying_options_json": json.dumps(candidate.buying_options),
            "positive_reasons_json": json.dumps(score.positive_reasons),
            "negative_reasons_json": json.dumps(score.negative_reasons),
            "risk_flags_json": json.dumps(score.risk_flags),
            "unknown_fields_json": json.dumps(score.unknown_fields),
            "raw_payload_json": json.dumps(candidate.raw_payload, default=str),
            "normalized_title": normalized_title(candidate.title),
        }
        field_aliases = {
            "price_amount": "price",
            "shipping_amount": "shipping",
            "estimated_total_eur": "estimated_total_eur",
        }
        for name, value in fields.items():
            if getattr(record, name) != value:
                setattr(record, name, value)
                changed.add(field_aliases.get(name, name))
        record.last_seen_at = observed_at
        if changed:
            record.last_changed_at = observed_at
        return changed

    def _record_price_history(
        self, listing_id: int, run_id: int, candidate: ListingCandidate, observed_at
    ) -> None:
        history = PriceHistoryRecord(
            listing_id=listing_id,
            run_id=run_id,
            price_amount=_decimal_to_str(candidate.price_amount),
            shipping_amount=_decimal_to_str(candidate.shipping_amount),
            estimated_total_eur=_decimal_to_str(candidate.estimated_total_eur),
            observed_at=observed_at,
        )
        self.session.add(history)
        self.session.commit()


def _decimal_to_str(value: Decimal | None) -> str | None:
    return str(value) if value is not None else None


def _to_decimal(value: str | None) -> Decimal | None:
    return Decimal(value) if value is not None else None
