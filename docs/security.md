# Security

## Secret Handling Rules

- real secrets live only in local or VPS `.env`
- `.env` stays ignored by git
- `.env.example` contains variable names and safe defaults only
- no command should print real secret values
- logs, DB payload previews, and docs must remain sanitized

## GitHub

- the public repo may contain `.env.example`
- the public repo must not contain `.env`
- if GitHub push protection flags a secret, rotate the secret and remove it from history before pushing
- future CI integrations should use GitHub Secrets, not tracked files

## Logging

The app logs:

- run start and end
- sanitized external errors
- strong alert and digest outcomes

The app does not log:

- eBay client secret
- eBay bearer token
- Telegram bot token
- SMTP password

## Database and Payloads

SQLite stores:

- normalized listing data
- score explanations
- alert history
- run summaries
- sanitized error logs

SQLite must not store credentials or auth headers.

## VPS Practices

- keep `.env` at repo root on the VPS
- apply `chmod 600 .env`
- run the systemd service as a dedicated non-root user when possible
- restrict repo directory ownership to the operator/service user
- inspect logs with `journalctl` instead of ad hoc shell history containing secrets

## Safe Validation Workflow

Use these commands before turning on real mode:

```bash
.venv/bin/radar doctor
.venv/bin/radar validate-config
.venv/bin/radar run-once --mock --dry-run
.venv/bin/radar test-alert --dry-run
.venv/bin/radar digest --dry-run
```

## Incident Response

If a secret is exposed:

1. rotate the secret immediately
2. remove it from tracked files and commit history if needed
3. update the VPS `.env`
4. rerun `radar doctor`
5. verify the remote repo no longer contains the secret

