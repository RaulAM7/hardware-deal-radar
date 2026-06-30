from __future__ import annotations

import json

import typer
import yaml
from rich.console import Console
from rich.table import Table

from hardware_deal_radar.config.loader import ConfigError, load_config_bundle
from hardware_deal_radar.pipeline.run import (
    RuntimeOptions,
    doctor_report,
    generate_digest,
    run_once,
    test_alert,
)
from hardware_deal_radar.reports.recent import explain_listing, listing_summary
from hardware_deal_radar.settings import load_settings
from hardware_deal_radar.storage.db import create_sqlite_engine, init_db, session_scope
from hardware_deal_radar.storage.listings_repo import ListingsRepository
from hardware_deal_radar.utils.logging import configure_logging

app = typer.Typer(no_args_is_help=True)
console = Console()


def _build_options(
    config_dir: str,
    mock: bool,
    dry_run: bool,
    noop: bool,
    db_path: str | None,
) -> RuntimeOptions:
    return RuntimeOptions(
        config_dir=config_dir,
        use_mock=mock,
        dry_run=dry_run,
        noop=noop,
        db_path_override=db_path,
    )


@app.callback()
def main(log_level: str = typer.Option("INFO", "--log-level")) -> None:
    configure_logging(log_level)


@app.command("validate-config")
def validate_config(config_dir: str = typer.Option("config", "--config-dir")) -> None:
    try:
        load_config_bundle(config_dir)
    except ConfigError as exc:
        console.print(str(exc))
        raise typer.Exit(code=1) from exc
    console.print("Config is valid.")


@app.command("show-config")
def show_config(config_dir: str = typer.Option("config", "--config-dir")) -> None:
    try:
        config = load_config_bundle(config_dir)
    except ConfigError as exc:
        console.print(str(exc))
        raise typer.Exit(code=1) from exc
    console.print(yaml.safe_dump(config.sanitized_dump(), sort_keys=False))


@app.command("run-once")
def run_once_command(
    config_dir: str = typer.Option("config", "--config-dir"),
    mock: bool = typer.Option(False, "--mock"),
    dry_run: bool = typer.Option(False, "--dry-run"),
    noop: bool = typer.Option(False, "--noop"),
    db_path: str | None = typer.Option(None, "--db-path"),
) -> None:
    try:
        summary = run_once(_build_options(config_dir, mock, dry_run, noop, db_path))
    except (ConfigError, RuntimeError) as exc:
        console.print(str(exc))
        raise typer.Exit(code=1) from exc
    console.print(json.dumps(summary.model_dump(mode="json"), default=str, indent=2))


@app.command("digest")
def digest_command(
    config_dir: str = typer.Option("config", "--config-dir"),
    dry_run: bool = typer.Option(False, "--dry-run"),
    noop: bool = typer.Option(False, "--noop"),
    db_path: str | None = typer.Option(None, "--db-path"),
) -> None:
    try:
        payload = generate_digest(_build_options(config_dir, False, dry_run, noop, db_path))
    except (ConfigError, RuntimeError) as exc:
        console.print(str(exc))
        raise typer.Exit(code=1) from exc
    console.print(payload)


@app.command("test-alert")
def test_alert_command(
    config_dir: str = typer.Option("config", "--config-dir"),
    dry_run: bool = typer.Option(False, "--dry-run"),
    noop: bool = typer.Option(False, "--noop"),
) -> None:
    try:
        result = test_alert(_build_options(config_dir, False, dry_run, noop, None))
    except ConfigError as exc:
        console.print(str(exc))
        raise typer.Exit(code=1) from exc
    console.print(result.status)


@app.command("list-recent")
def list_recent(
    db_path: str | None = typer.Option(None, "--db-path"),
) -> None:
    settings = load_settings()
    if db_path:
        settings.RADAR_DB_PATH = db_path
    engine = create_sqlite_engine(settings.db_path())
    init_db(engine)
    with session_scope(engine) as session:
        records = ListingsRepository(session).list_recent()
    if not records:
        console.print("No listings stored yet.")
        return
    table = Table("ID", "Listing")
    for record in records:
        table.add_row(str(record.id), listing_summary(record))
    console.print(table)


@app.command("explain-score")
def explain_score(listing_id: int, db_path: str | None = typer.Option(None, "--db-path")) -> None:
    settings = load_settings()
    if db_path:
        settings.RADAR_DB_PATH = db_path
    engine = create_sqlite_engine(settings.db_path())
    init_db(engine)
    with session_scope(engine) as session:
        record = ListingsRepository(session).get_listing(listing_id)
    if record is None:
        raise typer.Exit(code=1)
    console.print(explain_listing(record))


@app.command("doctor")
def doctor(config_dir: str = typer.Option("config", "--config-dir")) -> None:
    rows = doctor_report(config_dir)
    table = Table("Check", "Status")
    for name, status in rows:
        table.add_row(name, status)
    console.print(table)
