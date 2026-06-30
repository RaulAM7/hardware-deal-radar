# Module Design v1

## Package Layout

```txt
src/hardware_deal_radar/
  __init__.py
  main.py
  cli.py
  settings.py
  config/
    __init__.py
    loader.py
    schemas.py
  sources/
    __init__.py
    base.py
    ebay_client.py
    ebay_normalizer.py
    mock_source.py
  pipeline/
    __init__.py
    run.py
    normalize.py
    enrich.py
    cost.py
    score.py
    alert_decision.py
  storage/
    __init__.py
    db.py
    models.py
    listings_repo.py
    alerts_repo.py
    runs_repo.py
  alerts/
    __init__.py
    formatter.py
    telegram.py
    email.py
    noop.py
  reports/
    __init__.py
    digest.py
    recent.py
  utils/
    __init__.py
    logging.py
    money.py
    text.py
    time.py
```

## Module Responsibilities

- `main.py`: console-script entrypoint that calls the Typer app.
- `cli.py`: commands, flags, exit codes, Rich output.
- `settings.py`: `.env` loading, environment schema, safe secret handling.
- `config.loader`: reads YAML files and merges defaults.
- `config.schemas`: Pydantic models for searches, scoring, marketplaces.
- `sources.base`: `SourceClient` protocol and raw listing types.
- `sources.ebay_client`: eBay OAuth, search requests, pagination, error mapping.
- `sources.ebay_normalizer`: converts eBay payloads into normalized listing candidates.
- `sources.mock_source`: fixture source for `--mock` mode.
- `pipeline.run`: run orchestration across searches and marketplaces.
- `pipeline.enrich`: RAM/SSD/CPU/model/keyboard extraction.
- `pipeline.cost`: total EUR estimate and marketplace risk adjustments.
- `pipeline.score`: deterministic score calculation and explanations.
- `pipeline.alert_decision`: strong/digest/ignore/reject decision plus anti-duplicate checks.
- `storage.db`: engine/session/table creation.
- `storage.models`: SQLModel tables.
- `storage.*_repo`: query/update operations only.
- `alerts.formatter`: Telegram and digest message text, sanitized.
- `alerts.telegram`: Telegram Bot API adapter.
- `alerts.email`: SMTP digest adapter.
- `alerts.noop`: console/file simulated outbound adapter.
- `reports.digest`: digest candidate aggregation.
- `reports.recent`: `list-recent` and score explanation view models.
- `utils.*`: shared pure helpers.

## Public Internal Interfaces

Source client:

```txt
search(search_config, marketplace_config, settings) -> list[RawListing]
```

Normalizer:

```txt
normalize(raw_listing, marketplace_config) -> ListingCandidate
```

Scorer:

```txt
score(candidate, scoring_config) -> ScoreResult
```

Alert decision:

```txt
decide_alert(candidate, score_result, alert_history, thresholds) -> AlertDecision
```

Repositories:

```txt
upsert_listing(candidate, score_result, run_id) -> ListingRecord
record_alert(alert_decision, status) -> AlertRecord
record_run_start(settings, config) -> RunRecord
record_run_finish(run_id, summary) -> RunRecord
```

## Test Boundaries

- Unit tests cover config schemas, text extraction, cost estimation, scoring, dedup keys, and alert decision rules.
- Adapter tests use mocked HTTP/SMTP/Telegram clients.
- End-to-end tests use mock fixtures and a temporary SQLite database.
- No test depends on real credentials.
