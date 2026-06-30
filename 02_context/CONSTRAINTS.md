# CONSTRAINTS

## Budget

- Exact purchase budget: Unknown.
- The buying decision must be based on estimated total cost, not visible listing price alone.
- Used/refurbished purchase is only justified when the total cost is clearly attractive versus credible alternatives.

## Time

- Run cadence: every 6 hours.
- v1 delivery deadline: Unknown.

## Tooling

- Use Python 3.12+.
- Use SQLite for v1 persistence.
- Use YAML for searches, scoring, and marketplace config.
- Use CLI as the primary interface.
- Use official eBay Browse API.
- Use Telegram Bot API for strong alerts.
- Use SMTP for email digest.
- Deploy VPS-first with venv plus systemd timer.
- Docker may be documented but is not required.

## Non-negotiables

- ThinkPad only in v1.
- No frontend web app.
- No SaaS.
- No multi-user system.
- No automatic purchase.
- No HTML scraping in v1.
- No generative AI in scoring v1.
- No Postgres/Supabase in v1.
- No Kubernetes, microservices, queues, or distributed architecture unless a later spec explicitly changes scope.
- Do not commit `.env`.
- Do not print, log, test with, or document real secrets.

## Operational Constraints

- The system must run in real, mock, dry-run, and noop modes.
- `radar doctor` must validate config, environment, DB access, and real-service readiness when applicable.
- External failures should be visible in logs and should not break unrelated searches, marketplaces, persistence, or digest generation.
- Implementation must continue even when credentials are missing by using mock/noop/dry-run paths.

## Product Constraints

- Alert little, but alert well.
- Alerts must explain score, positives, risks, inferred fields, unknowns, total cost, and link.
- UK is allowed but penalized.
- Foreign keyboard layouts are penalized, not automatically rejected.
- Listings with "for parts", "spares", "defective", "broken", "no boot", "BIOS locked", or equivalent risk terms should be rejected or heavily penalized.

## Repo Constraints

- Keep one active spec in `03_specs/now/`.
- Heavy context belongs in `docs/` and `codex/`; `02_context/` must stay skimmable.
- The previous scaffold/npm spec is superseded and must not drive implementation.
