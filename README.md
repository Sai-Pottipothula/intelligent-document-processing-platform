# Intelligent Document Processing (IDP) Platform

AI-powered document intelligence platform that transforms unstructured PDF documents into validated structured JSON using GPT-4.1 or Claude. The platform supports OCR for scanned PDFs, schema-constrained extraction, evaluation benchmarking, caching, cost tracking, and cloud deployment.

## Live Demo

API Documentation:

https://pbsn99--intelligent-document-processing-platform-fastapi-app.modal.run/docs

Deployment: Modal

---

## Problem Statement

Organizations receive large volumes of unstructured documents such as resumes, invoices, insurance policies, contracts, and support tickets. Manually extracting information from these documents is time-consuming, error-prone, and difficult to scale.

This platform automates document understanding by converting PDFs into structured JSON that can be directly stored in databases, analytics platforms, or downstream business workflows.

---

## Key Features

* Multi-model extraction using GPT-4.1 and Claude
* OCR support for scanned PDFs using Tesseract
* Schema-constrained structured outputs
* Pydantic validation layer
* FastAPI REST API
* Streamlit drag-and-drop web interface
* CLI support for batch processing
* Response caching to reduce latency and cost
* Cost tracking per extraction
* Accuracy and latency benchmarking framework
* Dockerized deployment
* Cloud-hosted on Modal

---

## Architecture

```text
PDF Upload
    │
    ▼
PDF Parser (PyPDF)
    │
    ├── OCR Fallback (Tesseract)
    │
    ▼
Document Text
    │
    ├── GPT-4.1 Mini
    └── Claude
    │
    ▼
Structured Extraction
    │
    ├── Pydantic Validation
    ├── Cache Layer
    ├── Cost Tracking
    └── Evaluation Harness
    │
    ▼
FastAPI API / Streamlit UI
    │
    ▼
Docker + Modal Deployment
```

---

## Tech Stack

### AI & LLMs

* OpenAI GPT-4.1 Mini
* Anthropic Claude
* Structured Outputs
* Prompt Engineering

### Backend

* Python
* FastAPI
* Pydantic

### Document Processing

* PyPDF
* Tesseract OCR

### Evaluation

* Accuracy Benchmarking
* Latency Tracking
* Cost Analysis

### Frontend

* Streamlit

### Deployment

* Docker
* Modal

---

## Supported Extraction Schema

The platform currently extracts:

* Name
* Emails
* Phone Numbers
* Total Years of Experience
* Education History
* Employment History
* Skills
* Certifications
* Location
* LinkedIn Profile
* GitHub Profile
* Portfolio URL
* Confidence Score
* Missing Fields

---

## Sample Output

```json
{
  "name": "John Doe",
  "emails": ["john@example.com"],
  "phones": ["+1-555-123-4567"],
  "skills": ["Python", "AWS", "FastAPI"],
  "confidence_score": 0.96
}
```

---

## Running Locally

### Installation

```bash
git clone <repository-url>
cd intelligent-document-processing-platform

python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
```

Configure:

```bash
OPENAI_API_KEY=your_key
ANTHROPIC_API_KEY=your_key
```

---

### CLI

```bash
python extract.py samples/resume1.pdf --model gpt --cache

python extract.py samples/resume1.pdf --model claude --cache
```

---

### FastAPI

```bash
uvicorn app.main:app --reload
```

Open:

```text
http://localhost:8000/docs
```

---

### Streamlit UI

```bash
streamlit run ui/streamlit_app.py
```

---

### Docker

```bash
docker build -t idp-platform .

docker run -p 8000:8000 --env-file .env idp-platform
```

---

## Evaluation Framework

The platform includes an evaluation harness for comparing extraction quality across models.

Metrics:

* Per-field accuracy
* Overall extraction accuracy
* Latency per document
* Estimated API cost
* OCR performance

Example benchmark:

| Model        | Accuracy | Avg Latency |
| ------------ | -------- | ----------- |
| GPT-4.1 Mini | 78.4%    | 8.66s       |
| Claude       | 66.7%    | 8.20s       |

---

## Future Roadmap

* Invoice extraction
* Insurance policy extraction
* Contract intelligence
* Batch document processing
* Human review workflows
* Multi-tenant architecture
* Vector search integration
* Enterprise audit logging

---

## Project Highlights

* Designed a reusable Intelligent Document Processing architecture rather than a single-purpose resume parser
* Implemented multi-model extraction using GPT and Claude
* Added OCR support for scanned PDFs
* Built an evaluation framework for accuracy, latency, and cost analysis
* Deployed the platform publicly using Docker and Modal
* Designed the system to support future document types with minimal architectural changes
