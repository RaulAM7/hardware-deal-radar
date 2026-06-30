from __future__ import annotations

from hardware_deal_radar.config.loader import ConfigBundle
from hardware_deal_radar.models import ListingCandidate
from hardware_deal_radar.sources.base import RawListing
from hardware_deal_radar.sources.ebay_normalizer import normalize_item


def normalize_listing(raw_listing: RawListing, config: ConfigBundle) -> ListingCandidate:
    marketplace = config.marketplaces.marketplaces[raw_listing.marketplace]
    return normalize_item(raw_listing, marketplace, config.scoring)
