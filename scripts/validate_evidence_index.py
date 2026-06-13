import argparse
import csv
import json
import sys
from pathlib import Path


REQUIRED_COLUMNS = [
    "evidence_id",
    "evidence_type",
    "paper_id",
    "arxiv_id",
    "code_id",
    "artifact_path",
    "locator",
    "claim_summary",
    "claim_scope",
    "confidence",
    "status",
    "notes",
]

ALLOWED_EVIDENCE_TYPES = {"paper", "code", "protocol", "log", "table", "figure", "note"}
ALLOWED_CLAIM_SCOPES = {"fact", "method", "result", "recommendation", "failure_mode", "procedure"}
ALLOWED_CONFIDENCE = {"high", "medium", "low"}
ALLOWED_STATUS = {"verified", "provisional", "missing_locator", "needs_review"}
PAPER_BACKED_TYPES = {"paper", "table", "figure"}


def load_index_values(path: Path, key: str) -> set[str]:
    if not path.exists():
        return set()
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return {row.get(key, "").strip() for row in csv.DictReader(f) if row.get(key, "").strip()}


def validate_rows(rows: list[dict], known_papers: set[str], known_codes: set[str], check_paths: bool, repo_root: Path) -> list[dict]:
    errors: list[dict] = []
    seen_ids: set[str] = set()

    for idx, row in enumerate(rows, start=2):
        row_id = row.get("evidence_id", "").strip()

        def add_error(message: str, field: str | None = None) -> None:
            errors.append({"line": idx, "evidence_id": row_id, "field": field or "", "message": message})

        for col in REQUIRED_COLUMNS:
            if col not in row:
                add_error(f"Missing column in parsed row: {col}", col)

        for field in ("evidence_id", "evidence_type", "locator", "claim_summary", "claim_scope", "confidence", "status"):
            if not row.get(field, "").strip():
                add_error("Required field is empty", field)

        if row_id:
            if row_id in seen_ids:
                add_error("Duplicate evidence_id", "evidence_id")
            seen_ids.add(row_id)

        evidence_type = row.get("evidence_type", "").strip()
        if evidence_type and evidence_type not in ALLOWED_EVIDENCE_TYPES:
            add_error(f"Invalid evidence_type: {evidence_type}", "evidence_type")

        claim_scope = row.get("claim_scope", "").strip()
        if claim_scope and claim_scope not in ALLOWED_CLAIM_SCOPES:
            add_error(f"Invalid claim_scope: {claim_scope}", "claim_scope")

        confidence = row.get("confidence", "").strip()
        if confidence and confidence not in ALLOWED_CONFIDENCE:
            add_error(f"Invalid confidence: {confidence}", "confidence")

        status = row.get("status", "").strip()
        if status and status not in ALLOWED_STATUS:
            add_error(f"Invalid status: {status}", "status")

        paper_id = row.get("paper_id", "").strip()
        code_id = row.get("code_id", "").strip()
        artifact_path = row.get("artifact_path", "").strip()
        locator = row.get("locator", "").strip()

        if not any((paper_id, code_id, artifact_path)):
            add_error("At least one anchor is required: paper_id, code_id, or artifact_path", "artifact_path")

        if evidence_type in PAPER_BACKED_TYPES and not paper_id:
            add_error("paper-backed evidence requires paper_id", "paper_id")

        if evidence_type == "code" and not code_id:
            add_error("code evidence requires code_id", "code_id")

        if evidence_type in {"protocol", "log", "note"} and not artifact_path:
            add_error(f"{evidence_type} evidence requires artifact_path", "artifact_path")

        if status != "missing_locator" and locator == "page:?":
            add_error("Placeholder locator is not allowed outside missing_locator status", "locator")

        if paper_id and known_papers and paper_id not in known_papers:
            add_error(f"Unknown paper_id: {paper_id}", "paper_id")

        if code_id and known_codes and code_id not in known_codes:
            add_error(f"Unknown code_id: {code_id}", "code_id")

        if check_paths and artifact_path:
            full_path = repo_root / artifact_path
            if not full_path.exists():
                add_error(f"artifact_path does not exist locally: {artifact_path}", "artifact_path")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate metadata/evidence_index.csv against the project schema.")
    parser.add_argument("--input", default="metadata/evidence_index.csv", help="Evidence CSV to validate")
    parser.add_argument("--papers", default="metadata/papers_index.csv", help="Paper index CSV for paper_id validation")
    parser.add_argument("--codes", default="metadata/code_index.csv", help="Code index CSV for code_id validation")
    parser.add_argument("--json", help="Optional JSON output path for validation results")
    parser.add_argument("--check-paths", action="store_true", help="Check that artifact_path exists in the local workspace")
    args = parser.parse_args()

    repo_root = Path.cwd()
    input_path = repo_root / args.input
    if not input_path.exists():
        print(f"Missing input file: {input_path}", file=sys.stderr)
        return 1

    with input_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames or []
        rows = list(reader)

    errors: list[dict] = []
    missing_columns = [col for col in REQUIRED_COLUMNS if col not in fieldnames]
    extra_columns = [col for col in fieldnames if col not in REQUIRED_COLUMNS]
    for col in missing_columns:
        errors.append({"line": 1, "evidence_id": "", "field": col, "message": "Missing required column"})
    for col in extra_columns:
        errors.append({"line": 1, "evidence_id": "", "field": col, "message": "Unexpected extra column"})

    known_papers = load_index_values(repo_root / args.papers, "paper_id")
    known_codes = load_index_values(repo_root / args.codes, "code_id")
    errors.extend(validate_rows(rows, known_papers, known_codes, args.check_paths, repo_root))

    result = {
        "input": str(input_path),
        "row_count": len(rows),
        "error_count": len(errors),
        "ok": not errors,
        "errors": errors,
    }

    if args.json:
        out_path = repo_root / args.json
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(result, indent=2, ensure_ascii=True), encoding="utf-8")

    if errors:
        for err in errors:
            prefix = f"line {err['line']}"
            if err["evidence_id"]:
                prefix += f" [{err['evidence_id']}]"
            if err["field"]:
                prefix += f" {err['field']}"
            print(f"{prefix}: {err['message']}", file=sys.stderr)
        return 1

    print(f"Validated {len(rows)} evidence rows with no errors.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
