# Planning Specs v1 - 2026-06-30

## What was produced

- Numbered implementation specs in `specs/SPEC-001-project-foundation.md` through `specs/SPEC-010-tests-observability-and-docs.md`.
- Sequential implementation handoff in `codex/implementation-plan.md`.
- Consolidated architecture in `docs/architecture-consolidated.md`.
- Data model contract in `docs/data-model-v1.md`.
- Module design in `docs/module-design-v1.md`.
- Credential strategy in `docs/credential-strategy.md`.
- Anti-blocking protocol in `docs/anti-blocking-protocol.md`.
- Implementation readiness checklist in `docs/implementation-readiness-checklist.md`.
- Updated assumptions and technical decisions.

## Scope confirmation

- No functional implementation was added.
- No `.env` secrets were read or documented.
- V1 scope remains Python, SQLite, YAML, CLI, eBay Browse API, Telegram, email digest, and systemd timer.
- Frontend, SaaS, scraping, Postgres/Supabase, Kubernetes, multi-user support, automatic purchase, and generative-AI scoring remain out of scope.

## QA against active spec

- [x] Numbered spec set covers project foundation, config, eBay API, normalization, storage/deduplication, scoring, alerts, CLI, deployment, tests, observability, and docs.
- [x] Each spec includes objective, scope, out-of-scope, expected files/modules, tasks, acceptance criteria, tests/checks, risks, and assumptions.
- [x] `codex/implementation-plan.md` defines implementation order and dependencies.
- [x] Closed decisions remain aligned with `docs/technical-decisions.md`.
- [x] Assumptions remain aligned with `docs/assumptions.md`.
- [x] Plan preserves mock, dry-run, and noop behavior so credentials do not block implementation.
- [x] Plan keeps the previous npm scaffold direction out of active implementation.
- [x] Deliverable note is written under `04_outputs/`.

## Unknowns left for implementation

- Exact purchase budget by model/generation.
- Final SMTP provider and production VPS path/user.
- Exact official eBay Browse API request details must be verified during `SPEC-003`.

## Suggested next action

Start the implementation goal and follow `codex/implementation-plan.md` in numeric spec order.
