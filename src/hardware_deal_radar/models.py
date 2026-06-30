from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import Any

from pydantic import BaseModel, Field


class ListingCandidate(BaseModel):
    source: str = "ebay"
    marketplace: str
    source_item_id: str | None = None
    canonical_url: str | None = None
    title: str
    description: str | None = None
    seller_username: str | None = None
    seller_type: str | None = None
    seller_feedback_score: int | None = None
    seller_feedback_percentage: float | None = None
    seller_country: str | None = None
    item_country: str | None = None
    condition: str | None = None
    buying_options: list[str] = Field(default_factory=list)
    currency: str | None = None
    price_amount: Decimal | None = None
    shipping_amount: Decimal | None = None
    estimated_total_eur: Decimal | None = None
    estimated_import_cost_eur: Decimal | None = None
    risk_adjustment_eur: Decimal | None = None
    model_family: str | None = None
    model_generation: str | None = None
    cpu_text: str | None = None
    ram_gb: int | None = None
    ssd_gb: int | None = None
    keyboard_layout: str | None = None
    is_thinkpad: bool = False
    is_target_family: bool = False
    is_business_seller: bool | None = None
    has_returns: bool | None = None
    has_warranty: bool | None = None
    listing_status: str | None = None
    risk_flags: list[str] = Field(default_factory=list)
    matched_reject_keywords: list[str] = Field(default_factory=list)
    matched_penalty_keywords: list[str] = Field(default_factory=list)
    unknown_fields: list[str] = Field(default_factory=list)
    raw_payload: dict[str, Any] = Field(default_factory=dict)


class ScoreResult(BaseModel):
    score_total: int
    score_version: str = "v1"
    positive_reasons: list[str] = Field(default_factory=list)
    negative_reasons: list[str] = Field(default_factory=list)
    risk_flags: list[str] = Field(default_factory=list)
    unknown_fields: list[str] = Field(default_factory=list)
    recommendation: str


class AlertDecision(BaseModel):
    should_send: bool
    include_in_digest: bool = False
    channel: str
    alert_type: str
    threshold: int | None = None
    reason: str
    status: str


class RunSummary(BaseModel):
    searches_count: int = 0
    marketplaces_count: int = 0
    raw_results_count: int = 0
    new_listings_count: int = 0
    updated_listings_count: int = 0
    strong_alerts_count: int = 0
    digest_candidates_count: int = 0
    errors_count: int = 0
    listings: list[ListingCandidate] = Field(default_factory=list)
    scored: list[tuple[ListingCandidate, ScoreResult]] = Field(default_factory=list)


@dataclass
class UpsertResult:
    listing_id: int
    is_new: bool
    changed_fields: set[str] = field(default_factory=set)
    previous_score_total: int | None = None
    previous_estimated_total_eur: Decimal | None = None
    current_score_total: int | None = None
    current_estimated_total_eur: Decimal | None = None


@dataclass
class AlertSendResult:
    status: str
    payload_preview: str
    error_message: str | None = None
    sent_at: datetime | None = None


@dataclass
class DigestEntry:
    listing_id: int
    candidate: ListingCandidate
    score: ScoreResult
