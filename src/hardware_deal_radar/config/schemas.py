from __future__ import annotations

from pydantic import BaseModel, Field, field_validator, model_validator


class SearchConfig(BaseModel):
    name: str
    enabled: bool = True
    query: str
    marketplaces: list[str]
    min_ram_gb: int = 32
    preferred_ram_gb: int = 64
    max_estimated_total_eur: float | None = None
    strong_alert_threshold: int | None = None
    digest_threshold: int | None = None
    positive_keywords: list[str] = Field(default_factory=list)
    negative_keywords: list[str] = Field(default_factory=list)
    target_families: list[str] = Field(default_factory=list)
    exclusions: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_ram_thresholds(self) -> SearchConfig:
        if self.min_ram_gb <= 0:
            raise ValueError("min_ram_gb must be positive")
        if self.preferred_ram_gb < self.min_ram_gb:
            raise ValueError("preferred_ram_gb must be >= min_ram_gb")
        return self


class SearchesFile(BaseModel):
    searches: list[SearchConfig]


class Thresholds(BaseModel):
    strong_alert: int
    digest: int
    ignore_below: int

    @model_validator(mode="after")
    def validate_order(self) -> Thresholds:
        if not (self.strong_alert > self.digest > self.ignore_below):
            raise ValueError("thresholds must satisfy strong_alert > digest > ignore_below")
        return self


class RamPoints(BaseModel):
    below_minimum: int
    minimum: int
    preferred: int


class RamConfig(BaseModel):
    minimum_gb: int
    preferred_gb: int
    points: RamPoints

    @model_validator(mode="after")
    def validate_ram(self) -> RamConfig:
        if self.minimum_gb <= 0:
            raise ValueError("minimum_gb must be positive")
        if self.preferred_gb < self.minimum_gb:
            raise ValueError("preferred_gb must be >= minimum_gb")
        return self


class StoragePoints(BaseModel):
    ssd_512gb: int = 4
    ssd_1tb: int = 8
    ssd_2tb: int = 10


class StorageConfig(BaseModel):
    points: StoragePoints


class SellerConfig(BaseModel):
    business_seller: int = 10
    feedback_percentage_99_plus: int = 8
    feedback_percentage_97_plus: int = 5
    feedback_low_penalty: int = -10
    returns_accepted: int = 7
    warranty_available: int = 5


class NegativeKeywordConfig(BaseModel):
    reject: list[str] = Field(default_factory=list)
    penalize: list[str] = Field(default_factory=list)


class ScoringConfig(BaseModel):
    thresholds: Thresholds
    ram: RamConfig
    storage: StorageConfig
    seller: SellerConfig
    marketplace: dict[str, int]
    keyboard: dict[str, int]
    negative_keywords: NegativeKeywordConfig


class MarketplaceConfig(BaseModel):
    label: str
    country: str
    currency: str
    marketplace_id: str
    base_risk_penalty: int = 0
    import_risk_penalty: int = 0
    keyboard_risk_penalty: int = 0
    eur_exchange_rate: float = 1.0
    in_eu: bool = True
    language: str | None = None
    notes: str | None = None

    @field_validator("currency")
    @classmethod
    def uppercase_currency(cls, value: str) -> str:
        return value.upper()


class MarketplacesFile(BaseModel):
    marketplaces: dict[str, MarketplaceConfig]
