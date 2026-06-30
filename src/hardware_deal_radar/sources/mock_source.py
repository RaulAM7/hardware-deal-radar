from __future__ import annotations

import json
from importlib import resources

from hardware_deal_radar.config.schemas import MarketplaceConfig, SearchConfig
from hardware_deal_radar.settings import Settings
from hardware_deal_radar.sources.base import RawListing


class MockSourceClient:
    def search(
        self,
        search_config: SearchConfig,
        marketplace_name: str,
        marketplace: MarketplaceConfig,
        settings: Settings,
    ) -> list[RawListing]:
        del search_config, marketplace, settings
        fixture = (
            resources.files("hardware_deal_radar.fixtures")
            .joinpath("mock_ebay_search_response.json")
            .read_text(encoding="utf-8")
        )
        payload = json.loads(fixture)
        items = payload.get("itemSummaries", [])
        return [
            RawListing(source="ebay", marketplace=marketplace_name, payload=item) for item in items
        ]
