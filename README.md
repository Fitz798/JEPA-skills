# JEPA Skills

A reusable skill package for Claude Code, Codex, and similar coding/research agents focused on JEPA research workflows.

## What this project provides

- `jepa-research/SKILL.md`: JEPA research skill definition (triggering + workflow).
- `metadata/`: structured indexes and templates for citations, evidence, and eval protocol.
- `scripts/`: corpus organization and metadata build scripts.

## What this project does not bundle by default

- Full paper PDFs and full third-party codebases should usually stay local.
- For open-source publishing, share metadata + scripts; fetch source artifacts on demand.

## Repository layout

```text
.
├─ jepa-research/
│  ├─ SKILL.md
│  ├─ references/
│  └─ scripts/
├─ metadata/
├─ scripts/
└─ corpus/                 # local cache; large files ignored by default
```

## Quick start

1. Put your local paper/code assets under `corpus/` (optional for public repo users).
2. Build a shareable paper catalog:

```powershell
python scripts/build_paper_catalog.py --input metadata/papers_index.csv --output metadata/paper_catalog.csv
```

3. Use the skill:
   - Ask the agent about JEPA paper comparison, reproduction, debugging, intro drafting, and citations.
   - The skill expects evidence-style answers tied to metadata records.

## Skill capabilities (v1)

- Research Q&A with traceable evidence.
- Reproduction planning and config guidance.
- Code-debug assistance (entrypoint/config/log failure triage).
- Introduction/related-work drafting with citation candidate lists.
- Citation recommendation from local metadata.

## Open-source release checklist

1. Keep `.gitignore` defaults for `corpus/papers/all` and `corpus/code/archives`.
2. Keep metadata CSVs and templates.
3. Add your preferred `LICENSE` (MIT recommended for this repo code).
4. Include a short disclaimer: users are responsible for third-party paper/code licenses.

