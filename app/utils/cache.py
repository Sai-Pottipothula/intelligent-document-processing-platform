from __future__ import annotations
import hashlib
import json
from pathlib import Path
from typing import Any

CACHE_DIR = Path(".cache")
CACHE_DIR.mkdir(exist_ok=True)


def make_cache_key(model: str, text: str, system_prompt: str) -> str:
    payload = {"model": model, "text": text, "system_prompt": system_prompt}
    raw = json.dumps(payload, sort_keys=True).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def get_cached(key: str) -> dict[str, Any] | None:
    file = CACHE_DIR / f"{key}.json"
    if file.exists():
        return json.loads(file.read_text())
    return None


def set_cached(key: str, value: dict[str, Any]) -> None:
    file = CACHE_DIR / f"{key}.json"
    file.write_text(json.dumps(value, indent=2))
