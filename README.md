# JEPA Skills

A reusable skill package for Claude Code, Codex, and similar coding/research agents focused on JEPA research workflows.

## What this project provides

- `jepa-research/SKILL.md`: JEPA research skill definition (triggering + workflow, 4 modes).
- `metadata/`: structured indexes (papers, code, evidence) with 71% long-tail coverage.
- `scripts/`: corpus organization, metadata build, evidence validation, and annotation scripts.
- `eval/`: 40-prompt benchmark suite with scoring rubric and 5-version comparison history.
- `docs/`: roadmap, execution tracker, evidence schema, paper-code linking policy, release workflow.
- `CLAUDE.md`: project rules for Claude Code agents working in this repo.

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

## Skill capabilities (v1.3.0)

All 4 modes score 100% on the 40-prompt eval benchmark:

| Mode | Factual | Citation | Key Metric |
|------|---------|----------|------------|
| Research Q&A | 100% | 100% | — |
| Reproduction Plan | 100% | 100% | Executability 100% |
| Debug Triage | 100% | 100% | Debug Hit 100% |
| Writing/Citation | 100% | 100% | — |
| **Hallucination rate** | **0.0%** | | |

See `eval/results/v1_3_0_benchmark_comparison.md` for the full 5-version comparison from v1.0.0 to v1.3.0.

## Open-source readiness

This repo is ready to open-source as a metadata-and-workflow package. Third-party paper PDFs and code archives are excluded from Git by `.gitignore`.

Release gates (all passing for v1.3.0):

1. production evidence schema documented ✅
2. `evidence_index.csv` with real data ✅
3. validation scripts for evidence and metadata completeness ✅
4. documented eval workflow that another contributor can rerun ✅

Sanity check after cloning:

```powershell
python scripts/build_paper_catalog.py --input metadata/papers_index.csv --output metadata/paper_catalog.csv
python scripts/annotate_long_tail.py --input metadata/paper_catalog.csv --output metadata/paper_catalog.csv
python scripts/validate_evidence_index.py --input metadata/evidence_index.csv --check-paths --json eval/results/evidence_index_validation.json
python scripts/check_metadata_completeness.py --input metadata/paper_catalog.csv --json eval/results/metadata_completeness_report.json
```

## Open-source release checklist

1. Keep `.gitignore` defaults for `corpus/papers/all` and `corpus/code/archives` ✅
2. Keep metadata CSVs and templates ✅
3. MIT license included ✅
4. Users are responsible for third-party paper/code licenses ✅
