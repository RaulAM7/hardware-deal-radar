from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol

from hardware_deal_radar.config.schemas import MarketplaceConfig, SearchConfig
from hardware_deal_radar.settings import Settings


class SourceError(RuntimeError):
    """Source request or auth failure."""


@dataclass
class RawListing:
    source: str
    marketplace: str
    payload: dict[str, Any]


class SourceClient(Protocol):
    def search(
        self,
        search_config: SearchConfig,
        marketplace_name: str,
        marketplace: MarketplaceConfig,
        settings: Settings,
    ) -> list[RawListing]: ...
