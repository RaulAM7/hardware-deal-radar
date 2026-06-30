from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml
from pydantic import ValidationError

from hardware_deal_radar.config.schemas import MarketplacesFile, ScoringConfig, SearchesFile


class ConfigError(RuntimeError):
    """Raised when configuration files are missing or invalid."""


@dataclass
class ConfigBundle:
    searches: SearchesFile
    scoring: ScoringConfig
    marketplaces: MarketplacesFile

    def sanitized_dump(self) -> dict[str, Any]:
        return {
            "searches": self.searches.model_dump(),
            "scoring": self.scoring.model_dump(),
            "marketplaces": self.marketplaces.model_dump(),
        }


def _load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise ConfigError(f"Missing config file: {path}")
    try:
        with path.open("r", encoding="utf-8") as handle:
            data = yaml.safe_load(handle) or {}
    except yaml.YAMLError as exc:
        raise ConfigError(f"Invalid YAML in {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise ConfigError(f"Config file must contain a mapping: {path}")
    return data


def load_config_bundle(config_dir: str | Path = "config") -> ConfigBundle:
    config_path = Path(config_dir)
    try:
        searches = SearchesFile.model_validate(_load_yaml(config_path / "searches.yaml"))
        scoring = ScoringConfig.model_validate(_load_yaml(config_path / "scoring.yaml"))
        marketplaces = MarketplacesFile.model_validate(
            _load_yaml(config_path / "marketplaces.yaml")
        )
    except ValidationError as exc:
        raise ConfigError(str(exc)) from exc

    known_marketplaces = set(marketplaces.marketplaces)
    for search in searches.searches:
        unknown = set(search.marketplaces) - known_marketplaces
        if unknown:
            names = ", ".join(sorted(unknown))
            raise ConfigError(f"Search {search.name} references unknown marketplaces: {names}")
        if search.strong_alert_threshold is not None and search.digest_threshold is not None:
            if search.strong_alert_threshold <= search.digest_threshold:
                raise ConfigError(
                    f"Search {search.name} has invalid thresholds: strong must be > digest"
                )
        if search.digest_threshold is not None:
            if search.digest_threshold <= scoring.thresholds.ignore_below:
                raise ConfigError(
                    f"Search {search.name} has invalid digest threshold: must be > ignore_below"
                )
    return ConfigBundle(searches=searches, scoring=scoring, marketplaces=marketplaces)
