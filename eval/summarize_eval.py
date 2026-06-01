import argparse
import json
from collections import defaultdict
from pathlib import Path


METRICS = ["factual_correct", "citation_hit", "executable", "debug_hit", "hallucination"]


def safe_rate(rows, key):
    vals = [r[key] for r in rows if r.get(key) is not None]
    if not vals:
        return None, 0
    return sum(vals) / len(vals), len(vals)


def pct(x):
    if x is None:
        return "n/a"
    return f"{x * 100:.1f}%"


def load_jsonl(path: Path):
    rows = []
    with path.open("r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON at line {line_no}: {e}") from e
            rows.append(obj)
    return rows


def build_report(rows):
    by_mode = defaultdict(list)
    for r in rows:
        by_mode[r.get("mode", "unknown")].append(r)

    overall = {}
    for m in METRICS:
        overall[m] = safe_rate(rows, m)

    mode_stats = {}
    for mode, mrows in sorted(by_mode.items()):
        mode_stats[mode] = {m: safe_rate(mrows, m) for m in METRICS}

    return overall, mode_stats


def to_markdown(input_name, rows, overall, mode_stats):
    lines = []
    lines.append(f"# Eval Summary: {input_name}")
    lines.append("")
    lines.append(f"- Total prompts judged: {len(rows)}")
    lines.append("")
    lines.append("## Overall")
    lines.append("")
    lines.append("| Metric | Rate | N |")
    lines.append("|---|---:|---:|")
    lines.append(f"| Factual correctness | {pct(overall['factual_correct'][0])} | {overall['factual_correct'][1]} |")
    lines.append(f"| Citation hit | {pct(overall['citation_hit'][0])} | {overall['citation_hit'][1]} |")
    lines.append(f"| Executability | {pct(overall['executable'][0])} | {overall['executable'][1]} |")
    lines.append(f"| Debug hit | {pct(overall['debug_hit'][0])} | {overall['debug_hit'][1]} |")
    lines.append(f"| Hallucination rate | {pct(overall['hallucination'][0])} | {overall['hallucination'][1]} |")
    lines.append("")
    lines.append("## By Mode")
    lines.append("")
    for mode, stats in mode_stats.items():
        lines.append(f"### {mode}")
        lines.append("")
        lines.append("| Metric | Rate | N |")
        lines.append("|---|---:|---:|")
        lines.append(f"| Factual correctness | {pct(stats['factual_correct'][0])} | {stats['factual_correct'][1]} |")
        lines.append(f"| Citation hit | {pct(stats['citation_hit'][0])} | {stats['citation_hit'][1]} |")
        lines.append(f"| Executability | {pct(stats['executable'][0])} | {stats['executable'][1]} |")
        lines.append(f"| Debug hit | {pct(stats['debug_hit'][0])} | {stats['debug_hit'][1]} |")
        lines.append(f"| Hallucination rate | {pct(stats['hallucination'][0])} | {stats['hallucination'][1]} |")
        lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Summarize JEPA skill eval results.")
    parser.add_argument("--input", required=True, help="Path to judged result JSONL")
    parser.add_argument("--output", required=True, help="Path to output markdown summary")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    rows = load_jsonl(input_path)
    overall, mode_stats = build_report(rows)
    md = to_markdown(input_path.name, rows, overall, mode_stats)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(md, encoding="utf-8")
    print(f"Wrote summary: {output_path}")


if __name__ == "__main__":
    main()

