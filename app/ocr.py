from __future__ import annotations
from pathlib import Path


def extract_text_with_ocr(path: str | Path) -> str:
    """OCR fallback for scanned PDFs. Requires poppler + tesseract installed locally."""
    try:
        from pdf2image import convert_from_path
        import pytesseract
    except ImportError as exc:
        raise RuntimeError(
            "OCR dependencies missing. Install pdf2image and pytesseract, plus system packages poppler and tesseract."
        ) from exc

    pages = convert_from_path(str(path))
    text_parts = [pytesseract.image_to_string(page) for page in pages]
    return "\n".join(text_parts).strip()
