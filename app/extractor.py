from __future__ import annotations

import time
from pathlib import Path

from app.pdf_parser import extract_text_from_pdf
from app.ocr import extract_text_with_ocr
from app.schema import SYSTEM_PROMPT
from app.utils.cache import make_cache_key, get_cached, set_cached


def extract_text(path: str | Path, use_ocr: bool = True) -> str:
    text = extract_text_from_pdf(path)

    if use_ocr and len(text.strip()) < 100:
        text = extract_text_with_ocr(path)

    return text


def extract_resume(
    path: str | Path,
    model: str = "gpt",
    cache: bool = False,
    use_ocr: bool = True
) -> dict:
    text = extract_text(path, use_ocr=use_ocr)

    key = make_cache_key(model, text, SYSTEM_PROMPT)

    if cache:
        cached = get_cached(key)
        if cached:
            cached["metadata"]["cache_hit"] = True
            return cached

    start = time.perf_counter()

    if model == "gpt":
        from app.models.gpt_backend import extract_with_gpt
        model_result = extract_with_gpt(text)

    elif model == "claude":
        from app.models.claude_backend import extract_with_claude
        model_result = extract_with_claude(text)

    else:
        raise ValueError("model must be 'gpt' or 'claude'")

    latency_ms = round((time.perf_counter() - start) * 1000, 2)

    data = model_result.get("data", model_result)
    usage = model_result.get("usage", {})

    result = {
        "data": data,
        "metadata": {
            "model": model,
            "latency_ms": latency_ms,
            "cache_hit": False,
            "input_chars": len(text),
            "usage": usage,
        },
    }

    if cache:
        set_cached(key, result)

    return result