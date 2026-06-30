from __future__ import annotations

from hardware_deal_radar.config.loader import load_config_bundle
from hardware_deal_radar.pipeline.normalize import normalize_listing
from hardware_deal_radar.pipeline.score import score_candidate
from hardware_deal_radar.settings import load_settings
from hardware_deal_radar.sources.mock_source import MockSourceClient
from hardware_deal_radar.storage.db import create_sqlite_engine, init_db, session_scope
from hardware_deal_radar.storage.listings_repo import ListingsRepository


def test_storage_creates_and_updates_listing(isolated_project) -> None:
    bundle = load_config_bundle("config")
    search = bundle.searches.searches[0]
    marketplace = bundle.marketplaces.marketplaces["EBAY_DE"]
    raw = MockSourceClient().search(search, "EBAY_DE", marketplace, load_settings())[0]
    listing = normalize_listing(raw, bundle)
    score = score_candidate(listing, search, bundle.scoring, marketplace)
    engine = create_sqlite_engine((isolated_project / "data" / "test.sqlite").resolve())
    init_db(engine)
    with session_scope(engine) as session:
        repo = ListingsRepository(session)
        result = repo.upsert_listing(listing, score, 1)
        assert result.is_new is True
        result2 = repo.upsert_listing(listing, score, 2)
        assert result2.is_new is False
        assert repo.list_recent(limit=5)
