import argparse
import csv
from pathlib import Path


def norm(s: str) -> str:
    return (s or "").strip().lower()


def first_present(row: dict, *keys: str) -> str:
    for key in keys:
        value = row.get(key, "")
        if value:
            return value
    return ""


def split_query_terms(query: str) -> list[str]:
    raw_terms = [norm(x) for x in query.split(",") if norm(x)]
    terms: list[str] = []
    expansions = {
        "multimodal": ["cross-modal", "vision-language", "audio", "speech", "clinical"],
        "vision-language": ["vl", "multimodal", "vision language"],
        "audio": ["speech", "waveform"],
        "transfer": ["adaptation", "downstream", "representation"],
        "linear probe": ["linear", "probe", "downstream", "evaluation"],
        "masking": ["mask", "context", "contextual"],
        "context": ["masking", "in-context"],
        "auxiliary": ["auxiliary objectives", "ablation"],
        "normalization": ["feature normalization", "stability"],
    }
    for term in raw_terms:
        terms.append(term)
        terms.extend(expansions.get(term, []))
        parts = [p for p in term.replace("/", " ").replace("-", " ").split() if len(p) >= 2]
        if len(parts) > 1:
            terms.extend(parts)
    return list(dict.fromkeys(terms))


def classify_term(term: str) -> str:
    if term in {"multimodal", "vision-language", "vision language", "cross-modal", "clinical"}:
        return "multimodal"
    if term in {"ijepa", "i-jepa"}:
        return "image"
    if term in {"vjepa", "v-jepa", "video"}:
        return "video"
    if term in {"audio", "audio-jepa", "speech", "waveform"}:
        return "audio"
    if term in {"world", "world-model", "worldmodel", "planning"}:
        return "world"
    if term in {
        "masking",
        "mask",
        "context",
        "contextual",
        "in-context",
        "auxiliary",
        "auxiliary objectives",
        "ablation",
        "normalization",
        "feature normalization",
        "stability",
        "linear",
        "probe",
        "downstream",
        "evaluation",
    }:
        return "analysis"
    if term in {"byol", "simclr", "reconstruction", "contrastive"}:
        return "baseline"
    return ""


def alias_boost(term: str, paper_id: str, title: str) -> int:
    alias_targets = {
        "byol": ("bootstrap your own latent",),
        "i-jepa": ("joint embedding predictive architecture",),
        "ijepa": ("joint embedding predictive architecture",),
        "v-jepa": ("v jepa", "video jepa"),
        "vjepa": ("v jepa", "video jepa"),
        "audio-jepa": ("audio jepa",),
        "lejepa": ("lejepa",),
        "lpjepa": ("lpjepa", "rectified lpjepa"),
    }
    targets = alias_targets.get(term, ())
    if not targets:
        return 0
    for target in targets:
        if target in title or target in paper_id:
            return 8
    return 0


