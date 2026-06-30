# SPEC-005 - Storage and Deduplication

## Objective

Implement SQLite persistence, run tracking, listing upsert, deduplication, alert history, price history, and sanitized error logging.

## Scope

- Create SQLModel table models from `docs/data-model-v1.md`.
- Initialize SQLite database automatically.
- Implement repositories for runs, listings, alerts, price history, and errors.
- Implement deduplication identity and update detection.
- Support temporary SQLite DBs for tests.

## Out of Scope

- Alembic migrations unless trivial and non-blocking.
- Remote databases.
- Advanced analytics.
- Multi-user access controls.

## Expected Files and Modules

- `src/hardware_deal_radar/storage/db.py`
- `src/hardware_deal_radar/storage/models.py`
- `src/hardware_deal_radar/storage/listings_repo.py`
- `src/hardware_deal_radar/storage/alerts_repo.py`
- `src/hardware_deal_radar/storage/runs_repo.py`
- `tests/test_storage.py`
- `tests/test_deduplication.py`

## Tasks

- Implement DB engine creation from `RADAR_DB_PATH`.
- Create parent data directory when safe.
- Define SQLModel tables: runs, listings, alerts, price_history, error_logs.
- Add indexes and unique constraints for dedup keys where SQLite supports them simply.
- Implement `upsert_listing` by preferred source identity and fallbacks.
- Detect relevant changes and update `last_changed_at`.
- Record price history when price/shipping/estimated total changes.
- Record alerts and prevent duplicate strong alerts unless significant change occurs.
- Sanitize error logs and alert payload previews.

## Acceptance Criteria

- [ ] Database tables are created on first run.
- [ ] Re-seeing the same listing does not create duplicates.
- [ ] Price changes create history records.
- [ ] Alert history can answer whether a strong alert was already sent.
- [ ] Run records include counts and status.
- [ ] No secrets are persisted.
- [ ] Storage tests pass using a temporary SQLite file.

## Tests and Checks

- Test table creation.
- Test insert new listing.
- Test update existing listing by source item ID.
- Test fallback dedup by canonical URL.
- Test price history creation.
- Test alert duplicate query.
- Test sanitized error log.

## Risks

- Dedup fallbacks can merge distinct listings if too aggressive; prefer source item ID and canonical URL.
- JSON text fields need consistent serialization.

## Assumptions

- Automatic table creation is enough for v1.
- SQLite is local to the VPS and not shared by concurrent writers beyond scheduled/manual runs.
