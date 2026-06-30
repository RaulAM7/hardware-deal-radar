# Hardware Deal Radar

CLI radar for finding real ThinkPad buying opportunities on eBay Europe.

It loads YAML searches, queries the official eBay Browse API or local mock fixtures, normalizes listings, estimates total cost in EUR, scores candidates deterministically, stores history in SQLite, and sends strong alerts by Telegram plus digest alerts by email.

## Scope

- Python 3.12+
- `uv` dependency workflow with local `.venv`
- YAML config under `config/`
- SQLite persistence
- eBay Browse API as the only v1 source
- Telegram strong alerts
- SMTP email digest
- systemd timer every 6 hours on a VPS

Out of scope in v1:

- frontend or SaaS UI
- HTML scraping
- generative-AI scoring
- external database
- automatic purchasing

## Quickstart

1. Sync the environment:

```bash
~/.local/bin/uv sync --extra dev
```

2. Create the local environment file:

```bash
cp .env.example .env
chmod 600 .env
```

3. Review runtime config:

- `config/searches.yaml`
- `config/scoring.yaml`
- `config/marketplaces.yaml`

4. Run the non-blocking preflight:

```bash
~/.local/bin/uv run radar validate-config
~/.local/bin/uv run radar show-config
~/.local/bin/uv run radar run-once --mock --dry-run
~/.local/bin/uv run radar test-alert --dry-run
~/.local/bin/uv run radar digest --dry-run
~/.local/bin/uv run radar doctor
```

## Commands

```bash
~/.local/bin/uv run radar --help
~/.local/bin/uv run radar run-once
~/.local/bin/uv run radar run-once --mock --dry-run
~/.local/bin/uv run radar digest
~/.local/bin/uv run radar digest --dry-run
~/.local/bin/uv run radar test-alert
~/.local/bin/uv run radar test-alert --dry-run
~/.local/bin/uv run radar list-recent
~/.local/bin/uv run radar explain-score 1
~/.local/bin/uv run radar validate-config
~/.local/bin/uv run radar show-config
~/.local/bin/uv run radar doctor
```

## Runtime Modes

- `real`: live eBay, Telegram, SMTP, and SQLite.
- `mock`: fixture-backed source, no eBay credentials required.
- `dry-run`: pipeline runs and persists, but sends no real outbound alerts.
- `noop`: outbound adapters simulate delivery instead of hitting Telegram/SMTP.

These modes are designed so missing credentials never block implementation or local validation.

## Environment Contract

The public environment contract lives in [`.env.example`](/home/skilland/workspaces/hardware-deal-radar/.env.example:1).

Rules:

- keep real `.env` local or on the VPS only
- do not commit `.env`
- do not print secrets in logs or docs
- use `chmod 600 .env` on the VPS

## Project Layout

- `src/hardware_deal_radar/`: package code
- `tests/`: pytest suite
- `config/`: example and runtime YAML files
- `scripts/`: VPS and systemd helpers
- `docs/`: architecture, security, runbook, troubleshooting
- `specs/`: implementation specs used for this build
- `04_outputs/`: implementation deliverables

## Development

Run the full local gate:

```bash
~/.local/bin/uv run pytest
~/.local/bin/uv run ruff check .
```

The Ruff configuration is scoped to the product code and tests in this repo, not the planning/context workspace that surrounds it.

## VPS Operation

Start with [docs/runbook.md](/home/skilland/workspaces/hardware-deal-radar/docs/runbook.md:1).

Related docs:

- [docs/security.md](/home/skilland/workspaces/hardware-deal-radar/docs/security.md:1)
- [docs/troubleshooting.md](/home/skilland/workspaces/hardware-deal-radar/docs/troubleshooting.md:1)

