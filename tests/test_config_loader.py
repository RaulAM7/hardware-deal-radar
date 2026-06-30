from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from hardware_deal_radar.config.loader import ConfigError, load_config_bundle


def test_load_valid_config(isolated_project: Path) -> None:
    bundle = load_config_bundle("config")
    assert bundle.searches.searches
    assert "EBAY_DE" in bundle.marketplaces.marketplaces


def test_invalid_marketplace_reference(isolated_project: Path) -> None:
    path = isolated_project / "config" / "searches.yaml"
    data = yaml.safe_load(path.read_text())
    data["searches"][0]["marketplaces"] = ["EBAY_XY"]
    path.write_text(yaml.safe_dump(data), encoding="utf-8")
    with pytest.raises(ConfigError):
        load_config_bundle("config")


def test_invalid_threshold_order(isolated_project: Path) -> None:
    path = isolated_project / "config" / "scoring.yaml"
    data = yaml.safe_load(path.read_text())
    data["thresholds"]["strong_alert"] = 50
    path.write_text(yaml.safe_dump(data), encoding="utf-8")
    with pytest.raises(ConfigError):
        load_config_bundle("config")
