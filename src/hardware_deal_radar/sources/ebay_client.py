from __future__ import annotations

import base64
from collections.abc import Mapping
from typing import Any

import httpx

from hardware_deal_radar.config.schemas import MarketplaceConfig, SearchConfig
from hardware_deal_radar.settings import Settings
from hardware_deal_radar.sources.base import RawListing, SourceError


class EbayBrowseClient:
    def __init__(self, client: httpx.Client | None = None, timeout: float = 10.0) -> None:
        self._client = client or httpx.Client(timeout=timeout)

    def _base_url(self, env: str) -> str:
        return "https://api.ebay.com" if env == "production" else "https://api.sandbox.ebay.com"

    def _fetch_token(self, settings: Settings) -> str:
        client_id = settings.EBAY_CLIENT_ID.get_secret_value() if settings.EBAY_CLIENT_ID else ""
        client_secret = (
            settings.EBAY_CLIENT_SECRET.get_secret_value() if settings.EBAY_CLIENT_SECRET else ""
        )
        if not client_id or not client_secret:
            raise SourceError("Missing required eBay credentials: EBAY_CLIENT_ID, EBAY_CLIENT_SECRET")

        basic = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode("ascii")
        response = self._client.post(
            f"{self._base_url(settings.EBAY_ENV)}/identity/v1/oauth2/token",
            headers={
                "Authorization": f"Basic {basic}",
                "Content-Type": "application/x-www-form-urlencoded",
            },
            data={"grant_type": "client_credentials", "scope": settings.EBAY_SCOPE},
        )
        if response.status_code >= 400:
            raise SourceError(f"eBay token request failed with status {response.status_code}")
        access_token = response.json().get("access_token")
        if not access_token:
            raise SourceError("eBay token response did not include access_token")
        return str(access_token)

    def search(
        self,
        search_config: SearchConfig,
        marketplace_name: str,
        marketplace: MarketplaceConfig,
        settings: Settings,
    ) -> list[RawListing]:
        token = self._fetch_token(settings)
        params = {"q": search_config.query, "limit": 25}
        response = self._client.get(
            f"{self._base_url(settings.EBAY_ENV)}/buy/browse/v1/item_summary/search",
            headers={
                "Authorization": f"Bearer {token}",
                "X-EBAY-C-MARKETPLACE-ID": marketplace.marketplace_id,
            },
            params=params,
        )
        if response.status_code >= 400:
            raise SourceError(
                f"eBay search failed for {marketplace_name} with status {response.status_code}"
            )
        payload = response.json()
        items = payload.get("itemSummaries", [])
        if not isinstance(items, list):
            raise SourceError("eBay search response itemSummaries was not a list")
        return [RawListing(source="ebay", marketplace=marketplace_name, payload=item) for item in items]


def sanitize_headers(headers: Mapping[str, Any]) -> dict[str, Any]:
    sanitized = dict(headers)
    if "Authorization" in sanitized:
        sanitized["Authorization"] = "<masked>"
    return sanitized
