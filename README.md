# Intelligent Document Processing (IDP) Platform

An AI-powered document intelligence platform that transforms unstructured PDF documents into validated structured JSON using either GPT or Claude.

The platform currently supports resume extraction and is designed to extend to invoices, insurance policies, contracts, support tickets, and other enterprise documents.

## Features

- Resume PDF ingestion
- OCR fallback for scanned PDFs
- Strict Pydantic schema validation
- GPT backend selectable by flag
- Claude backend selectable by flag
- CLI: `extract.py path/to/resume.pdf --model gpt`
- FastAPI endpoint: `POST /extract`
- Streamlit drag-and-drop UI
- Evaluation script for per-field accuracy
- Dockerized deployment
- Local response caching to reduce cost and latency
- Cost tracking per extraction

## Architecture

```text
Resume PDF
   ↓
PDF text extraction
   ↓
OCR fallback if scanned
   ↓
GPT or Claude backend
   ↓
Structured schema validation
   ↓
JSON response + confidence score
   ↓
CLI / FastAPI / Streamlit UI
   ↓
Evaluation report
```

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Add keys to `.env` or export them:

```bash
export OPENAI_API_KEY="your_key"
export ANTHROPIC_API_KEY="your_key"
```

## Run CLI

```bash
python extract.py samples/resume1.pdf --model gpt --cache
python extract.py samples/resume1.pdf --model claude --cache
```

## Run API

```bash
uvicorn app.main:app --reload
```

Test upload:

```bash
curl -X POST "http://localhost:8000/extract" \
  -F "file=@samples/resume1.pdf" \
  -F "model=gpt" \
  -F "cache=true"
```

## Run UI

```bash
streamlit run ui/streamlit_app.py
```

## Run evaluation

Add PDFs to:

```text
samples/
```

Add matching gold JSON files to:

```text
app/eval/gold_data/
```

Example:

```text
samples/resume1.pdf
app/eval/gold_data/resume1.json
```

Run:

```bash
python -m app.eval.evaluate --model gpt --output reports/gpt_eval_report.md
python -m app.eval.evaluate --model claude --output reports/claude_eval_report.md
```

## Docker

```bash
docker build -t resume-extraction-service .
docker run -p 8000:8000 --env-file .env resume-extraction-service
```

## JSON schema fields

- name
- emails
- phones
- total_years_experience
- education
- employment
- skills
- certifications
- location
- linkedin
- github
- portfolio
- confidence_score
- missing_fields

## Evaluation rubric alignment

| Requirement | Implemented |
|---|---|
| JSON schema with 12+ fields | Yes |
| GPT and Claude backends | Yes |
| Selectable model flag | Yes |
| CLI | Yes |
| FastAPI endpoint | Yes |
| Docker | Yes |
| OCR stretch goal | Yes |
| Confidence score stretch goal | Yes |
| Streamlit UI stretch goal | Yes |
| Markdown eval report | Yes |

## Notes

Before publishing benchmark numbers, update pricing in `app/utils/cost.py` using current provider pricing.
