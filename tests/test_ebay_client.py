from __future__ import annotations

import httpx
import pytest

from hardware_deal_radar.config.loader import load_config_bundle
from hardware_deal_radar.settings import Settings
from hardware_deal_radar.sources.base import SourceError
from hardware_deal_radar.sources.ebay_client import EbayBrowseClient, sanitize_headers


def test_sanitize_headers_masks_auth() -> None:
    assert sanitize_headers({"Authorization": "secret"})["Authorization"] == "<masked>"


def test_ebay_client_request_flow(isolated_project) -> None:
    captured = {"token": False, "search": False}

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith("/oauth2/token"):
            captured["token"] = True
            assert "Basic" in request.headers["Authorization"]
            return httpx.Response(200, json={"access_token": "token"})
        captured["search"] = True
        assert request.headers["X-EBAY-C-MARKETPLACE-ID"] == "EBAY_DE"
        return httpx.Response(
            200, json={"itemSummaries": [{"itemId": "1", "title": "ThinkPad T14 32GB"}]}
        )

    client = httpx.Client(transport=httpx.MockTransport(handler))
    bundle = load_config_bundle("config")
    search = bundle.searches.searches[0]
    marketplace = bundle.marketplaces.marketplaces["EBAY_DE"]
    settings = Settings.model_validate(
        {
            "EBAY_CLIENT_ID": "id",
            "EBAY_CLIENT_SECRET": "secret",
        }
    )
    results = EbayBrowseClient(client=client).search(search, "EBAY_DE", marketplace, settings)
    assert captured["token"] is True
    assert captured["search"] is True
    assert results[0].payload["itemId"] == "1"


def test_ebay_client_requires_credentials(isolated_project) -> None:
    bundle = load_config_bundle("config")
    search = bundle.searches.searches[0]
    marketplace = bundle.marketplaces.marketplaces["EBAY_DE"]
    with pytest.raises(SourceError):
        EbayBrowseClient(client=httpx.Client(transport=httpx.MockTransport(lambda _: None))).search(
            search,
            "EBAY_DE",
            marketplace,
            Settings(),
        )
