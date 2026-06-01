import argparse
import json
import re
from collections import defaultdict
from pathlib import Path


HEADER_RE = re.compile(r"^##\s+([A-Z]+\d+)\s*$", re.MULTILINE)


def parse_sections(markdown_text: str):
    matches = list(HEADER_RE.finditer(markdown_text))
    sections = {}
    for i, m in enumerate(matches):
        sid = m.group(1).strip()
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(markdown_text)
        sections[sid] = markdown_text[start:end]
    return sections


def classify_mode(prompt_id: str):
    if prompt_id.startswith("RQ"):
        return "research_qa"
    if prompt_id.startswith("RP"):
        return "reproduction_plan"
    if prompt_id.startswith("DBG"):
        return "debug_triage"
    if prompt_id.startswith("WRT"):
        return "writing_citation"
    return "unknown"


def has_evidence_block(text: str):
    return "evidence:" in text.lower()


def has_mapping_block(text: str):
    return "mapping:" in text.lower() or "claim-to-citation map:" in text.lower()


def main():
    parser = argparse.ArgumentParser(description="Check evidence and mapping coverage in markdown responses.")
    parser.add_argument("--responses", required=True, help="Markdown response file with ## ID sections")
    parser.add_argument("--output", required=True, help="Output JSON path")
    args = parser.parse_args()

    md = Path(args.responses).read_text(encoding="utf-8")
    sections = parse_sections(md)

    rows = []
    by_mode = defaultdict(list)
    for pid, body in sections.items():
        mode = classify_mode(pid)
        e = has_evidence_block(body)
        m = has_mapping_block(body)
        row = {
            "id": pid,
            "mode": mode,
            "has_evidence": int(e),
            "has_mapping": int(m),
            "has_both": int(e and m),
        }
        rows.append(row)
        by_mode[mode].append(row)

    summary = {
        "total": len(rows),
        "has_evidence_rate": sum(r["has_evidence"] for r in rows) / len(rows) if rows else 0.0,
        "has_mapping_rate": sum(r["has_mapping"] for r in rows) / len(rows) if rows else 0.0,
        "has_both_rate": sum(r["has_both"] for r in rows) / len(rows) if rows else 0.0,
        "by_mode": {},
        "rows": rows,
    }
    for mode, mrows in by_mode.items():
        n = len(mrows)
        summary["by_mode"][mode] = {
            "n": n,
            "has_evidence_rate": sum(r["has_evidence"] for r in mrows) / n if n else 0.0,
            "has_mapping_rate": sum(r["has_mapping"] for r in mrows) / n if n else 0.0,
            "has_both_rate": sum(r["has_both"] for r in mrows) / n if n else 0.0,
        }

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote coverage report: {out}")


if __name__ == "__main__":
    main()

