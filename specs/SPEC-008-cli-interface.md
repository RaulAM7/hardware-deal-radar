# SPEC-008 - CLI Interface

## Objective

Implement the operator-facing CLI commands that run the radar, inspect state, validate configuration, explain scores, and test alerts.

## Scope

- Implement all required `radar` commands.
- Add global flags for config dir, DB path override, mock, dry-run, noop, verbosity, and log level where applicable.
- Use Rich for readable output.
- Use meaningful exit codes.
- Keep commands usable on local dev and VPS.

## Out of Scope

- TUI or web UI.
- Interactive credential prompts.
- Automatic purchase flows.

## Expected Files and Modules

- `src/hardware_deal_radar/cli.py`
- `src/hardware_deal_radar/main.py`
- `src/hardware_deal_radar/reports/recent.py`
- `tests/test_cli_commands.py`

## Tasks

- Implement `radar run-once`.
- Implement `radar run-once --mock --dry-run`.
- Implement `radar digest`.
- Implement `radar digest --dry-run`.
- Implement `radar test-alert`.
- Implement `radar test-alert --dry-run`.
- Implement `radar list-recent`.
- Implement `radar explain-score <listing_id>`.
- Implement `radar validate-config`.
- Implement `radar show-config`.
- Implement `radar doctor`.
- Ensure commands do not print secrets.
- Make `doctor` usable before real credentials are configured.

## Acceptance Criteria

- [ ] `radar --help` lists all required commands.
- [ ] `radar validate-config` validates YAML files.
- [ ] `radar show-config` prints sanitized config.
- [ ] `radar run-once --mock --dry-run` completes with fixture data.
- [ ] `radar test-alert --dry-run` completes without Telegram/SMTP credentials.
- [ ] `radar digest --dry-run` completes with no real email.
- [ ] `radar list-recent` reads from SQLite and handles empty DB.
- [ ] `radar explain-score <listing_id>` explains known listing scores and handles missing IDs.
- [ ] `radar doctor` reports readiness without secret values.

## Tests and Checks

- CLI help snapshot or content assertions.
- Command tests with Typer test runner.
- Mock dry-run e2e command test.
- Empty DB command tests.
- Secret masking tests for `show-config` and `doctor`.

## Risks

- CLI can become a thin wrapper over untested orchestration; add command-level tests for key flows.
- Exit codes must distinguish validation failure from runtime partial failure.

## Assumptions

- The CLI is the only user interface in v1.
- Rich table/text output is sufficient for operator UX.
