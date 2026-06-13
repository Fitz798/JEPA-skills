import argparse
import csv
import json
import sys
from collections import Counter
from pathlib import Path


REQUIRED_COLUMNS = [
    "paper_id",
    "title",
    "tier",
    "modality",
    "task",
    "evidence_level",
    "code_id",
    "code_link_status",
    "link_confidence",
]

COMPLETENESS_FIELDS = [
    "modality",
    "task",
    "evidence_level",
    "code_id",
    "code_link_status",
    "link_confidence",
]

CORE_REQUIRED_FIELDS = [
    "modality",
    "task",
    "evidence_level",
    "code_link_status",
    "link_confidence",
]


def load_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        return reader.fieldnames or [], list(reader)


def is_missing(value: str | None) -> bool:
    return not (value or "").strip()


def clean(value: str | None) -> str:
    return (value or "").strip()


def summarize_field(rows: list[dict[str, str]], field: str) -> dict:
    total = len(rows)
    missing_rows = []
    for row in rows:
        if is_missing(row.get(field)):
            missing_rows.append(row.get("paper_id", "").strip())
    present = total - len(missing_rows)
    return {
        "field": field,
        "total_rows": total,
        "present_rows": present,
        "missing_rows": len(missing_rows),
        "coverage_rate": round((present / total), 4) if total else 0.0,
        "missing_paper_ids": missing_rows,
    }


def summarize_link_status(rows: list[dict[str, str]]) -> dict:
    counter = Counter()
    for row in rows:
        value = clean(row.get("code_link_status")) or "<missing>"
        counter[value] += 1
    return dict(sorted(counter.items()))


def summarize_core_linkage(rows: list[dict[str, str]]) -> dict:
    status_counter = Counter()
    linked_code_ids = 0
    for row in rows:
        status_counter[clean(row.get("code_link_status")) or "<missing>"] += 1
        if not is_missing(row.get("code_id")):
            linked_code_ids += 1
    total = len(rows)
    return {
        "total_core_rows": total,
        "rows_with_code_id": linked_code_ids,
        "code_id_coverage_rate": round((linked_code_ids / total), 4) if total else 0.0,
        "status_counts": dict(sorted(status_counter.items())),
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check metadata/paper_catalog.csv completeness for release gating."
    )
    parser.add_argument(
        "--input",
        default="metadata/paper_catalog.csv",
        help="Catalog CSV to analyze",
    )
    parser.add_argument(
        "--json",
        help="Optional JSON output path for the completeness report",
    )
    args = parser.parse_args()

    repo_root = Path.cwd()
    input_path = repo_root / args.input
    if not input_path.exists():
        print(f"Missing input file: {input_path}", file=sys.stderr)
        return 1

    fieldnames, rows = load_rows(input_path)
    missing_columns = [col for col in REQUIRED_COLUMNS if col not in fieldnames]
    if missing_columns:
        for col in missing_columns:
            print(f"Missing required column: {col}", file=sys.stderr)
        return 1

    core_rows = [row for row in rows if row.get("tier", "").strip() == "core"]

    overall = {field: summarize_field(rows, field) for field in COMPLETENESS_FIELDS}
    core = {field: summarize_field(core_rows, field) for field in COMPLETENESS_FIELDS}

    core_gate_failures = {
        field: core[field]["missing_paper_ids"]
        for field in CORE_REQUIRED_FIELDS
        if core[field]["missing_rows"] > 0
    }

    report = {
        "input": str(input_path),
        "row_count": len(rows),
        "core_row_count": len(core_rows),
        "overall": overall,
        "core": core,
        "overall_code_link_status_counts": summarize_link_status(rows),
        "core_code_linkage": summarize_core_linkage(core_rows),
        "core_gate_ok": not core_gate_failures,
        "core_gate_failures": core_gate_failures,
    }

    if args.json:
        out_path = repo_root / args.json
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(report, indent=2, ensure_ascii=True), encoding="utf-8")

    print(f"Rows: total={len(rows)} core={len(core_rows)}")
    for field in ("modality", "task", "evidence_level", "code_link_status", "link_confidence"):
        summary = core[field]
        print(
            f"Core {field}: {summary['present_rows']}/{summary['total_rows']} "
            f"({summary['coverage_rate']:.1%})"
        )
    print(
        "Core code_id: "
        f"{core['code_id']['present_rows']}/{core['code_id']['total_rows']} "
        f"({core['code_id']['coverage_rate']:.1%})"
    )

    if core_gate_failures:
        print("Core metadata completeness gate: FAIL", file=sys.stderr)
        for field, paper_ids in core_gate_failures.items():
            print(f"- {field}: {', '.join(paper_ids)}", file=sys.stderr)
        return 1

    print("Core metadata completeness gate: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
