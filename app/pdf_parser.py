from __future__ import annotations
from pathlib import Path
from pypdf import PdfReader


def extract_text_from_pdf(path: str | Path) -> str:
    path = Path(path)
    reader = PdfReader(str(path))
    chunks: list[str] = []
    for page in reader.pages:
        text = page.extract_text() or ""
        chunks.append(text)
    return "\n".join(chunks).strip()