def score_row(row: dict, query_terms: list[str]) -> tuple[int, dict]:
    paper_id = norm(row.get("paper_id", ""))
    title = norm(first_present(row, "title", "title_guess"))
    source_file = norm(first_present(row, "source_file", "current_name"))
    modality = norm(row.get("modality", ""))
    task = norm(row.get("task", ""))
    tier = norm(row.get("tier", ""))
    evidence_level = norm(row.get("evidence_level", ""))
    code_link_status = norm(row.get("code_link_status", ""))
    link_confidence = norm(row.get("link_confidence", ""))
    notes = norm(row.get("notes", ""))
    hay = " ".join([paper_id, title, source_file, modality, task, notes])

    score = 0
    matched_terms: list[str] = []

    for term in query_terms:
        if not term:
            continue
        if title == term:
            score += 10
            matched_terms.append(term)
            continue
        if term in title:
            score += 6
            matched_terms.append(term)
            continue
        if term in paper_id:
            score += 9
            matched_terms.append(term)
            continue
        if term in source_file:
            score += 7
            matched_terms.append(term)
            continue
        if term in hay:
            score += 2
            matched_terms.append(term)

        score += alias_boost(term, paper_id, title)

        category = classify_term(term)
        if category == "image" and ("i-jepa" in title or "ijepa" in paper_id):
            score += 5
        elif category == "video" and ("v-jepa" in title or "vjepa" in paper_id or "video" in title):
            score += 5
        elif category == "audio" and "audio" in title:
            score += 5
        elif category == "multimodal" and (
            "multimodal" in title
            or "vision-language" in title
            or "vision language" in title
            or "clinical" in title
        ):
            score += 5
        elif category == "world" and ("world model" in title or "world models" in title or "planning" in title):
            score += 4
        elif category == "analysis" and any(
            x in title for x in ("mask", "context", "auxiliary", "normalization", "linear", "ablation", "stability")
        ):
            score += 5
        elif category == "baseline" and any(x in title for x in ("byol", "simclr", "reconstruct", "contrastive")):
            score += 4

    if score == 0:
        return 0, {}

    if tier == "core":
        score += 3
    if "jepa" in title or "jepa" in paper_id:
        score += 5
    if evidence_level == "primary":
        score += 2
    elif evidence_level == "analysis":
        score += 3
    elif evidence_level == "official":
        score += 2

    if code_link_status == "exact_local_match":
        score += 3
    elif code_link_status == "family_match_only":
        score += 1
    elif code_link_status == "multiple_local_candidates":
        score -= 1

    if link_confidence == "high":
        score += 1
    elif link_confidence == "low":
        score -= 1

    if modality and any(term in modality for term in query_terms):
        score += 2
    if task and any(term in task for term in query_terms):
        score += 2

    diagnostics = {
        "matched_terms": ",".join(dict.fromkeys(matched_terms)),
        "tier_bonus": "3" if tier == "core" else "0",
        "code_link_status": row.get("code_link_status", ""),
    }
    return score, diagnostics


def main() -> None:
    parser = argparse.ArgumentParser(description="Build ranked JEPA citation candidates from papers metadata.")
    parser.add_argument("--metadata", required=True, help="Path to papers_index.csv or paper_catalog.csv")
    parser.add_argument("--query", required=True, help="Comma-separated query terms")
    parser.add_argument("--topk", type=int, default=20, help="Maximum rows to output")
    parser.add_argument("--output", required=True, help="Output CSV path")
    args = parser.parse_args()

    meta_path = Path(args.metadata)
    out_path = Path(args.output)
    query_terms = split_query_terms(args.query)

    with meta_path.open("r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))

    scored = []
    for row in rows:
        s, diagnostics = score_row(row, query_terms)
        if s > 0:
            scored.append((s, row, diagnostics))

    scored.sort(
        key=lambda x: (
            -x[0],
            norm(x[1].get("tier", "")) != "core",
            x[1].get("paper_id", ""),
        )
    )
    top_rows = scored[: args.topk]

    fieldnames = [
        "paper_id",
        "title",
        "year",
        "arxiv_id",
        "tier",
        "source_file",
        "paper_path",
        "code_id",
        "code_link_status",
        "link_confidence",
        "score",
        "matched_terms",
        "query",
    ]
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for score, row, diagnostics in top_rows:
            writer.writerow(
                {
                    "paper_id": row.get("paper_id", ""),
                    "title": first_present(row, "title", "title_guess"),
                    "year": first_present(row, "year", "year_guess"),
                    "arxiv_id": row.get("arxiv_id", ""),
                    "tier": row.get("tier", ""),
                    "source_file": first_present(row, "source_file", "current_name"),
                    "paper_path": first_present(row, "paper_path", "relative_path"),
                    "code_id": row.get("code_id", ""),
                    "code_link_status": row.get("code_link_status", ""),
                    "link_confidence": row.get("link_confidence", ""),
                    "score": score,
                    "matched_terms": diagnostics.get("matched_terms", ""),
                    "query": args.query,
                }
            )

    print(f"Wrote {len(top_rows)} rows to {out_path}")


if __name__ == "__main__":
    main()
