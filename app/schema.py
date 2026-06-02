from __future__ import annotations

RESUME_JSON_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "name": {"type": ["string", "null"]},
        "emails": {"type": "array", "items": {"type": "string"}},
        "phones": {"type": "array", "items": {"type": "string"}},
        "total_years_experience": {"type": ["number", "null"]},
        "education": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "institution": {"type": ["string", "null"]},
                    "degree": {"type": ["string", "null"]},
                    "year": {"type": ["string", "null"]}
                },
                "required": ["institution", "degree", "year"]
            }
        },
        "employment": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "company": {"type": ["string", "null"]},
                    "title": {"type": ["string", "null"]},
                    "start": {"type": ["string", "null"]},
                    "end": {"type": ["string", "null"]},
                    "summary": {"type": ["string", "null"]}
                },
                "required": ["company", "title", "start", "end", "summary"]
            }
        },
        "skills": {"type": "array", "items": {"type": "string"}},
        "certifications": {"type": "array", "items": {"type": "string"}},
        "location": {"type": ["string", "null"]},
        "linkedin": {"type": ["string", "null"]},
        "github": {"type": ["string", "null"]},
        "portfolio": {"type": ["string", "null"]},
        "confidence_score": {"type": "number"},
        "missing_fields": {"type": "array", "items": {"type": "string"}}
    },
    "required": [
        "name",
        "emails",
        "phones",
        "total_years_experience",
        "education",
        "employment",
        "skills",
        "certifications",
        "location",
        "linkedin",
        "github",
        "portfolio",
        "confidence_score",
        "missing_fields"
    ]
}


from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict


class Education(BaseModel):
    model_config = ConfigDict(extra="forbid")

    institution: Optional[str] = None
    degree: Optional[str] = None
    year: Optional[str] = None


class Employment(BaseModel):
    model_config = ConfigDict(extra="forbid")

    company: Optional[str] = None
    title: Optional[str] = None
    start: Optional[str] = None
    end: Optional[str] = None
    summary: Optional[str] = None


class ResumeExtraction(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: Optional[str] = None
    emails: List[str] = Field(default_factory=list)
    phones: List[str] = Field(default_factory=list)
    total_years_experience: Optional[float] = None
    education: List[Education] = Field(default_factory=list)
    employment: List[Employment] = Field(default_factory=list)
    skills: List[str] = Field(default_factory=list)
    certifications: List[str] = Field(default_factory=list)
    location: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    portfolio: Optional[str] = None
    confidence_score: float = Field(default=0.0, ge=0.0, le=1.0)
    missing_fields: List[str] = Field(default_factory=list)


SYSTEM_PROMPT = """
You are a precise resume information extraction engine.

Extract only information explicitly present in the resume text.

Rules:
- Do not hallucinate.
- Use null for missing scalar values.
- Use [] for missing arrays.
- Return data that matches the provided schema exactly.
- All required fields must be present.
- Estimate total_years_experience only when dates or explicit years make it reasonable.
- confidence_score should reflect overall extraction confidence from 0.0 to 1.0.
- missing_fields should list important fields that were not found.
"""