from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path

from hardware_deal_radar.alerts.email import EmailAlerter
from hardware_deal_radar.alerts.formatter import format_digest, format_telegram_alert
from hardware_deal_radar.alerts.noop import NoopAlerter
from hardware_deal_radar.alerts.telegram import TelegramAlerter
from hardware_deal_radar.config.loader import ConfigBundle, ConfigError, load_config_bundle
from hardware_deal_radar.models import AlertSendResult, ListingCandidate, RunSummary, ScoreResult
from hardware_deal_radar.pipeline.alert_decision import decide_alert
from hardware_deal_radar.pipeline.normalize import normalize_listing
from hardware_deal_radar.pipeline.score import score_candidate
from hardware_deal_radar.reports.digest import collect_digest_candidates
from hardware_deal_radar.settings import Settings, load_settings
from hardware_deal_radar.sources.base import SourceClient, SourceError
from hardware_deal_radar.sources.ebay_client import EbayBrowseClient
from hardware_deal_radar.sources.mock_source import MockSourceClient
from hardware_deal_radar.storage.alerts_repo import AlertsRepository
from hardware_deal_radar.storage.db import create_sqlite_engine, init_db, session_scope
from hardware_deal_radar.storage.listings_repo import ListingsRepository
from hardware_deal_radar.storage.runs_repo import RunsRepository

LOGGER = logging.getLogger(__name__)


@dataclass
class RuntimeOptions:
    config_dir: str = "config"
    use_mock: bool = False
    dry_run: bool = False
    noop: bool = False
    db_path_override: str | None = None


def load_runtime(config_dir: str = "config") -> tuple[Settings, ConfigBundle]:
    settings = load_settings()
    config = load_config_bundle(config_dir)
    return settings, config


def run_once(options: RuntimeOptions) -> RunSummary:
    settings, config = load_runtime(options.config_dir)
    if options.db_path_override:
        settings.RADAR_DB_PATH = options.db_path_override
    LOGGER.info("run_once start mode=%s db=%s", _mode_label(options), settings.db_path())
    engine = create_sqlite_engine(settings.db_path())
    init_db(engine)
    with session_scope(engine) as session:
        runs = RunsRepository(session)
        listings = ListingsRepository(session)
        alerts = AlertsRepository(session)
        run_record = runs.create_run(_mode_label(options))
        summary = RunSummary()
        summary.searches_count = len(config.searches.searches)
        summary.marketplaces_count = sum(
            len(search.marketplaces) for search in config.searches.searches
        )
        sender = _build_sender(settings, options)
        source_client: SourceClient = MockSourceClient() if options.use_mock else EbayBrowseClient()
        for search in config.searches.searches:
            if not search.enabled:
                continue
            for marketplace_name in search.marketplaces:
                marketplace = config.marketplaces.marketplaces[marketplace_name]
                try:
                    raw_listings = source_client.search(
                        search, marketplace_name, marketplace, settings
                    )
                except SourceError as exc:
                    LOGGER.warning(
                        "source error search=%s marketplace=%s error=%s",
                        search.name,
                        marketplace_name,
                        exc,
                    )
                    runs.log_error(
                        run_record.id, "source_error", str(exc), "ebay", marketplace_name
                    )
                    summary.errors_count += 1
                    continue
                summary.raw_results_count += len(raw_listings)
                for raw_listing in raw_listings:
                    candidate = normalize_listing(raw_listing, config)
                    score = score_candidate(candidate, search, config.scoring, marketplace)
                    upsert = listings.upsert_listing(candidate, score, run_record.id or 0)
                    if upsert.is_new:
                        summary.new_listings_count += 1
                    elif upsert.changed_fields:
                        summary.updated_listings_count += 1
                    summary.listings.append(candidate)
                    summary.scored.append((candidate, score))
                    strong_threshold = (
                        search.strong_alert_threshold or config.scoring.thresholds.strong_alert
                    )
                    digest_threshold = search.digest_threshold or config.scoring.thresholds.digest
                    decision = decide_alert(
                        score,
                        upsert,
                        strong_threshold,
                        digest_threshold,
                        has_previous_strong_alert=alerts.has_strong_alert(upsert.listing_id),
                    )
                    if decision.include_in_digest:
                        summary.digest_candidates_count += 1
                    if decision.should_send:
                        payload = format_telegram_alert(candidate, score)
                        send_result = sender.send(payload)
                        alerts.record_alert(
                            upsert.listing_id,
                            run_record.id,
                            decision,
                            send_result,
                            score.score_total,
                            candidate.estimated_total_eur,
                        )
                        if send_result.status in {"sent", "simulated"}:
                            summary.strong_alerts_count += 1
                        else:
                            LOGGER.warning(
                                "strong alert failed listing_id=%s status=%s",
                                upsert.listing_id,
                                send_result.status,
                            )
                            summary.errors_count += 1
        runs.finish_run(
            run_record, summary, status="success" if not summary.errors_count else "partial_failure"
        )
        LOGGER.info(
            "run_once end raw=%s new=%s updated=%s strong_alerts=%s digest=%s errors=%s",
            summary.raw_results_count,
            summary.new_listings_count,
            summary.updated_listings_count,
            summary.strong_alerts_count,
            summary.digest_candidates_count,
            summary.errors_count,
        )
        return summary


