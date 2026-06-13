import argparse
import json
from pathlib import Path


def load_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open("r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON at line {line_no}: {e}") from e
    return rows


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Filter JEPA eval prompts or judged results by mode.")
    parser.add_argument("--input", required=True, help="Input JSONL path")
    parser.add_argument("--mode", required=True, help="Mode to keep, for example research_qa")
    parser.add_argument("--output", required=True, help="Output JSONL path")
    args = parser.parse_args()

    rows = load_jsonl(Path(args.input))
    kept = [row for row in rows if row.get("mode") == args.mode]
    write_jsonl(Path(args.output), kept)
    print(f"Wrote {len(kept)} rows to {args.output}")


if __name__ == "__main__":
    main()
