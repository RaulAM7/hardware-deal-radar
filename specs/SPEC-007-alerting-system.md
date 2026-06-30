# SPEC-007 - Alerting System

## Objective

Implement Telegram strong alerts, SMTP email digest, noop/dry-run alert behavior, formatting, and anti-duplicate alert decisions.

## Scope

- Format actionable Telegram messages.
- Format email digest messages.
- Implement Telegram Bot API adapter.
- Implement SMTP adapter.
- Implement noop adapter for console/file simulation.
- Record sent, simulated, skipped, and failed alert statuses.
- Avoid duplicate alerts except for significant changes.

## Out of Scope

- WhatsApp, Slack, mobile app, or web notifications.
- Rich HTML email design beyond readable plain or simple HTML output.
- User interaction flows from alerts.

## Expected Files and Modules

- `src/hardware_deal_radar/alerts/formatter.py`
- `src/hardware_deal_radar/alerts/telegram.py`
- `src/hardware_deal_radar/alerts/email.py`
- `src/hardware_deal_radar/alerts/noop.py`
- `src/hardware_deal_radar/pipeline/alert_decision.py`
- `src/hardware_deal_radar/reports/digest.py`
- `tests/test_alert_decision.py`
- `tests/test_alert_formatting.py`
- `tests/test_noop_alerts.py`

## Tasks

- Implement Telegram message with title, model, RAM, SSD, CPU, marketplace, country, seller, price, shipping, estimated total, score, positives, risks, and link.
- Implement digest with run summary, top candidates, medium candidates, price drops, risks, and links.
- Enforce strong alert threshold from search or global scoring config.
- Enforce digest threshold from search or global scoring config.
- Check alert history before sending strong alerts.
- Re-alert only on relevant price drop, score crossing threshold, or critical data change.
- In dry-run, do not send real Telegram/SMTP; record simulated or print via noop.
- Sanitize all error messages and payload previews.
- Add `radar test-alert --dry-run` behavior against static fake candidate.

## Acceptance Criteria

- [ ] Strong candidate produces one Telegram alert decision.
- [ ] Same unchanged listing does not alert twice.
- [ ] Price drop can trigger a new alert.
- [ ] Digest includes watch candidates and run summary.
- [ ] Dry-run sends no real external message.
- [ ] Noop adapter works without credentials.
- [ ] Telegram/SMTP failures are recorded and do not break persistence.

## Tests and Checks

- Test alert formatting contains decision fields.
- Test duplicate suppression.
- Test price-drop re-alert.
- Test digest candidate selection.
- Test dry-run/noop paths without secrets.
- Test sanitized adapter errors.

## Risks

- Alerts can become noisy if duplicate rules are loose; default to suppress unless change is significant.
- Message formatting can expose too much raw payload; include only decision-relevant fields.

## Assumptions

- Telegram is the urgent channel.
- Email digest is daily/manual and can be generated on demand by CLI.
