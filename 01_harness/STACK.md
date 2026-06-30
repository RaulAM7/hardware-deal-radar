# STACK

Default: docs-first workspace.

Current product target:
- Runtime/framework: Python 3.12+ CLI package
- Persistence: SQLite
- Configuration: YAML files under `config/`
- Source integration: official eBay Browse API
- Alerts: Telegram Bot API and SMTP email digest
- Scheduling/deployment: VPS with venv plus systemd timer every 6 hours
- Test/lint candidates: pytest and ruff

Candidate implementation libraries:
- Typer for CLI
- Pydantic for settings/config schemas
- httpx for HTTP APIs
- PyYAML for YAML parsing
- SQLModel or lightweight SQLAlchemy for SQLite
- Rich for terminal output

Current repo state:
- Context and planning workspace only.
- No functional Python implementation yet.
- Previous scaffold/npm direction is superseded by the Hardware Deal Radar context pack.

Expected future commands:
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
