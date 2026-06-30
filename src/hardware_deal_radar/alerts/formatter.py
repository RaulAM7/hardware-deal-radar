from __future__ import annotations

from collections.abc import Sequence

from hardware_deal_radar.models import DigestEntry, ListingCandidate, ScoreResult


def format_telegram_alert(candidate: ListingCandidate, score: ScoreResult) -> str:
    lines = [
        "Possible ThinkPad deal",
        candidate.title,
        f"RAM: {candidate.ram_gb or 'unknown'} GB",
        f"SSD: {candidate.ssd_gb or 'unknown'} GB",
        f"CPU: {candidate.cpu_text or 'unknown'}",
        f"Marketplace: {candidate.marketplace}",
        f"Country: {candidate.item_country or 'unknown'}",
        f"Seller: {candidate.seller_username or 'unknown'}",
        f"Price: {candidate.price_amount or 'unknown'}",
        f"Shipping: {candidate.shipping_amount or 'unknown'}",
        f"Estimated total: {candidate.estimated_total_eur or 'unknown'} EUR",
        f"Score: {score.score_total}/100",
        "",
        "Positive reasons:",
    ]
    lines.extend(f"+ {reason}" for reason in score.positive_reasons)
    lines.append("Risks:")
    lines.extend(f"- {risk}" for risk in score.risk_flags or score.negative_reasons)
    lines.extend(["", f"Link: {candidate.canonical_url or 'unavailable'}"])
    return "\n".join(lines)


def format_digest(entries: Sequence[DigestEntry], run_summary: str) -> str:
    lines = ["Hardware Deal Radar digest", "", run_summary, ""]
    if not entries:
        lines.append("No candidates met digest threshold.")
        return "\n".join(lines)
    for entry in entries:
        candidate = entry.candidate
        score = entry.score
        lines.extend(
            [
                candidate.title,
                f"Marketplace: {candidate.marketplace}",
                f"Estimated total: {candidate.estimated_total_eur or 'unknown'} EUR",
                f"Score: {score.score_total}/100",
                f"Risks: {', '.join(score.risk_flags or score.negative_reasons) or 'none'}",
                f"Link: {candidate.canonical_url or 'unavailable'}",
                "",
            ]
        )
    return "\n".join(lines).rstrip()
