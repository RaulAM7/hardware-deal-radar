from __future__ import annotations

from hardware_deal_radar.config.schemas import MarketplaceConfig, ScoringConfig
from hardware_deal_radar.models import ListingCandidate
from hardware_deal_radar.utils.text import (
    detect_keyboard_layout,
    extract_cpu_text,
    extract_model_family,
    extract_model_generation,
    extract_ram_gb,
    extract_ssd_gb,
    find_keywords,
    normalize_whitespace,
)


def enrich_candidate(
    candidate: ListingCandidate,
    marketplace: MarketplaceConfig,
    scoring: ScoringConfig,
) -> ListingCandidate:
    text = normalize_whitespace(" ".join(filter(None, [candidate.title, candidate.description])))
    candidate.model_family = extract_model_family(text)
    candidate.model_generation = extract_model_generation(text)
    candidate.ram_gb = extract_ram_gb(text)
    candidate.ssd_gb = extract_ssd_gb(text)
    candidate.cpu_text = extract_cpu_text(text)
    candidate.keyboard_layout = detect_keyboard_layout(text)
    candidate.is_thinkpad = "thinkpad" in text.lower()
    candidate.is_target_family = candidate.model_family in {
        "P14s",
        "T14",
        "T16",
        "P1",
        "X1 Extreme",
    }
    candidate.is_business_seller = candidate.seller_type in {"business", "Business", "professional"}
    candidate.matched_reject_keywords = find_keywords(text, scoring.negative_keywords.reject)
    candidate.matched_penalty_keywords = find_keywords(text, scoring.negative_keywords.penalize)

    if marketplace.country == "GB":
        candidate.risk_flags.append("import_risk")
    if candidate.keyboard_layout is None:
        candidate.risk_flags.append("keyboard_layout_risk")
    if candidate.matched_reject_keywords:
        candidate.risk_flags.append("possible_parts_only")
    if candidate.matched_penalty_keywords:
        candidate.risk_flags.append("condition_risk")
    if candidate.ram_gb is None:
        candidate.unknown_fields.append("ram_gb")
    if candidate.ssd_gb is None:
        candidate.unknown_fields.append("ssd_gb")
    if candidate.cpu_text is None:
        candidate.unknown_fields.append("cpu_text")
    if candidate.model_family is None:
        candidate.unknown_fields.append("model_family")
    if candidate.keyboard_layout is None:
        candidate.unknown_fields.append("keyboard_layout")
    return candidate
