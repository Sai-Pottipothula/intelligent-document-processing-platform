from __future__ import annotations

PRICE_PER_1M = {
    "gpt": {"input": 0.15, "output": 0.60},
    "claude": {"input": 3.00, "output": 15.00},
}


def estimate_cost(model: str, input_tokens: int, output_tokens: int) -> float:
    pricing = PRICE_PER_1M.get(model, PRICE_PER_1M["gpt"])

    cost = (
        (input_tokens / 1_000_000 * pricing["input"])
        + (output_tokens / 1_000_000 * pricing["output"])
    )

    return round(cost, 8)