# SPEC-006 - Scoring Engine

## Objective

Implement deterministic, explainable scoring for normalized listing candidates using YAML-configured thresholds, weights, reasons, risks, and recommendations.

## Scope

- Calculate score from hardware, seller, price, marketplace, confidence, and risk components.
- Clamp score to 0-100.
- Produce positive reasons, negative reasons, risk flags, unknown fields, and recommendation.
- Support reject behavior for hard-negative keywords or minimum failures.
- Version the scoring logic.

## Out of Scope

- Generative AI or LLM scoring.
- Perfect market-price comparison.
- External price-history services.
- Automatic purchasing recommendations beyond simple text categories.

## Expected Files and Modules

- `src/hardware_deal_radar/pipeline/score.py`
- `src/hardware_deal_radar/config/schemas.py`
- `tests/test_scoring.py`

## Tasks

- Define `ScoreResult` model.
- Implement hardware scoring for RAM, SSD, CPU text, ThinkPad target family, and model generation if known.
- Implement seller scoring for business seller, feedback percentage, feedback count, returns, warranty, and seller risk.
- Implement price scoring against search `max_estimated_total_eur`.
- Implement marketplace/keyboard/import penalties from config.
- Penalize unknown core fields without inventing values.
- Reject or heavily penalize configured reject keywords.
- Produce recommendation:
  - `strong_candidate` for score >= strong threshold.
  - `watch` for score >= digest threshold.
  - `ignore` for score >= ignore-below but below digest.
  - `reject` for hard failures or below ignore threshold.
- Add `score_version`.

## Acceptance Criteria

- [ ] Score is deterministic for identical input/config.
- [ ] Score is clamped to 0-100.
- [ ] 64 GB RAM and target ThinkPad family increase score.
- [ ] RAM below 32 GB rejects or heavily penalizes.
- [ ] UK/import and foreign keyboard risks reduce score and produce risk flags.
- [ ] Reject keywords produce `reject`.
- [ ] Score result explains positives, negatives, risks, unknowns, and recommendation.

## Tests and Checks

- Test strong P14s 64 GB candidate.
- Test 32 GB medium candidate.
- Test RAM below minimum.
- Test UK penalty.
- Test keyboard unknown penalty.
- Test reject keyword.
- Test deterministic output.

## Risks

- Initial weights are approximate; keep all weights configurable.
- Scores can look authoritative despite incomplete data; include unknown fields and confidence penalties.

## Assumptions

- Initial thresholds are strong `80`, digest `60`, ignore-below `50`.
- Exact CPU/model generation quality can be improved later without changing the public score contract.
