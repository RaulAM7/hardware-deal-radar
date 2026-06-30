# Credential Strategy

## Rules

- Never commit `.env`.
- Never print real secrets.
- Never log real secrets.
- Never copy real secrets into docs, tests, fixtures, snapshots, or examples.
- Never ask the user to paste secrets into prompts.
- `.env.example` contains names and safe defaults only.
- `.env` is local/VPS-only and is ignored by git.

## Environment Variables

Canonical variables are defined by root `.env.example`:

- `EBAY_ENV`
- `EBAY_CLIENT_ID`
- `EBAY_CLIENT_SECRET`
- `EBAY_SCOPE`
- `EBAY_MARKETPLACE_DEFAULT`
- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_CHAT_ID`
- `SMTP_HOST`
- `SMTP_PORT`
- `SMTP_USERNAME`
- `SMTP_PASSWORD`
- `SMTP_FROM`
- `DIGEST_EMAIL_TO`
- `RADAR_ENV`
- `RADAR_DB_PATH`
- `RADAR_LOG_LEVEL`

## Runtime Requirements

- Real eBay mode requires `EBAY_CLIENT_ID` and `EBAY_CLIENT_SECRET`.
- Real Telegram alerting requires `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID`.
- Real email digest requires SMTP variables.
- Mock, dry-run, and noop modes must not require real eBay, Telegram, or SMTP credentials.

## Doctor Checks

`radar doctor` must report:

- `.env` present or absent.
- required real-mode variables present or missing, without values.
- `.env` file permissions warning if readable by group/world.
- config YAML validity.
- DB path parent directory availability.
- eBay reachability only when real eBay check is requested or real mode is active.
- Telegram token/chat readiness only when real Telegram check is requested or real mode is active.
- SMTP readiness only when email digest is enabled in real mode.

## Secret Handling in Code

- Settings objects must mask secret values in `repr`, Rich output, logs, errors, and diagnostics.
- HTTP errors must not include Authorization headers.
- SMTP errors must not include passwords.
- Alert payload previews must include message content but not credentials.
- Raw payload JSON may store marketplace item data only, never auth data.

## GitHub and VPS

- Public GitHub repo stores only `.env.example`.
- VPS stores real `.env` with permissions `600`.
- If GitHub Actions are added later, use GitHub Secrets, not repo files.
