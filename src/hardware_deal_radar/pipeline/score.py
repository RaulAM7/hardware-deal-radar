from __future__ import annotations

from decimal import Decimal

from hardware_deal_radar.config.schemas import MarketplaceConfig, ScoringConfig, SearchConfig
from hardware_deal_radar.models import ListingCandidate, ScoreResult


def score_candidate(
    candidate: ListingCandidate,
    search: SearchConfig,
    scoring: ScoringConfig,
    marketplace: MarketplaceConfig,
) -> ScoreResult:
    positive: list[str] = []
    negative: list[str] = []
    risk_flags = list(dict.fromkeys(candidate.risk_flags))
    unknown_fields = list(dict.fromkeys(candidate.unknown_fields))
    score = 0

    if candidate.matched_reject_keywords:
        return ScoreResult(
            score_total=0,
            negative_reasons=[
                f"reject keyword: {keyword}" for keyword in candidate.matched_reject_keywords
            ],
            risk_flags=risk_flags,
            unknown_fields=unknown_fields,
            recommendation="reject",
        )

    if candidate.ram_gb is None:
        score -= 4
        negative.append("RAM unknown")
    elif candidate.ram_gb < scoring.ram.minimum_gb:
        score += scoring.ram.points.below_minimum
        negative.append(f"RAM below minimum ({candidate.ram_gb} GB)")
    elif candidate.ram_gb >= scoring.ram.preferred_gb:
        score += scoring.ram.points.preferred
        positive.append(f"{candidate.ram_gb}GB RAM")
    else:
        score += scoring.ram.points.minimum
        positive.append(f"{candidate.ram_gb}GB RAM")

    if candidate.ssd_gb is None:
        score -= 2
        negative.append("SSD unknown")
    elif candidate.ssd_gb >= 2048:
        score += scoring.storage.points.ssd_2tb
        positive.append("2TB SSD")
    elif candidate.ssd_gb >= 1024:
        score += scoring.storage.points.ssd_1tb
        positive.append("1TB SSD")
    elif candidate.ssd_gb >= 512:
        score += scoring.storage.points.ssd_512gb
        positive.append("512GB SSD")
    else:
        score -= 3
        negative.append("small SSD")

    if candidate.cpu_text:
        lowered_cpu = candidate.cpu_text.lower()
        if "ryzen 7 pro" in lowered_cpu or "7840" in lowered_cpu or "8840" in lowered_cpu:
            score += 12
            positive.append("modern CPU")
        elif "i7" in lowered_cpu or "i9" in lowered_cpu:
            score += 8
            positive.append("strong CPU")
        else:
            score += 3
    else:
        score -= 3
        negative.append("CPU unknown")

    if candidate.is_target_family:
        score += 10
        positive.append(f"target family {candidate.model_family}")
    elif candidate.is_thinkpad:
        score += 4
        positive.append("ThinkPad family")
    else:
        score -= 8
        negative.append("not a target ThinkPad")

    if candidate.model_generation and candidate.model_generation.isdigit():
        if int(candidate.model_generation) >= 4:
            score += 6
            positive.append(f"Gen {candidate.model_generation}")

    if candidate.is_business_seller:
        score += scoring.seller.business_seller
        positive.append("business seller")
    if candidate.seller_feedback_percentage is not None:
        if candidate.seller_feedback_percentage >= 99:
            score += scoring.seller.feedback_percentage_99_plus
            positive.append("seller feedback 99+")
        elif candidate.seller_feedback_percentage >= 97:
            score += scoring.seller.feedback_percentage_97_plus
            positive.append("seller feedback 97+")
        else:
            score += scoring.seller.feedback_low_penalty
            negative.append("seller feedback low")
            risk_flags.append("seller_risk")
    else:
        score -= 3
        negative.append("seller feedback unknown")

    if candidate.has_returns:
        score += scoring.seller.returns_accepted
        positive.append("returns accepted")
    if candidate.has_warranty:
        score += scoring.seller.warranty_available
        positive.append("warranty available")

    if candidate.estimated_total_eur is not None and search.max_estimated_total_eur is not None:
        max_total = Decimal(str(search.max_estimated_total_eur))
        if candidate.estimated_total_eur <= max_total * Decimal("0.75"):
            score += 20
            positive.append("price very competitive")
        elif candidate.estimated_total_eur <= max_total * Decimal("0.90"):
            score += 12
            positive.append("price competitive")
        elif candidate.estimated_total_eur <= max_total:
            score += 6
        else:
            score -= 10
            negative.append("price above target")

    score += scoring.marketplace.get(candidate.marketplace, 0)
    if candidate.marketplace == "EBAY_GB":
        negative.append("UK import risk")
        risk_flags.append("import_risk")

    keyboard_key = candidate.keyboard_layout or "unknown"
    score += scoring.keyboard.get(keyboard_key, scoring.keyboard.get("other", -8))
    if keyboard_key not in {"ES", None}:
        negative.append(f"keyboard {keyboard_key.lower()}")

    score -= 2 * len(candidate.matched_penalty_keywords)
    for keyword in candidate.matched_penalty_keywords:
        negative.append(keyword)

    score -= 2 * len(unknown_fields)
    score = max(0, min(100, score))

    strong_threshold = search.strong_alert_threshold or scoring.thresholds.strong_alert
    digest_threshold = search.digest_threshold or scoring.thresholds.digest
    if score >= strong_threshold:
        recommendation = "strong_candidate"
    elif score >= digest_threshold:
        recommendation = "watch"
    elif score >= scoring.thresholds.ignore_below:
        recommendation = "ignore"
    else:
        recommendation = "reject"

    return ScoreResult(
        score_total=score,
        positive_reasons=list(dict.fromkeys(positive)),
        negative_reasons=list(dict.fromkeys(negative)),
        risk_flags=list(dict.fromkeys(risk_flags)),
        unknown_fields=list(dict.fromkeys(unknown_fields)),
        recommendation=recommendation,
    )
