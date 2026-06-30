# 001_planning-and-specs

## Outcome

- What must exist at the end:
  - The repo has implementation-ready specs and an ordered implementation plan for Hardware Deal Radar v1.

## Scope

- In scope:
  - Read `02_context/`, `docs/`, `codex/`, `config/`, `01_harness/`, and root project instructions.
  - Produce numbered implementation specs for the full v1 system.
  - Produce an ordered implementation plan.
  - Capture assumptions, closed decisions, risks, and acceptance criteria.
  - Keep v1 aligned with Python CLI, SQLite, YAML, eBay Browse API, Telegram/email, and VPS/systemd.
- Out of scope:
  - Functional implementation.
  - Frontend, SaaS, scraping, Postgres/Supabase, Kubernetes, multi-user support, automatic purchasing, or generative-AI scoring.
  - Real credential setup.

## Inputs

- Files:
  - `02_context/*`
  - `docs/*`
  - `codex/agent-rules.md`
  - `codex/definition-of-done.md`
  - `codex/goal-01-planning.md`
  - `config/*.example.yaml`
  - `.env.example`
  - `01_harness/RULES.md`
  - `01_harness/STACK.md`
  - `01_harness/TASKFLOW.md`
- Links:
  - `https://api.ebay.com/oauth/api_scope`
- Data:
  - Context pack migrated from `CONTENEDOR CONTEXT PACK/`
  - Original raw project context in `00_inbox/`

## Deliverable

- Path: `04_outputs/2026-06-30_planning-specs_v1.md`
- Format: planning summary and QA note.

## Required Planning Outputs

- `specs/SPEC-001-project-foundation.md`
- `specs/SPEC-002-config-system.md`
- `specs/SPEC-003-ebay-api-integration.md`
- `specs/SPEC-004-normalization-pipeline.md`
- `specs/SPEC-005-storage-and-deduplication.md`
- `specs/SPEC-006-scoring-engine.md`
- `specs/SPEC-007-alerting-system.md`
- `specs/SPEC-008-cli-interface.md`
- `specs/SPEC-009-scheduling-and-vps-deployment.md`
- `specs/SPEC-010-tests-observability-and-docs.md`
- `codex/implementation-plan.md`

## Acceptance Criteria

- [ ] There is a numbered spec set covering project foundation, config, eBay API, normalization, storage/deduplication, scoring, alerts, CLI, deployment, tests, observability, and docs.
- [ ] Each spec includes objective, scope, out-of-scope, expected files/modules, tasks, acceptance criteria, tests/checks, risks, and assumptions.
- [ ] `codex/implementation-plan.md` defines the implementation order and dependencies between specs.
- [ ] Closed decisions remain aligned with `docs/technical-decisions.md`.
- [ ] Assumptions remain aligned with `docs/assumptions.md`.
- [ ] The plan explicitly preserves mock, dry-run, and noop behavior so credentials do not block implementation.
- [ ] The plan keeps the previous npm scaffold direction out of active implementation.
- [ ] A deliverable note is written under `04_outputs/`.

## Risks and Edge Cases

- Risk: specs become too broad and re-open closed product decisions.
- Risk: implementation plan overfits to unavailable real credentials.
- Risk: old scaffold references re-enter active scope.
- Edge case: eBay Browse API details may require official documentation verification during the API integration spec.

## Open Questions

- Q1: Exact purchase budget thresholds by model/generation are still unknown.
- Q2: Exact scoring weights need to be finalized in the scoring spec.
- Q3: Final SMTP provider and VPS host details are still unknown.
