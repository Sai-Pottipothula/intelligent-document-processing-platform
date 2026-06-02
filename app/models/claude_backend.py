from __future__ import annotations

import json
import os

from anthropic import Anthropic
from dotenv import load_dotenv

from app.schema import ResumeExtraction
from app.utils.cost import estimate_cost

load_dotenv()


def extract_with_claude(
    text: str,
    model_name: str = "claude-sonnet-4-6"
) -> dict:
    api_key = os.getenv("ANTHROPIC_API_KEY")

    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY is missing. Add it to your .env file.")

    client = Anthropic(api_key=api_key)

    prompt = f"""
Extract resume information and return ONLY valid JSON.

Required JSON structure:
{{
  "name": null,
  "emails": [],
  "phones": [],
  "total_years_experience": null,
  "education": [
    {{
      "institution": null,
      "degree": null,
      "year": null
    }}
  ],
  "employment": [
    {{
      "company": null,
      "title": null,
      "start": null,
      "end": null,
      "summary": null
    }}
  ],
  "skills": [],
  "certifications": [],
  "location": null,
  "linkedin": null,
  "github": null,
  "portfolio": null,
  "confidence_score": 0.0,
  "missing_fields": []
}}

Rules:
- Return JSON only.
- Do not include markdown.
- Do not include explanations.
- Extract only information explicitly present in the resume.
- Use null for missing scalar values.
- Use [] for missing arrays.

Resume text:
{text}
"""

    response = client.messages.create(
        model=model_name,
        max_tokens=4000,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    content = response.content[0].text
    parsed = json.loads(content)
    data = ResumeExtraction.model_validate(parsed).model_dump()

    input_tokens = response.usage.input_tokens if response.usage else 0
    output_tokens = response.usage.output_tokens if response.usage else 0

    return {
        "data": data,
        "usage": {
            "provider": "anthropic",
            "model_name": model_name,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "estimated_cost_usd": estimate_cost("claude", input_tokens, output_tokens),
        },
    }