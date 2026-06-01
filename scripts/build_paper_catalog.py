import argparse
import csv
from pathlib import Path


def arxiv_url(arxiv_id: str) -> str:
    aid = (arxiv_id or "").strip()
    if not aid:
        return ""
    return f"https://arxiv.org/abs/{aid}"


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a shareable paper catalog from local papers index.")
    parser.add_argument("--input", required=True, help="Input CSV: papers_index.csv")
    parser.add_argument("--output", required=True, help="Output CSV: paper_catalog.csv")
    args = parser.parse_args()

    inp = Path(args.input)
    out = Path(args.output)

    with inp.open("r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))

    fieldnames = [
        "paper_id",
        "title",
        "year",
        "arxiv_id",
        "source_url",
        "tier",
        "modality",
        "task",
        "evidence_level",
        "code_repo_url",
        "code_commit",
        "citation_key",
        "notes",
    ]

    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows:
            pid = r.get("paper_id", "")
            arxiv_id = r.get("arxiv_id", "")
            title = r.get("title_guess", "")
            year = r.get("year_guess", "")
            tier = r.get("tier", "")
            citation_key = (pid or "").replace("arxiv_", "arxiv")
            writer.writerow(
                {
                    "paper_id": pid,
                    "title": title,
                    "year": year,
                    "arxiv_id": arxiv_id,
                    "source_url": arxiv_url(arxiv_id),
                    "tier": tier,
                    "modality": "",
                    "task": "",
                    "evidence_level": "",
                    "code_repo_url": "",
                    "code_commit": "",
                    "citation_key": citation_key,
                    "notes": "",
                }
            )

    print(f"Wrote {len(rows)} rows to {out}")


if __name__ == "__main__":
    main()

