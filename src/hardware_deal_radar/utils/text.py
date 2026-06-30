from __future__ import annotations

import re
from urllib.parse import urlsplit, urlunsplit

MODEL_PATTERN = re.compile(r"\b(P14s|T14|T16|P1|X1 Extreme)\b", re.IGNORECASE)
GEN_PATTERN = re.compile(r"\bGen(?:eration)?\s*(\d+)\b", re.IGNORECASE)
RAM_PATTERN = re.compile(r"\b(32|64|128)\s*GB\b", re.IGNORECASE)
SSD_TB_PATTERN = re.compile(r"\b(1|2)\s*TB\b", re.IGNORECASE)
SSD_GB_PATTERN = re.compile(r"\b(256|512)\s*GB\b", re.IGNORECASE)
CPU_PATTERN = re.compile(
    r"(Ryzen\s+\d+\s+PRO\s+[A-Z0-9-]+|Intel\s+(?:Core\s+)?i[579][-\s]?[A-Z0-9-]+|i[579]-\d{4,5}[A-Z]*)",
    re.IGNORECASE,
)


def normalize_whitespace(value: str) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def canonicalize_url(url: str | None) -> str | None:
    if not url:
        return None
    split = urlsplit(url)
    return urlunsplit((split.scheme, split.netloc, split.path, "", ""))


def extract_model_family(text: str) -> str | None:
    match = MODEL_PATTERN.search(text)
    return match.group(1) if match else None


def extract_model_generation(text: str) -> str | None:
    match = GEN_PATTERN.search(text)
    return match.group(1) if match else None


def extract_ram_gb(text: str) -> int | None:
    match = RAM_PATTERN.search(text)
    return int(match.group(1)) if match else None


def extract_ssd_gb(text: str) -> int | None:
    tb = SSD_TB_PATTERN.search(text)
    if tb:
        return int(tb.group(1)) * 1024
    gb = SSD_GB_PATTERN.search(text)
    return int(gb.group(1)) if gb else None


def extract_cpu_text(text: str) -> str | None:
    match = CPU_PATTERN.search(text)
    return normalize_whitespace(match.group(1)) if match else None


def detect_keyboard_layout(text: str) -> str | None:
    lowered = text.lower()
    if (
        "spanish keyboard" in lowered
        or "teclado espanol" in lowered
        or "teclado español" in lowered
    ):
        return "ES"
    if "uk keyboard" in lowered or "english keyboard" in lowered:
        return "UK"
    if "german keyboard" in lowered or "teclado aleman" in lowered:
        return "DE"
    if "italian keyboard" in lowered or "teclado italiano" in lowered:
        return "IT"
    return None


def find_keywords(text: str, keywords: list[str]) -> list[str]:
    lowered = text.lower()
    return [keyword for keyword in keywords if keyword.lower() in lowered]


def normalized_title(text: str) -> str:
    cleaned = normalize_whitespace(text).lower()
    return re.sub(r"[^a-z0-9]+", " ", cleaned).strip()
