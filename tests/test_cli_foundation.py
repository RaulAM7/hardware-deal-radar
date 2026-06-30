from __future__ import annotations

from hardware_deal_radar import __version__
from hardware_deal_radar.cli import app
from hardware_deal_radar.settings import load_settings


def test_package_import() -> None:
    assert __version__ == "0.1.0"


def test_cli_help(runner) -> None:
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "run-once" in result.output
    assert "validate-config" in result.output


def test_settings_mask_secrets(monkeypatch, isolated_project) -> None:
    monkeypatch.setenv("EBAY_CLIENT_ID", "client-id")
    monkeypatch.setenv("EBAY_CLIENT_SECRET", "client-secret")
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "bot-token")
    settings = load_settings()
    masked = settings.masked_dict()
    assert masked["EBAY_CLIENT_ID"] == "<set>"
    assert masked["EBAY_CLIENT_SECRET"] == "<set>"
    assert masked["TELEGRAM_BOT_TOKEN"] == "<set>"
