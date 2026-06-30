# Data Model v1

## Goals

The database must support deduplication, score explanation, alert history, digest generation, CLI inspection, and resilient run diagnostics. Use SQLite via SQLModel. Automatic table creation at startup is acceptable for v1.

## Tables

### runs

Fields:

- `id`: integer primary key.
- `started_at`: UTC datetime.
- `finished_at`: UTC datetime nullable.
- `status`: `running`, `success`, `partial_failure`, `failed`.
- `mode`: `real`, `mock`, `dry_run`, `noop`, or combined mode label.
- `searches_count`: integer.
- `marketplaces_count`: integer.
- `raw_results_count`: integer.
- `new_listings_count`: integer.
- `updated_listings_count`: integer.
- `strong_alerts_count`: integer.
- `digest_candidates_count`: integer.
- `errors_count`: integer.
- `summary_json`: JSON text.

### listings

Fields:

- `id`: integer primary key.
- `source`: string, v1 value `ebay`.
- `marketplace`: string, for example `EBAY_DE`.
- `source_item_id`: string nullable.
- `canonical_url`: string nullable.
- `title`: string.
- `seller_username`: string nullable.
- `seller_type`: string nullable.
- `seller_feedback_score`: integer nullable.
- `seller_feedback_percentage`: float nullable.
- `seller_country`: string nullable.
- `item_country`: string nullable.
- `condition`: string nullable.
- `buying_options`: JSON text.
- `currency`: string nullable.
- `price_amount`: decimal nullable.
- `shipping_amount`: decimal nullable.
- `estimated_total_eur`: decimal nullable.
- `estimated_import_cost_eur`: decimal nullable.
- `risk_adjustment_eur`: decimal nullable.
- `model_family`: string nullable.
- `model_generation`: string nullable.
- `cpu_text`: string nullable.
- `ram_gb`: integer nullable.
- `ssd_gb`: integer nullable.
- `keyboard_layout`: string nullable.
- `is_thinkpad`: boolean.
- `is_target_family`: boolean.
- `is_business_seller`: boolean nullable.
- `has_returns`: boolean nullable.
- `has_warranty`: boolean nullable.
- `listing_status`: string nullable.
- `score_total`: integer nullable.
- `score_version`: string nullable.
- `positive_reasons_json`: JSON text.
- `negative_reasons_json`: JSON text.
- `risk_flags_json`: JSON text.
- `unknown_fields_json`: JSON text.
- `recommendation`: `strong_candidate`, `watch`, `ignore`, or `reject`.
- `first_seen_at`: UTC datetime.
- `last_seen_at`: UTC datetime.
- `last_changed_at`: UTC datetime nullable.
- `raw_payload_json`: JSON text.

### alerts

Fields:

- `id`: integer primary key.
- `listing_id`: foreign key to `listings.id`.
- `run_id`: foreign key to `runs.id`, nullable for manual tests.
- `alert_type`: `strong`, `digest`, `test`, or `price_drop`.
- `channel`: `telegram`, `email`, `noop`, or `console`.
- `threshold`: integer nullable.
- `score_at_send`: integer nullable.
- `price_at_send`: decimal nullable.
- `status`: `sent`, `simulated`, `failed`, or `skipped`.
- `sent_at`: UTC datetime nullable.
- `error_message`: string nullable, sanitized.
- `payload_preview`: text, sanitized and without secrets.

### price_history

Fields:

- `id`: integer primary key.
- `listing_id`: foreign key to `listings.id`.
- `run_id`: foreign key to `runs.id`.
- `price_amount`: decimal nullable.
- `shipping_amount`: decimal nullable.
- `estimated_total_eur`: decimal nullable.
- `observed_at`: UTC datetime.

### error_logs

Fields:

- `id`: integer primary key.
- `run_id`: foreign key to `runs.id`, nullable.
- `source`: string nullable.
- `marketplace`: string nullable.
- `error_type`: string.
- `message`: string, sanitized.
- `created_at`: UTC datetime.

## Deduplication Keys

Preferred stable identity:

- `source + marketplace + source_item_id`

Fallback identity order:

- canonical URL.
- `marketplace + seller_username + normalized_title + price_amount`.

## Relevant Changes

An existing listing becomes updated when any of these change:

- visible price.
- shipping amount.
- estimated total cost.
- score or recommendation.
- condition.
- seller identity or seller risk.
- return/warranty signal.
- availability/status.
- extracted RAM, SSD, CPU, model, or keyboard.

## Indexes

Required indexes:

- unique preferred identity when `source_item_id` exists.
- `canonical_url`.
- `marketplace`.
- `score_total`.
- `recommendation`.
- `first_seen_at`.
- `last_seen_at`.
- `estimated_total_eur`.
- `ram_gb`.
- `model_family`.
- `alerts.listing_id`.
- `alerts.status`.
- `price_history.listing_id`.

## JSON Policy

Use JSON text fields for source payload, score reasons, risk flags, unknown fields, and run summaries. Do not store secrets. Raw eBay payloads are acceptable if sanitized for credentials and tokens.
