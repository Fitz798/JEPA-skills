import argparse
import csv
from pathlib import Path


def norm(s: str) -> str:
    return (s or "").strip().lower()


def score_row(row: dict, query_terms: list[str]) -> int:
    hay = " ".join(
        [
            norm(row.get("paper_id", "")),
            norm(row.get("title_guess", "")),
            norm(row.get("current_name", "")),
        ]
    )
    return sum(1 for t in query_terms if t and t in hay)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build ranked JEPA citation candidates from papers metadata.")
    parser.add_argument("--metadata", required=True, help="Path to papers_index.csv or paper_catalog.csv")
    parser.add_argument("--query", required=True, help="Comma-separated query terms")
    parser.add_argument("--topk", type=int, default=20, help="Maximum rows to output")
    parser.add_argument("--output", required=True, help="Output CSV path")
    args = parser.parse_args()

    meta_path = Path(args.metadata)
    out_path = Path(args.output)
    query_terms = [norm(x) for x in args.query.split(",") if norm(x)]

    with meta_path.open("r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))

    scored = []
    for row in rows:
        s = score_row(row, query_terms)
        if s > 0:
            scored.append((s, row))

    scored.sort(key=lambda x: (-x[0], x[1].get("paper_id", "")))
    top_rows = [row for _, row in scored[: args.topk]]

    fieldnames = [
        "paper_id",
        "title_guess",
        "year_guess",
        "arxiv_id",
        "tier",
        "current_name",
        "relative_path",
        "score",
        "query",
    ]
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in top_rows:
            writer.writerow(
                {
                    "paper_id": row.get("paper_id", ""),
                    "title_guess": row.get("title_guess", ""),
                    "year_guess": row.get("year_guess", ""),
                    "arxiv_id": row.get("arxiv_id", ""),
                    "tier": row.get("tier", ""),
                    "current_name": row.get("current_name", ""),
                    "relative_path": row.get("relative_path", ""),
                    "score": score_row(row, query_terms),
                    "query": args.query,
                }
            )

    print(f"Wrote {len(top_rows)} rows to {out_path}")


if __name__ == "__main__":
    main()

