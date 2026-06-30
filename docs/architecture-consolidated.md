# Architecture Consolidated

## Purpose

Hardware Deal Radar v1 is a VPS-first Python CLI that detects high-signal ThinkPad deals on eBay Europe. It reads YAML config, queries the official eBay Browse API, normalizes listings, estimates total cost, scores opportunities, persists history in SQLite, and sends actionable Telegram/email alerts.

## Non-Negotiable Shape

- Runtime: Python 3.12+.
- Package/dependency workflow: `uv` with a standard `.venv`.
- CLI framework: Typer.
- Settings and schemas: Pydantic.
- HTTP client: httpx.
- YAML parser: PyYAML.
- Persistence: SQLite via SQLModel.
- Terminal output: Rich.
- Tests/lint: pytest and ruff.
- Scheduler: systemd timer every 6 hours.
- Deployment: VPS with venv.
- Docker: optional documentation only.

## Runtime Modes

- `real`: live eBay, Telegram, SMTP, and SQLite.
- `mock`: local fixtures instead of live source APIs.
- `dry-run`: run pipeline and persist as configured, but do not send real alerts.
- `noop`: replace outbound alert adapters with console/file outputs.

Modes must be composable where useful. The minimum implementation checks are:

- `radar run-once --mock --dry-run`
- `radar test-alert --dry-run`
- `radar digest --dry-run`
- `radar doctor`

## Data Flow

```txt
CLI/systemd
  -> settings and config loader
  -> search orchestration
  -> source client
  -> source normalizer
  -> enrichment and extraction
  -> cost estimation
  -> scoring
  -> SQLite persistence and deduplication
  -> alert decision
  -> Telegram and email/noop adapters
  -> run summary and logs
```

## Component Boundaries

- CLI owns command parsing, user-facing output, and exit codes.
- Config owns YAML loading, schema validation, defaults, and config display.
- Settings owns environment variables and safe secret handling.
- Sources own remote API auth, request building, pagination, rate/error handling, and raw payload capture.
- Pipeline owns normalization, extraction, cost estimation, scoring orchestration, and alert decisions.
- Storage owns schema creation, repositories, deduplication queries, alert history, and run records.
- Alerts own message formatting and channel adapters.
- Reports own digest generation and recent-listing views.
- Utils own money, text parsing, time, logging, and serialization helpers.

## Error Policy

- Critical config errors fail fast with clear CLI output.
- One failed marketplace does not stop other marketplaces.
- One failed search does not stop other searches.
- Telegram/email failures are recorded and do not roll back listing persistence.
- Real-mode external failures must appear in run summary and logs.
- Secrets must never be printed, logged, serialized into DB payload previews, or included in docs.

## Scheduling

The implementation must provide systemd unit and timer templates plus a setup script or runbook. The timer runs every 6 hours and invokes the installed CLI in real mode unless the operator overrides it.

## Public Interfaces

Required CLI commands:

- `radar run-once`
- `radar run-once --mock --dry-run`
- `radar digest`
- `radar digest --dry-run`
- `radar test-alert`
- `radar test-alert --dry-run`
- `radar list-recent`
- `radar explain-score <listing_id>`
- `radar validate-config`
- `radar show-config`
- `radar doctor`

Required config files:

- `config/searches.yaml`
- `config/scoring.yaml`
- `config/marketplaces.yaml`

Required environment contract:

- Root `.env` exists locally or on the VPS.
- `.env` is ignored by git.
- `.env.example` documents names only, with no real credentials.
