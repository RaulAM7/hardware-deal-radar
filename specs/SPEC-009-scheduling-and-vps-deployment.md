# SPEC-009 - Scheduling and VPS Deployment

## Objective

Prepare Hardware Deal Radar for VPS operation with venv installation, `.env` setup, systemd service/timer, logs, and operator runbook.

## Scope

- Add scripts or documented commands for VPS setup.
- Add systemd service and timer templates.
- Document `.env` placement and permissions.
- Document manual run, dry-run, doctor, logs, and timer operations.
- Keep Docker optional only.

## Out of Scope

- Provisioning a VPS.
- Managing real DNS, reverse proxy, SSL, or web server.
- Kubernetes, Docker Compose as required runtime, or daemon architecture.
- Storing real secrets in repo.

## Expected Files and Modules

- `scripts/install-vps.sh`
- `scripts/run-once.sh`
- `scripts/setup-systemd.sh`
- `scripts/systemd/hardware-deal-radar.service`
- `scripts/systemd/hardware-deal-radar.timer`
- `docs/runbook.md`
- `README.md`
- `tests/test_deployment_templates.py`

## Tasks

- Define install flow: clone repo, install uv, create venv, sync dependencies, copy config examples, create data dir.
- Document `.env` creation from `.env.example` and permissions `600`.
- Add service template invoking the installed `radar run-once`.
- Add timer template for every 6 hours.
- Add commands to enable, start, inspect, and disable timer.
- Add logs instructions using `journalctl`.
- Add preflight sequence:
  - `radar doctor`
  - `radar validate-config`
  - `radar run-once --mock --dry-run`
  - `radar test-alert --dry-run`
  - `radar digest --dry-run`
- Ensure scripts are idempotent where practical.

## Acceptance Criteria

- [ ] Runbook explains VPS install and first-run sequence.
- [ ] systemd unit and timer templates exist.
- [ ] Timer cadence is every 6 hours.
- [ ] `.env` remains local/VPS-only.
- [ ] Scripts do not embed secrets.
- [ ] Deployment templates reference the project path and venv clearly.
- [ ] Local dev without systemd can still run all mock/dry-run commands manually.

## Tests and Checks

- Static test that systemd templates include expected command and timer cadence.
- Shellcheck if available, otherwise basic script syntax checks.
- README/runbook review against acceptance criteria.

## Risks

- VPS paths vary; templates should document variables or placeholders.
- systemd may not exist in local dev; do not make local tests require it.

## Assumptions

- Deployment target is a Linux VPS with systemd.
- Operator will place real `.env` on the VPS outside git.
