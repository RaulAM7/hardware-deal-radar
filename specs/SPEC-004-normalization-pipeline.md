# SPEC-004 - Normalization Pipeline

## Objective

Convert raw source payloads into normalized listing candidates enriched with ThinkPad-relevant hardware, seller, cost, and risk fields.

## Scope

- Normalize raw eBay listing payloads.
- Extract RAM, SSD, CPU text, model family, model generation, keyboard layout, condition, seller, and buying data.
- Estimate EUR total cost from price, shipping, currency, and marketplace risk config.
- Flag reject/penalty keywords.
- Produce structured candidates for scoring and persistence.

## Out of Scope

- Perfect natural-language parsing.
- Exact customs/tax calculation.
- Live currency exchange APIs.
- Scoring formula implementation beyond fields required by scorer.

## Expected Files and Modules

- `src/hardware_deal_radar/sources/ebay_normalizer.py`
- `src/hardware_deal_radar/pipeline/normalize.py`
- `src/hardware_deal_radar/pipeline/enrich.py`
- `src/hardware_deal_radar/pipeline/cost.py`
- `src/hardware_deal_radar/utils/text.py`
- `src/hardware_deal_radar/utils/money.py`
- `tests/test_normalization.py`
- `tests/test_enrichment.py`
- `tests/test_cost_estimation.py`

## Tasks

- Define normalized `ListingCandidate` model.
- Map eBay item fields into candidate fields.
- Canonicalize listing URLs.
- Extract model families: P14s, T14, T16, P1, X1 Extreme.
- Extract RAM patterns including `32GB`, `32 GB`, `64GB`, `64 GB`.
- Extract SSD patterns including `512GB`, `1TB`, `2TB`.
- Extract CPU text with simple patterns for Ryzen PRO and Intel i7/i9 strings.
- Detect keyboard layout from title/description hints when available; otherwise mark unknown.
- Apply negative keyword flags from config.
- Estimate `estimated_total_eur`; for GBP in v1 use a configurable static conversion or mark conversion assumption clearly.
- Add risk fields for UK import, keyboard uncertainty, low information, parts-only, and suspicious condition terms.

## Acceptance Criteria

- [ ] Fixture eBay payloads normalize into stable candidate objects.
- [ ] RAM, SSD, model family, and negative keywords are extracted from common title patterns.
- [ ] Unknown extracted fields are represented explicitly, not invented.
- [ ] UK listings get import risk fields.
- [ ] Total cost distinguishes visible price, shipping, estimated import cost, risk adjustment, and total EUR.
- [ ] Normalization works without network and without real credentials.

## Tests and Checks

- Test representative ThinkPad P14s/T14/T16/P1/X1 titles.
- Test reject keywords such as `for parts`, `broken`, `BIOS locked`, and `not working`.
- Test unknown RAM/SSD/CPU handling.
- Test UK risk adjustment.
- Test canonical URL fallback.

## Risks

- Source payloads may omit important fields; keep unknowns explicit.
- Text extraction can be brittle; keep patterns simple and well tested.

## Assumptions

- v1 can rely primarily on title and available eBay structured fields.
- Exact tax/customs math is out of scope; risk-adjusted estimates are acceptable.
