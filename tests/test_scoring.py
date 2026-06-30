from __future__ import annotations

from hardware_deal_radar.config.loader import load_config_bundle
from hardware_deal_radar.pipeline.normalize import normalize_listing
from hardware_deal_radar.pipeline.score import score_candidate
from hardware_deal_radar.settings import load_settings
from hardware_deal_radar.sources.mock_source import MockSourceClient


def test_strong_candidate_scores_high(isolated_project) -> None:
    bundle = load_config_bundle("config")
    search = bundle.searches.searches[0]
    marketplace = bundle.marketplaces.marketplaces["EBAY_DE"]
    raw = MockSourceClient().search(search, "EBAY_DE", marketplace, load_settings())[0]
    listing = normalize_listing(raw, bundle)
    score = score_candidate(listing, search, bundle.scoring, marketplace)
    assert score.score_total >= 80
    assert score.recommendation == "strong_candidate"


def test_reject_keyword_listing_rejects(isolated_project) -> None:
    bundle = load_config_bundle("config")
    search = bundle.searches.searches[0]
    marketplace = bundle.marketplaces.marketplaces["EBAY_GB"]
    raw = MockSourceClient().search(search, "EBAY_GB", marketplace, load_settings())[2]
    listing = normalize_listing(raw, bundle)
    score = score_candidate(listing, search, bundle.scoring, marketplace)
    assert score.recommendation == "reject"
