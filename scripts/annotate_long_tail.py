"""Annotate long-tail papers with modality, task, and evidence_level.

Usage:
  python scripts/annotate_long_tail.py --input metadata/paper_catalog.csv --output metadata/paper_catalog.csv
"""

import argparse
import csv
from pathlib import Path


# Inferred from paper title keywords for each unannotated JEPA-title paper.
# Format: paper_id -> {modality, task, evidence_level}
ANNOTATIONS = {
    "arxiv_2501.14622": {"modality": "robotics", "task": "policy learning", "evidence_level": "primary"},
    "arxiv_2605.05586": {"modality": "3d", "task": "representation learning", "evidence_level": "primary"},
    "arxiv_2601.00366": {"modality": "language", "task": "representation learning", "evidence_level": "primary"},
    "arxiv_2605.24631": {"modality": "vision", "task": "generation", "evidence_level": "primary"},
    "arxiv_2603.00049": {"modality": "vision", "task": "representation learning", "evidence_level": "primary"},
    "arxiv_2602.11389": {"modality": "vision", "task": "world model", "evidence_level": "primary"},
    "arxiv_2602.02093": {"modality": "genomics", "task": "representation learning", "evidence_level": "primary"},
    "arxiv_2605.10840": {"modality": "clinical", "task": "representation learning", "evidence_level": "primary"},
    "arxiv_2511.18424": {"modality": "multimodal", "task": "3d representation learning", "evidence_level": "primary"},
    "arxiv_2605.14759": {"modality": "materials", "task": "generation", "evidence_level": "primary"},
    "arxiv_2511.17354": {"modality": "vision", "task": "representation learning", "evidence_level": "primary"},
    "arxiv_2605.20811": {"modality": "robotics", "task": "policy learning", "evidence_level": "primary"},
    "arxiv_2601.22032": {"modality": "multimodal", "task": "planning", "evidence_level": "primary"},
    "arxiv_2604.23336": {"modality": "language", "task": "retrieval", "evidence_level": "primary"},
    "arxiv_2602.14771": {"modality": "vision", "task": "tracking", "evidence_level": "primary"},
    "arxiv_2510.05949": {"modality": "vision", "task": "representation analysis", "evidence_level": "analysis"},
    "arxiv_2602.07016": {"modality": "vision", "task": "scene understanding", "evidence_level": "primary"},
    "arxiv_2605.31580": {"modality": "multimodal", "task": "representation learning", "evidence_level": "primary"},
    "arxiv_2605.31068": {"modality": "multimodal", "task": "representation learning", "evidence_level": "primary"},
    "arxiv_2602.07000": {"modality": "networks", "task": "prediction", "evidence_level": "primary"},
    "arxiv_2510.21840": {"modality": "video", "task": "generation", "evidence_level": "primary"},
    "arxiv_2602.17162": {"modality": "genomics", "task": "representation learning", "evidence_level": "primary"},
    "arxiv_2603.29796": {"modality": "multimodal", "task": "sensing", "evidence_level": "primary"},
    "arxiv_2512.19171": {"modality": "language", "task": "reasoning", "evidence_level": "primary"},
    "arxiv_2510.00974": {"modality": "multimodal", "task": "generation", "evidence_level": "primary"},
    "arxiv_2504.10512": {"modality": "language", "task": "recommendation", "evidence_level": "primary"},
    "arxiv_2604.21046": {"modality": "vision", "task": "semi-supervised learning", "evidence_level": "primary"},
    "arxiv_2512.19605": {"modality": "vision", "task": "representation learning", "evidence_level": "primary"},
    "arxiv_2603.13265": {"modality": "language", "task": "reasoning", "evidence_level": "primary"},
    "arxiv_2509.14252": {"modality": "language", "task": "representation learning", "evidence_level": "primary"},
    "arxiv_2603.16281": {"modality": "eeg", "task": "representation learning", "evidence_level": "primary"},
    "arxiv_2511.08544": {"modality": "vision", "task": "representation learning", "evidence_level": "primary"},
    "arxiv_2602.04643": {"modality": "time-series", "task": "representation learning", "evidence_level": "primary"},
    "arxiv_2605.14120": {"modality": "time-series", "task": "prediction", "evidence_level": "primary"},
    "arxiv_2604.01349": {"modality": "physics", "task": "simulation", "evidence_level": "primary"},
    "arxiv_2601.15891": {"modality": "clinical", "task": "representation learning", "evidence_level": "primary"},
    "arxiv_2602.01456": {"modality": "vision", "task": "representation learning", "evidence_level": "primary"},
    "arxiv_2605.15394": {"modality": "language", "task": "representation analysis", "evidence_level": "analysis"},
    "arxiv_2509.24317": {"modality": "video", "task": "representation learning", "evidence_level": "analysis"},
    "arxiv_2602.12540": {"modality": "lidar", "task": "world model", "evidence_level": "primary"},
    "arxiv_2605.09241": {"modality": "vision", "task": "world model", "evidence_level": "primary"},
    "arxiv_2605.31111": {"modality": "vision", "task": "world model", "evidence_level": "primary"},
    "arxiv_2605.03245": {"modality": "multimodal", "task": "representation learning", "evidence_level": "primary"},
    "arxiv_2602.19322": {"modality": "clinical", "task": "representation learning", "evidence_level": "primary"},
    "arxiv_2603.20111": {"modality": "vision", "task": "world model", "evidence_level": "primary"},
    "arxiv_2601.20190": {"modality": "wireless", "task": "representation learning", "evidence_level": "primary"},
    "arxiv_2505.03176": {"modality": "vision", "task": "world model", "evidence_level": "primary"},
    # Additional relevant non-JEPA-title papers to reach 80+ coverage
    "arxiv_2410.08559": {"modality": "clinical", "task": "representation learning", "evidence_level": "primary"},
    "arxiv_2507.15216": {"modality": "vision", "task": "representation learning", "evidence_level": "primary"},
    "arxiv_2602.03604": {"modality": "vision", "task": "tooling", "evidence_level": "primary"},
    "arxiv_2601.19822": {"modality": "engineering", "task": "prediction", "evidence_level": "primary"},
    "arxiv_2509.25449": {"modality": "time-series", "task": "representation learning", "evidence_level": "primary"},
    "arxiv_2603.19312": {"modality": "vision", "task": "world model", "evidence_level": "primary"},
    "arxiv_2601.01577": {"modality": "robotics", "task": "world model", "evidence_level": "primary"},
    "arxiv_2602.12245": {"modality": "vision", "task": "representation analysis", "evidence_level": "analysis"},
    "arxiv_2502.18056": {"modality": "vision", "task": "representation analysis", "evidence_level": "analysis"},
    "arxiv_2507.03633": {"modality": "eeg", "task": "representation learning", "evidence_level": "primary"},
    "arxiv_2511.16333": {"modality": "clinical", "task": "world model", "evidence_level": "primary"},
    # Batch 2: top-25 most relevant remaining papers (v1.4.0 prep)
    "arxiv_2501.04969": {"modality": "lidar", "task": "object detection", "evidence_level": "primary"},
    "arxiv_2602.09040": {"modality": "audio", "task": "representation learning", "evidence_level": "primary"},
    "arxiv_2502.01684": {"modality": "graph", "task": "representation learning", "evidence_level": "primary"},
    "arxiv_2603.26799": {"modality": "vision", "task": "representation learning", "evidence_level": "primary"},
    "arxiv_2508.10489": {"modality": "time-series", "task": "system identification", "evidence_level": "primary"},
    "arxiv_2605.11130": {"modality": "time-series", "task": "prediction", "evidence_level": "primary"},
    "arxiv_2601.09524": {"modality": "video", "task": "classification", "evidence_level": "primary"},
    "arxiv_2603.20048": {"modality": "wireless", "task": "world model", "evidence_level": "primary"},
    "arxiv_2604.13518": {"modality": "vision", "task": "representation analysis", "evidence_level": "analysis"},
    "arxiv_2604.16585": {"modality": "vision", "task": "world model", "evidence_level": "primary"},
    "arxiv_2605.21963": {"modality": "clinical", "task": "world model", "evidence_level": "primary"},
    "arxiv_2502.14819": {"modality": "robotics", "task": "planning", "evidence_level": "primary"},
    "arxiv_2508.00447": {"modality": "multimodal", "task": "representation learning", "evidence_level": "primary"},
    "arxiv_2511.09783": {"modality": "time-series", "task": "representation analysis", "evidence_level": "analysis"},
    "arxiv_2601.03665": {"modality": "video", "task": "generation", "evidence_level": "primary"},
    "arxiv_2601.06212": {"modality": "multimodal", "task": "representation learning", "evidence_level": "primary"},
    "arxiv_2603.19100": {"modality": "eeg", "task": "representation learning", "evidence_level": "primary"},
    "arxiv_2603.22649": {"modality": "clinical", "task": "representation analysis", "evidence_level": "analysis"},
    "arxiv_2604.08503": {"modality": "video", "task": "generation", "evidence_level": "primary"},
    "arxiv_2601.22128": {"modality": "clinical", "task": "world model", "evidence_level": "primary"},
    "arxiv_2603.25216": {"modality": "wireless", "task": "world model", "evidence_level": "primary"},
    "arxiv_2604.16333": {"modality": "multimodal", "task": "reasoning", "evidence_level": "primary"},
    "arxiv_2507.19119": {"modality": "time-series", "task": "prediction", "evidence_level": "primary"},
    "arxiv_2602.02620": {"modality": "vision", "task": "representation learning", "evidence_level": "primary"},
    "arxiv_2602.14642": {"modality": "physics", "task": "simulation", "evidence_level": "primary"},
}


def main():
    parser = argparse.ArgumentParser(description="Annotate long-tail papers with modality, task, and evidence_level.")
    parser.add_argument("--input", required=True, help="Path to paper_catalog.csv")
    parser.add_argument("--output", required=True, help="Output CSV path")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    with input_path.open("r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))

    updated = 0
    skipped = 0
    for row in rows:
        pid = row.get("paper_id", "").strip()
        if pid in ANNOTATIONS:
            ann = ANNOTATIONS[pid]
            # Only write if the field is currently empty
            if not row.get("modality", "").strip():
                row["modality"] = ann["modality"]
            if not row.get("task", "").strip():
                row["task"] = ann["task"]
            if not row.get("evidence_level", "").strip():
                row["evidence_level"] = ann["evidence_level"]
            updated += 1
        else:
            skipped += 1

    fieldnames = list(rows[0].keys())
    with output_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Annotated: {updated} papers")
    print(f"Untouched: {skipped} papers")
    print(f"Total: {len(rows)} papers")


if __name__ == "__main__":
    main()
