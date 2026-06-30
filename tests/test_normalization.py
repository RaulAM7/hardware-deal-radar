from __future__ import annotations

from hardware_deal_radar.config.loader import load_config_bundle
from hardware_deal_radar.pipeline.normalize import normalize_listing
from hardware_deal_radar.settings import load_settings
from hardware_deal_radar.sources.mock_source import MockSourceClient


def test_normalize_listing_extracts_fields(isolated_project) -> None:
    bundle = load_config_bundle("config")
    raw = MockSourceClient().search(
        bundle.searches.searches[0],
        "EBAY_DE",
        bundle.marketplaces.marketplaces["EBAY_DE"],
        load_settings(),
    )[0]
    listing = normalize_listing(raw, bundle)
    assert listing.model_family == "P14s"
    assert listing.ram_gb == 64
    assert listing.ssd_gb == 1024
    assert listing.cpu_text is not None
    assert listing.estimated_total_eur is not None


def test_normalize_listing_marks_reject_keywords(isolated_project) -> None:
    bundle = load_config_bundle("config")
    raw = MockSourceClient().search(
        bundle.searches.searches[0],
        "EBAY_GB",
        bundle.marketplaces.marketplaces["EBAY_GB"],
        load_settings(),
    )[2]
    listing = normalize_listing(raw, bundle)
    assert "possible_parts_only" in listing.risk_flags
    assert listing.matched_reject_keywords
