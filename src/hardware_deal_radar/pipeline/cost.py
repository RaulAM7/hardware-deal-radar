from __future__ import annotations

from decimal import Decimal

from hardware_deal_radar.config.schemas import MarketplaceConfig
from hardware_deal_radar.models import ListingCandidate
from hardware_deal_radar.utils.money import convert_to_eur, quantize_money


def apply_cost_estimate(
    candidate: ListingCandidate, marketplace: MarketplaceConfig
) -> ListingCandidate:
    price_eur = convert_to_eur(
        candidate.price_amount, candidate.currency, marketplace.eur_exchange_rate
    )
    shipping_eur = convert_to_eur(
        candidate.shipping_amount,
        candidate.currency or marketplace.currency,
        marketplace.eur_exchange_rate,
    )
    estimated_import = Decimal(str(marketplace.import_risk_penalty))
    risk_adjustment = Decimal(str(marketplace.base_risk_penalty))
    candidate.estimated_import_cost_eur = quantize_money(estimated_import)
    candidate.risk_adjustment_eur = quantize_money(risk_adjustment)
    total = (
        (price_eur or Decimal("0"))
        + (shipping_eur or Decimal("0"))
        + estimated_import
        + risk_adjustment
    )
    candidate.estimated_total_eur = quantize_money(total)
    candidate.price_amount = (
        price_eur if candidate.currency and candidate.currency != "EUR" else candidate.price_amount
    )
    candidate.shipping_amount = (
        shipping_eur
        if candidate.currency and candidate.currency != "EUR"
        else candidate.shipping_amount
    )
    return candidate
