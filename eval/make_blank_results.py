import argparse
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Create a blank judged-results file from prompt JSONL.")
    parser.add_argument("--prompts", required=True, help="Path to prompt JSONL")
    parser.add_argument("--output", required=True, help="Path to output result JSONL")
    args = parser.parse_args()

    prompts = Path(args.prompts)
    output = Path(args.output)

    rows = []
    for line in prompts.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        p = json.loads(line)
        rows.append(
            {
                "id": p.get("id"),
                "mode": p.get("mode"),
                "prompt": p.get("prompt"),
                "response_path": "",
                "factual_correct": None,
                "citation_hit": None,
                "executable": None,
                "debug_hit": None,
                "hallucination": 0,
                "notes": "",
            }
        )

    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"Wrote {len(rows)} blank rows to {output}")


if __name__ == "__main__":
    main()

