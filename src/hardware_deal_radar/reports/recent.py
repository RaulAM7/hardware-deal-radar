from __future__ import annotations

import json

from hardware_deal_radar.storage.models import ListingRecord


def listing_summary(record: ListingRecord) -> str:
    return (
        f"[{record.id}] {record.title} | {record.marketplace} | "
        f"score={record.score_total or 'n/a'} | total={record.estimated_total_eur or 'n/a'}"
    )


def explain_listing(record: ListingRecord) -> str:
    positives = json.loads(record.positive_reasons_json or "[]")
    negatives = json.loads(record.negative_reasons_json or "[]")
    risks = json.loads(record.risk_flags_json or "[]")
    unknowns = json.loads(record.unknown_fields_json or "[]")
    lines = [
        f"Listing {record.id}: {record.title}",
        f"Marketplace: {record.marketplace}",
        f"Score: {record.score_total or 'n/a'}",
        f"Recommendation: {record.recommendation or 'n/a'}",
        "Positive reasons:",
    ]
    lines.extend(f"+ {item}" for item in positives or ["none"])
    lines.append("Negative reasons:")
    lines.extend(f"- {item}" for item in negatives or ["none"])
    lines.append("Risk flags:")
    lines.extend(f"- {item}" for item in risks or ["none"])
    lines.append("Unknown fields:")
    lines.extend(f"- {item}" for item in unknowns or ["none"])
    return "\n".join(lines)
