# Contributing to JEPA Skills

## Quick start

1. Clone the repo (corpus assets are not included — see below).
2. Run the sanity check:

```powershell
python scripts/build_paper_catalog.py --input metadata/papers_index.csv --output metadata/paper_catalog.csv
python scripts/validate_evidence_index.py --input metadata/evidence_index.csv
python scripts/check_metadata_completeness.py --input metadata/paper_catalog.csv --json eval/results/metadata_completeness_report.json
```

3. Read `CLAUDE.md` for architecture overview and common commands.

## What to contribute

| Area | Ideas |
|------|-------|
| **Metadata** | Add modality/task/evidence_level for unannotated papers in `paper_catalog.csv` |
| **Evidence** | Add new evidence rows to `evidence_index.csv` for papers or code artifacts |
| **Code links** | Find and verify remote repositories for papers without code links |
| **Eval** | Propose new eval prompts for edge cases not covered by the 40-prompt set |
| **Docs** | Fix errors, improve clarity, add examples |

## Development conventions

- Python scripts use stdlib only (no pip dependencies).
- Run commands from repo root so relative paths resolve correctly.
- Validate on Python 3.11+.
- Evidence IDs (`E0001`-`E0018`) in `evidence_index.csv` are stable — do not renumber existing rows. New evidence gets the next available ID.
- Paper-code links follow the conservative policy in `docs/paper-code-linking-policy.md`.

## Eval workflow

1. Make your change to the skill or metadata.
2. Run relevant eval prompts through the skill.
3. Judge outputs against `eval/scoring_rubric.md`.
4. Save scored JSONL and generate summary:

```powershell
python eval/summarize_eval.py --input eval/results/<scored>.jsonl --output eval/results/<summary>.md
```

5. Compare against the latest benchmark in `eval/results/`.

## Release process

See `docs/v1.2.0-release-eval-workflow.md` for the full rerunnable workflow. A release is complete when:

1. Paper catalog rebuilds cleanly
2. Evidence index validates
3. Metadata completeness gate passes (`core_gate_ok: true`)
4. Benchmark comparison doc exists with measured deltas
5. CHANGELOG.md, VERSION, and git tag are updated

## Corpus access

This repo does not distribute paper PDFs or code archives. To work with local corpus assets:

1. Place papers under `corpus/papers/all/`
2. Place code archives under `corpus/code/archives/`
3. Use `scripts/organize_jepa_corpus.ps1` to ingest from existing collections
4. Run `--check-paths` validation to verify local paths

## License

MIT. Third-party papers and code referenced by metadata have their own licenses — users are responsible for compliance.
