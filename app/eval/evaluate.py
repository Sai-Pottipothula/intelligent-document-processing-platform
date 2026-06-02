from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Any

from app.extractor import extract_resume


SAMPLES_DIR = Path("samples")
GOLD_DIR = Path("app/eval/gold_data")
REPORTS_DIR = Path("reports")


FIELDS_TO_SCORE = [
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
]


def normalize(value: Any) -> Any:
    if isinstance(value, str):
        return value.strip().lower()
    if isinstance(value, list):
        return [normalize(v) for v in value]
    if isinstance(value, dict):
        return {k: normalize(v) for k, v in value.items()}
    return value


def list_recall_score(predicted: list, gold: list) -> float:
    if not gold:
        return 1.0 if not predicted else 0.0

    predicted_set = set(json.dumps(normalize(item), sort_keys=True) for item in predicted)
    gold_set = set(json.dumps(normalize(item), sort_keys=True) for item in gold)

    matched = len(predicted_set.intersection(gold_set))
    return matched / len(gold_set)


def employment_score(predicted: list, gold: list) -> float:
    if not gold:
        return 1.0 if not predicted else 0.0

    matched = 0

    for gold_job in gold:
        gold_company = normalize(gold_job.get("company"))
        gold_title = normalize(gold_job.get("title"))

        for pred_job in predicted:
            pred_company = normalize(pred_job.get("company"))
            pred_title = normalize(pred_job.get("title"))

            if gold_company == pred_company and gold_title == pred_title:
                matched += 1
                break

    return matched / len(gold)


def education_score(predicted: list, gold: list) -> float:
    if not gold:
        return 1.0 if not predicted else 0.0

    matched = 0

    for gold_edu in gold:
        gold_institution = normalize(gold_edu.get("institution"))
        gold_degree = normalize(gold_edu.get("degree"))

        for pred_edu in predicted:
            pred_institution = normalize(pred_edu.get("institution"))
            pred_degree = normalize(pred_edu.get("degree"))

            if gold_institution == pred_institution and gold_degree == pred_degree:
                matched += 1
                break

    return matched / len(gold)


def field_score(field: str, predicted: Any, gold: Any) -> float:
    predicted_norm = normalize(predicted)
    gold_norm = normalize(gold)

    if field == "skills":
        return list_recall_score(predicted_norm or [], gold_norm or [])

    if field == "certifications":
        return list_recall_score(predicted_norm or [], gold_norm or [])

    if field == "emails":
        return list_recall_score(predicted_norm or [], gold_norm or [])

    if field == "phones":
        return list_recall_score(predicted_norm or [], gold_norm or [])

    if field == "employment":
        return employment_score(predicted_norm or [], gold_norm or [])

    if field == "education":
        return education_score(predicted_norm or [], gold_norm or [])

    return 1.0 if predicted_norm == gold_norm else 0.0


def evaluate_resume(pdf_path: Path, gold_path: Path, model: str) -> dict:
    with gold_path.open("r", encoding="utf-8") as f:
        gold = json.load(f)

    start = time.time()
    result = extract_resume(str(pdf_path), model=model)
    latency = round(time.time() - start, 2)

    predicted = result.get("data", result)

    field_scores = {}

    for field in FIELDS_TO_SCORE:
        score = field_score(
            field,
            predicted.get(field),
            gold.get(field)
        )
        field_scores[field] = round(score, 4)

    accuracy = round(
        sum(field_scores.values()) / len(FIELDS_TO_SCORE),
        4
    )

    return {
        "file": pdf_path.name,
        "model": model,
        "accuracy": accuracy,
        "latency_seconds": latency,
        "field_scores": field_scores,
        "predicted": predicted,
        "gold": gold,
    }


def generate_markdown_report(results: list[dict], model: str) -> str:
    total_accuracy = sum(r["accuracy"] for r in results) / len(results)
    avg_latency = sum(r["latency_seconds"] for r in results) / len(results)

    field_totals = {field: 0.0 for field in FIELDS_TO_SCORE}

    for result in results:
        for field, score in result["field_scores"].items():
            field_totals[field] += score

    lines = []
    lines.append(f"# Resume Extraction Evaluation Report - {model.upper()}")
    lines.append("")
    lines.append(f"Total resumes evaluated: {len(results)}")
    lines.append(f"Overall accuracy: {round(total_accuracy * 100, 2)}%")
    lines.append(f"Average latency: {round(avg_latency, 2)} seconds")
    lines.append("")
    lines.append("## Per-field Accuracy")
    lines.append("")
    lines.append("| Field | Accuracy |")
    lines.append("|---|---:|")

    for field in FIELDS_TO_SCORE:
        field_accuracy = field_totals[field] / len(results)
        lines.append(f"| {field} | {round(field_accuracy * 100, 2)}% |")

    lines.append("")
    lines.append("## Per-resume Results")
    lines.append("")
    lines.append("| Resume | Accuracy | Latency |")
    lines.append("|---|---:|---:|")

    for result in results:
        lines.append(
            f"| {result['file']} | {round(result['accuracy'] * 100, 2)}% | {result['latency_seconds']}s |"
        )

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", choices=["gpt", "claude"], default="gpt")
    args = parser.parse_args()

    REPORTS_DIR.mkdir(exist_ok=True)

    results = []

    for pdf_path in sorted(SAMPLES_DIR.glob("*.pdf")):
        gold_path = GOLD_DIR / f"{pdf_path.stem}.json"

        if not gold_path.exists():
            print(f"Skipping {pdf_path.name}: missing gold file {gold_path}")
            continue

        print(f"Evaluating {pdf_path.name} with {args.model}...")
        result = evaluate_resume(pdf_path, gold_path, args.model)
        results.append(result)

    if not results:
        print("No resumes evaluated. Add PDFs in samples/ and matching JSON files in app/eval/gold_data/.")
        return

    report = generate_markdown_report(results, args.model)

    report_path = REPORTS_DIR / f"eval_report_{args.model}.md"
    report_path.write_text(report, encoding="utf-8")

    raw_path = REPORTS_DIR / f"eval_results_{args.model}.json"
    raw_path.write_text(json.dumps(results, indent=2), encoding="utf-8")

    print(f"\nReport saved to: {report_path}")
    print(f"Raw results saved to: {raw_path}")


if __name__ == "__main__":
    main()