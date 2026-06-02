from __future__ import annotations

import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from app.schema import RESUME_JSON_SCHEMA, SYSTEM_PROMPT, ResumeExtraction
from app.utils.cost import estimate_cost

load_dotenv()


def extract_with_gpt(text: str, model_name: str = "gpt-4.1-mini") -> dict:
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("OPENAI_API_KEY is missing. Add it to your .env file.")

    client = OpenAI(api_key=api_key)

    response = client.responses.create(
        model=model_name,
        input=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Extract resume data from this text:\n\n{text}"},
        ],
        text={
            "format": {
                "type": "json_schema",
                "name": "resume_extraction",
                "schema": RESUME_JSON_SCHEMA,
                "strict": True,
            }
        },
    )

    parsed = json.loads(response.output_text)
    data = ResumeExtraction.model_validate(parsed).model_dump()

    input_tokens = response.usage.input_tokens if response.usage else 0
    output_tokens = response.usage.output_tokens if response.usage else 0

    return {
        "data": data,
        "usage": {
            "provider": "openai",
            "model_name": model_name,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "estimated_cost_usd": estimate_cost("gpt", input_tokens, output_tokens),
        },
    }