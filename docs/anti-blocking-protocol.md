# Anti-Blocking Protocol

## Principle

No human credential, external API, network condition, or systemd availability may block implementation progress. Real adapters must exist, but every external dependency must have a mock, dry-run, or noop path.

## Required Fallbacks

- eBay unavailable: use `--mock` fixture source.
- eBay credentials missing: `radar doctor` reports missing variables; `radar run-once --mock --dry-run` still works.
- Telegram missing/failing: use noop adapter and record simulated/failed alert status.
- SMTP missing/failing: skip or simulate digest and record reason.
- SQLite path missing: create parent directory when safe, otherwise fail clearly.
- systemd unavailable locally: provide unit/timer templates and document manual validation.
- Network unavailable: mock tests and local CLI commands still run.

## Implementation Rules

- Implement the real adapter and the fallback adapter in the same spec where that integration appears.
- Add a `doctor` check for every external dependency introduced.
- Add at least one test proving the fallback path works without secrets.
- Continue to later specs when a real credential is absent.
- Document any human action needed in README/runbook, not as a blocker in code.

## Minimum Non-Blocking Commands

These commands must work before v1 is considered implementation-ready:

```bash
radar validate-config
radar show-config
radar run-once --mock --dry-run
radar test-alert --dry-run
radar digest --dry-run
radar doctor
```

## Escalation

Stop only for a design contradiction that makes the spec impossible, not for missing secrets, failing external APIs, absent systemd on the dev machine, or incomplete SMTP setup.