def generate_digest(options: RuntimeOptions) -> str:
    settings, config = load_runtime(options.config_dir)
    if options.db_path_override:
        settings.RADAR_DB_PATH = options.db_path_override
    LOGGER.info("digest start db=%s", settings.db_path())
    engine = create_sqlite_engine(settings.db_path())
    init_db(engine)
    with session_scope(engine) as session:
        entries = collect_digest_candidates(session, config.scoring)
    run_summary = f"Digest candidates: {len(entries)}"
    payload = format_digest(entries, run_summary)
    if not entries:
        LOGGER.info("digest skipped because no candidates met threshold")
        return payload
    sender = _build_sender(settings, options, digest=True)
    result = sender.send(payload)
    with session_scope(engine) as session:
        alerts = AlertsRepository(session)
        channel = "noop" if options.dry_run or options.noop else "email"
        for entry in entries:
            alerts.record_event(
                listing_id=entry.listing_id,
                run_id=None,
                alert_type="digest",
                channel=channel,
                threshold=config.scoring.thresholds.digest,
                send_result=result,
                score_total=entry.score.score_total,
                estimated_total_eur=entry.candidate.estimated_total_eur,
            )
    if options.dry_run or options.noop:
        LOGGER.info("digest simulated candidates=%s", len(entries))
        return payload
    if result.status == "failed":
        LOGGER.warning("digest send failed status=%s", result.status)
        raise RuntimeError(result.error_message or "digest send failed")
    LOGGER.info("digest sent candidates=%s", len(entries))
    return payload


def test_alert(options: RuntimeOptions) -> AlertSendResult:
    settings, _config = load_runtime(options.config_dir)
    candidate = ListingCandidate(
        marketplace="EBAY_DE",
        title="ThinkPad P14s Gen 4 AMD Ryzen 7 PRO 7840U 64GB RAM 1TB SSD",
        item_country="DE",
        seller_username="test-seller",
        ram_gb=64,
        ssd_gb=1024,
        cpu_text="Ryzen 7 PRO 7840U",
        estimated_total_eur=799,
        canonical_url="https://example.invalid/listing",
    )
    score = ScoreResult(
        score_total=88,
        positive_reasons=["64GB RAM", "modern CPU", "business seller", "returns accepted"],
        negative_reasons=["keyboard unknown"],
        risk_flags=["keyboard_layout_risk"],
        recommendation="strong_candidate",
    )
    payload = format_telegram_alert(candidate, score)
    sender = _build_sender(settings, options)
    result = sender.send(payload)
    LOGGER.info("test_alert status=%s", result.status)
    return result


def _build_sender(settings: Settings, options: RuntimeOptions, digest: bool = False):
    if options.dry_run or options.noop:
        return NoopAlerter()
    if digest:
        return EmailAlerter(settings)
    return TelegramAlerter(settings)


def _mode_label(options: RuntimeOptions) -> str:
    flags = []
    if options.use_mock:
        flags.append("mock")
    if options.dry_run:
        flags.append("dry_run")
    if options.noop:
        flags.append("noop")
    return ",".join(flags) or "real"


def doctor_report(config_dir: str = "config") -> list[tuple[str, str]]:
    settings = load_settings()
    rows: list[tuple[str, str]] = []
    env_path = Path(".env")
    rows.append(("env_file", "present" if env_path.exists() else "missing"))
    if env_path.exists():
        mode_bits = env_path.stat().st_mode & 0o777
        mode = oct(mode_bits)
        rows.append(("env_permissions", mode))
        if mode_bits & 0o077:
            rows.append(("env_permissions_warning", "expected 0o600"))
    rows.extend(settings.credential_status().items())
    rows.append(("db_parent", "present" if settings.db_path().parent.exists() else "missing"))
    try:
        load_config_bundle(config_dir)
        rows.append(("config", "valid"))
    except ConfigError as exc:
        rows.append(("config", f"invalid: {exc}"))
    return rows
