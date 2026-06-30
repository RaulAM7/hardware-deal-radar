# SPEC-003 - eBay API Integration

## Objective

Implement the official eBay Browse API source client, OAuth handling, marketplace mapping, and mock source fallback.

## Scope

- Add source abstraction.
- Add eBay Browse API client using httpx.
- Add OAuth client credentials flow.
- Add marketplace-specific request headers/IDs from YAML config.
- Add mock source backed by fixtures.
- Add doctor checks for eBay readiness without exposing credentials.

## Out of Scope

- HTML scraping.
- Sources other than eBay.
- Scoring and alerting decisions.
- Complete normalization beyond raw-to-candidate handoff.

## Expected Files and Modules

- `src/hardware_deal_radar/sources/base.py`
- `src/hardware_deal_radar/sources/ebay_client.py`
- `src/hardware_deal_radar/sources/mock_source.py`
- `tests/fixtures/ebay/search_response.json`
- `tests/test_ebay_client.py`
- `tests/test_mock_source.py`

## Tasks

- Define `SourceClient` protocol with `search(search_config, marketplace_config)`.
- Implement eBay token retrieval from `EBAY_CLIENT_ID`, `EBAY_CLIENT_SECRET`, `EBAY_SCOPE`, and `EBAY_ENV`.
- Implement Browse API search requests for configured marketplace and query.
- Add request parameters for text query, limit, buying options if available, and marketplace ID/header.
- Add timeout and retry policy with bounded retries.
- Map eBay HTTP/auth/rate errors into sanitized domain errors.
- Store raw response payloads for normalization without storing auth headers or tokens.
- Implement mock source returning fixture payloads without credentials.
- Add eBay section to `radar doctor` that reports missing credentials by variable name only.

## Acceptance Criteria

- [ ] Source abstraction supports real and mock implementations.
- [ ] Real eBay client never logs client secret or bearer token.
- [ ] Missing credentials produce a clear doctor warning, not a crash in mock mode.
- [ ] Mock source works with `radar run-once --mock --dry-run`.
- [ ] eBay errors are sanitized and do not stop unrelated searches/marketplaces.
- [ ] Tests cover successful mock search and eBay request construction with mocked HTTP.

## Tests and Checks

- Test mock fixture loading.
- Test eBay token request construction without real network.
- Test search request uses marketplace settings.
- Test sanitized errors do not include secrets.
- Test missing credentials path.

## Risks

- eBay Browse API details may differ from assumptions; verify official docs during implementation.
- API rate limits may require conservative pagination in v1.

## Assumptions

- v1 uses production eBay by default.
- If sandbox support is added, it is controlled by `EBAY_ENV`.
- Exact marketplace IDs are defined in `marketplaces.yaml` during implementation if needed.
