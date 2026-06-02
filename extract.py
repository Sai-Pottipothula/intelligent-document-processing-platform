from __future__ import annotations
import argparse
import json
from app.extractor import extract_resume


def main():
    parser = argparse.ArgumentParser(description="Extract structured JSON from a resume PDF")
    parser.add_argument("path", help="Path to resume PDF")
    parser.add_argument("--model", choices=["gpt", "claude"], default="gpt")
    parser.add_argument("--cache", action="store_true", help="Cache repeated extraction calls")
    parser.add_argument("--no-ocr", action="store_true", help="Disable OCR fallback")
    args = parser.parse_args()

    result = extract_resume(args.path, model=args.model, cache=args.cache, use_ocr=not args.no_ocr)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
