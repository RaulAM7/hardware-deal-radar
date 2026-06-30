from __future__ import annotations

from hardware_deal_radar.config.schemas import MarketplaceConfig, ScoringConfig
from hardware_deal_radar.models import ListingCandidate
from hardware_deal_radar.pipeline.cost import apply_cost_estimate
from hardware_deal_radar.pipeline.enrich import enrich_candidate
from hardware_deal_radar.sources.base import RawListing
from hardware_deal_radar.utils.money import to_decimal
from hardware_deal_radar.utils.text import canonicalize_url


def normalize_item(
    raw_listing: RawListing,
    marketplace: MarketplaceConfig,
    scoring: ScoringConfig,
) -> ListingCandidate:
    payload = raw_listing.payload
    seller = payload.get("seller", {})
    shipping_options = payload.get("shippingOptions") or []
    shipping_cost = None
    if shipping_options:
        shipping_cost = shipping_options[0].get("shippingCost", {}).get("value")

    candidate = ListingCandidate(
        source=raw_listing.source,
        marketplace=raw_listing.marketplace,
        source_item_id=payload.get("itemId"),
        canonical_url=canonicalize_url(payload.get("itemWebUrl")),
        title=payload.get("title", ""),
        description=payload.get("shortDescription") or payload.get("subtitle"),
        seller_username=seller.get("username"),
        seller_type=seller.get("sellerType")
        or ("business" if seller.get("topRatedSeller") else None),
        seller_feedback_score=_to_int(seller.get("feedbackScore")),
        seller_feedback_percentage=_to_float(seller.get("feedbackPercentage")),
        seller_country=seller.get("sellerCountry"),
        item_country=(payload.get("itemLocation") or {}).get("country"),
        condition=payload.get("condition"),
        buying_options=list(payload.get("buyingOptions") or []),
        currency=(payload.get("price") or {}).get("currency"),
        price_amount=to_decimal((payload.get("price") or {}).get("value")),
        shipping_amount=to_decimal(shipping_cost),
        has_returns=payload.get("returnsAccepted"),
        has_warranty=payload.get("warrantyAvailable"),
        listing_status=payload.get("condition"),
        raw_payload=payload,
    )
    candidate = enrich_candidate(candidate, marketplace, scoring)
    return apply_cost_estimate(candidate, marketplace)


def _to_int(value: object) -> int | None:
    try:
        return int(str(value)) if value is not None else None
    except ValueError:
        return None


def _to_float(value: object) -> float | None:
    try:
        return float(str(value)) if value is not None else None
    except ValueError:
        return None
