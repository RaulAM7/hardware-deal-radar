# Troubleshooting

## `radar doctor` shows missing credentials

That is expected until you configure the real `.env`.

Safe path forward:

```bash
.venv/bin/radar run-once --mock --dry-run
.venv/bin/radar test-alert --dry-run
```

`doctor` reports variable names and readiness only. It does not print secret values.

## `validate-config` fails

Common causes:

- missing `config/searches.yaml`, `config/scoring.yaml`, or `config/marketplaces.yaml`
- invalid YAML syntax
- a search referencing an unknown marketplace
- threshold ordering that violates `strong > digest > ignore_below`

Recover by comparing runtime files against `config/*.example.yaml`.

## `run-once --mock --dry-run` works but real `run-once` fails

Likely causes:

- invalid eBay credentials
- outbound network restrictions on the VPS
- eBay rate or auth errors

Check:

```bash
.venv/bin/radar doctor
journalctl -u hardware-deal-radar.service -n 100 --no-pager
```

## Telegram alerts do not arrive

Check that both are configured:

- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_CHAT_ID`

Then run:

```bash
.venv/bin/radar test-alert
```

If that fails, inspect journald logs. The app records a sanitized failure instead of printing credentials.

## Digest does not send

Check:

- `SMTP_HOST`
- `SMTP_FROM`
- `DIGEST_EMAIL_TO`
- `SMTP_USERNAME` and `SMTP_PASSWORD` if the provider requires auth

For a safe validation:

```bash
.venv/bin/radar digest --dry-run
```

## No listings in `list-recent`

The database is empty or the app is writing to a different DB path.

Confirm:

```bash
.venv/bin/radar doctor
ls -l data/
```

Then run:

```bash
.venv/bin/radar run-once --mock --dry-run
```

## systemd timer does not fire

Check:

```bash
systemctl status hardware-deal-radar.timer
systemctl list-timers hardware-deal-radar.timer
journalctl -u hardware-deal-radar.timer -n 50 --no-pager
```

If the unit files changed, reload systemd:

```bash
sudo systemctl daemon-reload
sudo systemctl restart hardware-deal-radar.timer
```

## `.env` permissions warning

The intended mode is:

```bash
chmod 600 .env
```

This removes group/world readability on the VPS.

