# Runbook

## Purpose

This runbook covers local smoke validation and VPS deployment for Hardware Deal Radar.

## Recommended VPS Layout

- App directory: `/opt/hardware-deal-radar`
- Service user: `radar`
- Database path: `./data/radar.sqlite` inside the repo
- Logs: journald via systemd

## Initial Install

1. Clone the repo:

```bash
git clone https://github.com/RaulAM7/hardware-deal-radar.git /opt/hardware-deal-radar
cd /opt/hardware-deal-radar
```

2. Run the bootstrap helper:

```bash
APP_DIR=/opt/hardware-deal-radar ./scripts/install-vps.sh
```

That script:

- installs `uv` if missing
- creates `.venv` through `uv sync --extra dev`
- creates `data/`
- copies `config/*.example.yaml` only when the runtime file is missing
- copies `.env.example` to `.env` only when `.env` is missing
- applies `chmod 600 .env`

## Configure Secrets

Edit `/opt/hardware-deal-radar/.env` directly on the VPS.

Minimum variables by mode:

- mock and dry-run: none required
- real eBay mode: `EBAY_CLIENT_ID`, `EBAY_CLIENT_SECRET`
- real Telegram alerts: `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`
- real digest email: `SMTP_HOST`, `SMTP_FROM`, `DIGEST_EMAIL_TO`, plus auth if required

Never commit or upload the real `.env` to GitHub.

## Preflight Sequence

Run these before enabling the timer:

```bash
.venv/bin/radar doctor
.venv/bin/radar validate-config
.venv/bin/radar run-once --mock --dry-run
.venv/bin/radar test-alert --dry-run
.venv/bin/radar digest --dry-run
```

If all five commands succeed, the repo is ready for a real run.

## Manual Operation

Manual live run:

```bash
.venv/bin/radar run-once
```

Manual dry-run against fixtures:

```bash
.venv/bin/radar run-once --mock --dry-run
```

Manual digest generation:

```bash
.venv/bin/radar digest
```

List recent listings:

```bash
.venv/bin/radar list-recent
```

Explain one listing score:

```bash
.venv/bin/radar explain-score 1
```

## Install systemd Units

Render and install the unit/timer:

```bash
sudo APP_DIR=/opt/hardware-deal-radar RUN_AS_USER=radar ./scripts/setup-systemd.sh
```

The setup script installs:

- `hardware-deal-radar.service`
- `hardware-deal-radar.timer`

## systemd Operations

Enable and start the timer:

```bash
sudo systemctl enable --now hardware-deal-radar.timer
```

Inspect timer status:

```bash
systemctl status hardware-deal-radar.timer
systemctl list-timers hardware-deal-radar.timer
```

Run the service immediately:

```bash
sudo systemctl start hardware-deal-radar.service
```

Disable the timer:

```bash
sudo systemctl disable --now hardware-deal-radar.timer
```

## Logs

Follow service and timer logs:

```bash
journalctl -u hardware-deal-radar.service -f
journalctl -u hardware-deal-radar.timer -f
```

Show the most recent service run:

```bash
journalctl -u hardware-deal-radar.service -n 100 --no-pager
```

## Update Flow

```bash
cd /opt/hardware-deal-radar
git pull --ff-only
~/.local/bin/uv sync --extra dev
.venv/bin/radar doctor
sudo systemctl restart hardware-deal-radar.timer
```

## Rollback

1. `git checkout <known-good-commit>`
2. `~/.local/bin/uv sync --extra dev`
3. `.venv/bin/radar doctor`
4. `sudo systemctl restart hardware-deal-radar.service`

