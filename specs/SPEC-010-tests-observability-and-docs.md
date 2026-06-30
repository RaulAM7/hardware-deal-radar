# SPEC-010 - Tests, Observability, and Docs

## Objective

Complete quality gates, logging, documentation, runbook, and implementation readiness checks for v1 operation.

## Scope

- Add structured logging.
- Add run summaries and error visibility.
- Ensure tests cover core v1 behavior.
- Update README and docs for install, config, operation, troubleshooting, and safety.
- Produce final implementation QA checklist.

## Out of Scope

- Centralized logging service.
- Metrics dashboards.
- SaaS-grade observability.
- Exhaustive API contract test suite against live eBay.

## Expected Files and Modules

- `src/hardware_deal_radar/utils/logging.py`
- `docs/runbook.md`
- `docs/troubleshooting.md`
- `docs/security.md`
- `README.md`
- `04_outputs/YYYY-MM-DD_implementation_v1.md`
- test files across `tests/`

## Tasks

- Add logging setup controlled by `RADAR_LOG_LEVEL`.
- Log run start/end, mode, searches, marketplaces, result counts, new/updated listings, alert counts, digest counts, errors, and duration.
- Ensure errors are sanitized and actionable.
- Add tests for core modules and mock end-to-end flow.
- Ensure no tests require real `.env` secrets.
- Update README with quickstart, commands, config files, runtime modes, and next steps.
- Add runbook for VPS operation and troubleshooting.
- Add security doc covering `.env`, GitHub push protection, secret masking, and safe logs.
- Add final QA output under `04_outputs/` during implementation completion.

## Acceptance Criteria

- [ ] `uv run pytest` passes.
- [ ] `uv run ruff check .` passes.
- [ ] Mock dry-run command is covered by automated test.
- [ ] Logs include operational summary and sanitized errors.
- [ ] README explains local and VPS usage.
- [ ] Runbook explains doctor, dry-run, real run, alerts, digest, timer, and logs.
- [ ] Security docs explain secret handling.
- [ ] Final implementation output explicitly verifies all project DoD items.

## Tests and Checks

- Full pytest suite.
- Ruff check.
- Mock end-to-end CLI test.
- Secret leak search over tracked docs/tests/config for known env key patterns with values.
- Manual command smoke checks as documented in the final output.

## Risks

- Documentation can drift from commands; implementation must update docs in the same spec where behavior changes.
- Logs can expose payload details; keep logging sanitized and concise.

## Assumptions

- Minimal file/stdout plus journald logs are enough for v1.
- No external observability stack is required.
