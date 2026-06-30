# Implementation Plan

## Purpose

This plan is the handoff from planning to implementation. The implementation agent must follow specs in numeric order and must not redesign the product unless a spec is technically impossible.

## Execution Order

1. `SPEC-001-project-foundation`
   - Establish Python package, `uv`, Typer CLI, settings, `.env.example`, secret masking, pytest, and ruff.
   - Gate: `uv run radar --help`, `uv run pytest`, and `uv run ruff check .`.

2. `SPEC-002-config-system`
   - Implement YAML schemas and config commands.
   - Gate: valid config loads; invalid config fails clearly; no secrets in output.

3. `SPEC-003-ebay-api-integration`
   - Implement source abstraction, eBay client, OAuth, and mock source.
   - Gate: mocked HTTP tests pass; mock source works without credentials.

4. `SPEC-004-normalization-pipeline`
   - Normalize eBay payloads, extract ThinkPad specs, estimate cost, and flag risks.
   - Gate: fixtures produce candidates with explicit unknowns and risk flags.

5. `SPEC-005-storage-and-deduplication`
   - Implement SQLite schema, repositories, run records, listing upsert, alert history, and price history.
   - Gate: dedup and price-history tests pass on temporary SQLite DB.

6. `SPEC-006-scoring-engine`
   - Implement deterministic scoring and recommendation output.
   - Gate: scoring tests prove thresholds, penalties, reject paths, and deterministic output.

7. `SPEC-007-alerting-system`
   - Implement Telegram, SMTP digest, noop, dry-run behavior, formatting, and anti-duplicate alerts.
   - Gate: no real credentials needed for tests; dry-run sends nothing real.

8. `SPEC-008-cli-interface`
   - Connect commands to orchestration, storage, reports, config, doctor, and alert tests.
   - Gate: required commands exist and mock/dry-run flow completes.

9. `SPEC-009-scheduling-and-vps-deployment`
   - Add VPS scripts, systemd templates, and runbook deployment flow.
   - Gate: timer is every 6 hours; scripts/templates contain no secrets.

10. `SPEC-010-tests-observability-and-docs`
    - Complete logging, docs, security notes, troubleshooting, and final QA output.
    - Gate: full pytest and ruff pass; docs explain operation and troubleshooting.

## Dependency Rules

- Do not start real pipeline orchestration before config, source, normalization, storage, and scoring contracts exist.
- Every external integration must include fallback behavior in the same implementation phase.
- Every new command must have at least one test or documented smoke check.
- Any spec may update README/runbook when it introduces operator-visible behavior.
- Do not defer secret masking; it is required from `SPEC-001`.

## Runtime Mode Rules

- `real`: require real credentials for the live integrations being used.
- `mock`: source API credentials not required.
- `dry-run`: no real Telegram/SMTP sends.
- `noop`: outbound adapters write to console/file and records are simulated.

Minimum commands that must survive absent real credentials:

```bash
radar validate-config
radar show-config
radar run-once --mock --dry-run
radar test-alert --dry-run
radar digest --dry-run
radar doctor
```

## Data and Config Contracts

- Use `docs/data-model-v1.md` as the database contract.
- Use `docs/module-design-v1.md` as the package/module contract.
- Use `config/searches.yaml`, `config/scoring.yaml`, and `config/marketplaces.yaml` as runtime config names.
- Keep `config/*.example.yaml` as safe examples.
- Use `.env.example` as the public environment contract.
- Never read or document `.env` values in implementation notes.

## Quality Gates

After each spec:

- Run the most focused pytest subset for the changed behavior.
- Run ruff for changed Python once Python code exists.
- Run relevant CLI smoke command if the CLI path exists.
- Update docs when behavior becomes user-visible.

Before final implementation completion:

- `uv run pytest`
- `uv run ruff check .`
- `uv run radar validate-config`
- `uv run radar show-config`
- `uv run radar run-once --mock --dry-run`
- `uv run radar test-alert --dry-run`
- `uv run radar digest --dry-run`
- `uv run radar doctor`

## Human Actions That Must Not Block Implementation

- Providing eBay credentials.
- Providing Telegram token/chat ID.
- Providing SMTP credentials.
- Running on a real VPS.
- Enabling systemd timer.
- Confirming exact purchase budget.

When these are missing, implement real adapter plus mock/noop/dry-run behavior, document pending human action, and continue.

## Completion Definition

The implementation goal is complete only when every spec is implemented or explicitly marked not implemented with a reason, all required checks pass or are explained, and `04_outputs/YYYY-MM-DD_implementation_v1.md` verifies the project Definition of Done.
