from __future__ import annotations

import shutil
from pathlib import Path

import pytest
from typer.testing import CliRunner

REPO_ROOT = Path(__file__).resolve().parents[1]
SECRET_ENV_VARS = [
    "EBAY_CLIENT_ID",
    "EBAY_CLIENT_SECRET",
    "TELEGRAM_BOT_TOKEN",
    "TELEGRAM_CHAT_ID",
    "SMTP_HOST",
    "SMTP_USERNAME",
    "SMTP_PASSWORD",
    "SMTP_FROM",
    "DIGEST_EMAIL_TO",
]


@pytest.fixture()
def runner() -> CliRunner:
    return CliRunner()


@pytest.fixture()
def isolated_project(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    for source in (REPO_ROOT / "config").glob("*.yaml"):
        shutil.copy2(source, config_dir / source.name)
    (tmp_path / "data").mkdir()
    for key in SECRET_ENV_VARS:
        monkeypatch.delenv(key, raising=False)
    monkeypatch.chdir(tmp_path)
    return tmp_path
