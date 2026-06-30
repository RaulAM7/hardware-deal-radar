from __future__ import annotations

from datetime import datetime

from sqlmodel import Field, SQLModel


class RunRecord(SQLModel, table=True):
    __tablename__ = "runs"

    id: int | None = Field(default=None, primary_key=True)
    started_at: datetime
    finished_at: datetime | None = None
    status: str
    mode: str
    searches_count: int = 0
    marketplaces_count: int = 0
    raw_results_count: int = 0
    new_listings_count: int = 0
    updated_listings_count: int = 0
    strong_alerts_count: int = 0
    digest_candidates_count: int = 0
    errors_count: int = 0
    summary_json: str = "{}"


class ListingRecord(SQLModel, table=True):
    __tablename__ = "listings"

    id: int | None = Field(default=None, primary_key=True)
    source: str = Field(index=True)
    marketplace: str = Field(index=True)
    source_item_id: str | None = Field(default=None, index=True)
    canonical_url: str | None = Field(default=None, index=True)
    normalized_title: str = Field(default="", index=True)
    title: str
    seller_username: str | None = None
    seller_type: str | None = None
    seller_feedback_score: int | None = None
    seller_feedback_percentage: float | None = None
    seller_country: str | None = None
    item_country: str | None = None
    condition: str | None = None
    buying_options_json: str = "[]"
    currency: str | None = None
    price_amount: str | None = None
    shipping_amount: str | None = None
    estimated_total_eur: str | None = Field(default=None, index=True)
    estimated_import_cost_eur: str | None = None
    risk_adjustment_eur: str | None = None
    model_family: str | None = Field(default=None, index=True)
    model_generation: str | None = None
    cpu_text: str | None = None
    ram_gb: int | None = Field(default=None, index=True)
    ssd_gb: int | None = None
    keyboard_layout: str | None = None
    is_thinkpad: bool = False
    is_target_family: bool = False
    is_business_seller: bool | None = None
    has_returns: bool | None = None
    has_warranty: bool | None = None
    listing_status: str | None = None
    score_total: int | None = Field(default=None, index=True)
    score_version: str | None = None
    positive_reasons_json: str = "[]"
    negative_reasons_json: str = "[]"
    risk_flags_json: str = "[]"
    unknown_fields_json: str = "[]"
    recommendation: str | None = Field(default=None, index=True)
    first_seen_at: datetime
    last_seen_at: datetime
    last_changed_at: datetime | None = None
    raw_payload_json: str = "{}"


class AlertRecord(SQLModel, table=True):
    __tablename__ = "alerts"

    id: int | None = Field(default=None, primary_key=True)
    listing_id: int = Field(foreign_key="listings.id", index=True)
    run_id: int | None = Field(default=None, foreign_key="runs.id")
    alert_type: str
    channel: str
    threshold: int | None = None
    score_at_send: int | None = None
    price_at_send: str | None = None
    status: str = Field(index=True)
    sent_at: datetime | None = None
    error_message: str | None = None
    payload_preview: str = ""


class PriceHistoryRecord(SQLModel, table=True):
    __tablename__ = "price_history"

    id: int | None = Field(default=None, primary_key=True)
    listing_id: int = Field(foreign_key="listings.id", index=True)
    run_id: int = Field(foreign_key="runs.id")
    price_amount: str | None = None
    shipping_amount: str | None = None
    estimated_total_eur: str | None = None
    observed_at: datetime


class ErrorLogRecord(SQLModel, table=True):
    __tablename__ = "error_logs"

    id: int | None = Field(default=None, primary_key=True)
    run_id: int | None = Field(default=None, foreign_key="runs.id")
    source: str | None = None
    marketplace: str | None = None
    error_type: str
    message: str
    created_at: datetime
