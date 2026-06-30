from __future__ import annotations

from hardware_deal_radar.config.loader import load_config_bundle
from hardware_deal_radar.settings import load_settings
from hardware_deal_radar.sources.mock_source import MockSourceClient


def test_mock_source_returns_items(isolated_project) -> None:
    bundle = load_config_bundle("config")
    search = bundle.searches.searches[0]
    marketplace = bundle.marketplaces.marketplaces["EBAY_DE"]
    results = MockSourceClient().search(search, "EBAY_DE", marketplace, load_settings())
    assert len(results) >= 1
    assert results[0].payload["title"].startswith("Lenovo ThinkPad")
