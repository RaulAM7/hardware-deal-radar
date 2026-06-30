from __future__ import annotations

from pathlib import Path
from typing import Any

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


def _mask_secret(value: SecretStr | None) -> str:
    return "<set>" if value and value.get_secret_value() else "<empty>"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    EBAY_ENV: str = "production"
    EBAY_CLIENT_ID: SecretStr | None = None
    EBAY_CLIENT_SECRET: SecretStr | None = None
    EBAY_SCOPE: str = "https://api.ebay.com/oauth/api_scope"
    EBAY_MARKETPLACE_DEFAULT: str = "EBAY_ES"

    TELEGRAM_BOT_TOKEN: SecretStr | None = None
    TELEGRAM_CHAT_ID: SecretStr | None = None

    SMTP_HOST: str | None = None
    SMTP_PORT: int = 587
    SMTP_USERNAME: str | None = None
    SMTP_PASSWORD: SecretStr | None = None
    SMTP_FROM: str | None = None
    DIGEST_EMAIL_TO: str | None = None

    RADAR_ENV: str = "production"
    RADAR_DB_PATH: str = "./data/radar.sqlite"
    RADAR_LOG_LEVEL: str = "INFO"

    def db_path(self) -> Path:
        return Path(self.RADAR_DB_PATH).expanduser().resolve()

    def masked_dict(self) -> dict[str, Any]:
        data = self.model_dump()
        for key in (
            "EBAY_CLIENT_ID",
            "EBAY_CLIENT_SECRET",
            "TELEGRAM_BOT_TOKEN",
            "TELEGRAM_CHAT_ID",
            "SMTP_PASSWORD",
        ):
            data[key] = _mask_secret(getattr(self, key))
        return data

    def credential_status(self) -> dict[str, str]:
        return {
            "EBAY_CLIENT_ID": _mask_secret(self.EBAY_CLIENT_ID),
            "EBAY_CLIENT_SECRET": _mask_secret(self.EBAY_CLIENT_SECRET),
            "TELEGRAM_BOT_TOKEN": _mask_secret(self.TELEGRAM_BOT_TOKEN),
            "TELEGRAM_CHAT_ID": _mask_secret(self.TELEGRAM_CHAT_ID),
            "SMTP_HOST": "<set>" if self.SMTP_HOST else "<empty>",
            "SMTP_USERNAME": "<set>" if self.SMTP_USERNAME else "<empty>",
            "SMTP_PASSWORD": _mask_secret(self.SMTP_PASSWORD),
            "SMTP_FROM": "<set>" if self.SMTP_FROM else "<empty>",
            "DIGEST_EMAIL_TO": "<set>" if self.DIGEST_EMAIL_TO else "<empty>",
        }


def load_settings() -> Settings:
    return Settings()
