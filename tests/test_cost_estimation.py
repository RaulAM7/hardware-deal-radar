from __future__ import annotations

from hardware_deal_radar.config.loader import load_config_bundle
from hardware_deal_radar.pipeline.normalize import normalize_listing
from hardware_deal_radar.settings import load_settings
from hardware_deal_radar.sources.mock_source import MockSourceClient


def test_uk_listing_gets_import_adjustment(isolated_project) -> None:
    bundle = load_config_bundle("config")
    raw = MockSourceClient().search(
        bundle.searches.searches[0],
        "EBAY_GB",
        bundle.marketplaces.marketplaces["EBAY_GB"],
        load_settings(),
    )[2]
    listing = normalize_listing(raw, bundle)
    assert listing.estimated_import_cost_eur is not None
    assert listing.estimated_total_eur > listing.price_amount
