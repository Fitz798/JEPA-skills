# JEPA Skills

A reusable skill package for Claude Code, Codex, and similar coding/research agents focused on JEPA research workflows.

## What this project provides

- `jepa-research/SKILL.md`: JEPA research skill definition (triggering + workflow).
- `metadata/`: structured indexes and templates for citations, evidence, and eval protocol.
- `scripts/`: corpus organization and metadata build scripts.
- `docs/v1.2.0-roadmap.md`: next release roadmap and issue breakdown.
- `docs/v1.2.0-execution-todo.md`: execution checklist for the current release.
- `docs/evidence-index-schema.md`: production schema for structured evidence records.
- `docs/paper-code-linking-policy.md`: conservative policy for linking papers to local code archives.
- `docs/v1.2.0-release-eval-workflow.md`: rerunnable release and evaluation workflow for `v1.2.0`.

## What this project does not bundle by default

- Full paper PDFs and full third-party codebases should usually stay local.
- For open-source publishing, share metadata + scripts; fetch source artifacts on demand.

## Repository layout

```text
.
+-- jepa-research/
|   +-- SKILL.md
|   +-- references/
|   `-- scripts/
+-- metadata/
+-- scripts/
`-- corpus/                   # local cache; large files ignored by default
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

## Environment and migration notes

- The Python scripts in this repo use the standard library only. There is currently no `requirements.txt` or `pyproject.toml`.
- Validate on Python `3.11+`. This repo was checked successfully with Python `3.13.5`.
- Run commands from the repo root so relative paths resolve correctly.
- The current corpus layout expected by metadata and evidence files is:
  - `corpus/papers/all/`
  - `corpus/code/archives/`
- The optional import script `scripts/organize_jepa_corpus.ps1` can ingest raw assets from:
  - `JEPA-Papers/`
  - `JEPA-Papers/awesome-jepa/`
  - `JEPA-CodeBase/`
- After moving the repo to another machine, the recommended sanity check is:

```powershell
python scripts/build_paper_catalog.py --input metadata/papers_index.csv --output metadata/paper_catalog.csv
python scripts/validate_evidence_index.py --input metadata/evidence_index.csv --check-paths --json eval/results/evidence_index_validation.json
python scripts/check_metadata_completeness.py --input metadata/paper_catalog.csv --json eval/results/metadata_completeness_report.json
```

## Skill capabilities (v1)

- Research Q&A with traceable evidence.
- Reproduction planning and config guidance.
- Code-debug assistance (entrypoint/config/log failure triage).
- Introduction/related-work drafting with citation candidate lists.
- Citation recommendation from local metadata.

## Open-source readiness

This repo is already safe to open-source as a metadata-and-workflow package if you keep third-party paper PDFs and code archives out of Git.

For a stronger public `v1.2.0` release, the recommended minimum is:

1. production evidence schema documented
2. initial `evidence_index.csv` or a strong template with examples
3. validation scripts for evidence and metadata completeness
4. documented eval workflow that another contributor can rerun

Evidence validation command:

```powershell
python scripts/validate_evidence_index.py --input metadata/evidence_index.csv
```

Metadata completeness command:

```powershell
python scripts/check_metadata_completeness.py --input metadata/paper_catalog.csv --json eval/results/metadata_completeness_report.json
```

## Open-source release checklist

1. Keep `.gitignore` defaults for `corpus/papers/all` and `corpus/code/archives`.
2. Keep metadata CSVs and templates.
3. Add your preferred `LICENSE` (MIT recommended for this repo code).
4. Include a short disclaimer: users are responsible for third-party paper/code licenses.
