# Changelog

## v1.2.1 - 2026-06-14

- **Full 10-prompt `research_qa` judged rerun**: factual correctness 100% (↑10pp), citation hit 100% (↑20pp vs baseline 80%).
- RQ05 (multimodal transfer commonalities) and RQ07 (linear eval sensitivity) — the two historical QA misses — both scored 100% after targeted retrieval fixes and improved evidence binding.
- Updated `v1_2_0_benchmark_comparison.md` with v1.2.1 QA deltas.
- All 10 JEPA-2xx issues now fully closed including the deferred JEPA-206 citation-hit comparison.
- Updated retrieval diagnosis with slice-level confirmation.

## v1.2.0 - 2026-06-13

- Added a production `metadata/evidence_index.csv` plus a documented schema in `docs/evidence-index-schema.md`.
- Added `scripts/validate_evidence_index.py` to validate evidence rows, IDs, anchors, allowed enums, and optional local artifact paths.
- Expanded `scripts/build_paper_catalog.py` and `metadata/paper_catalog.csv` with modality, task, evidence-level, and conservative paper-to-code linkage fields.
- Added `scripts/check_metadata_completeness.py` plus machine-readable release-gate output for core metadata coverage.
- Added `eval/filter_eval_by_mode.py` and documented a rerunnable QA-only evaluation flow.
- Added `docs/paper-code-linking-policy.md`, `docs/v1.2.0-release-eval-workflow.md`, and execution-tracking docs for the release process.
- Added targeted `research_qa` retrieval diagnostics and rerun artifacts for `RQ05` and `RQ07`.
- Confirmed `v1.2.0` improves metadata structure and release hygiene, while the historical judged `research_qa` slice remains flat at `80%` citation hit.

## v1.1.0 - 2026-06-01

- Added evidence-binding hard constraints in `jepa-research/SKILL.md`.
- Added `references/evidence_binding_rules.md` for citation/traceability policy.
- Updated output templates to require action/claim -> evidence mapping in reproduction/debug outputs.
- Added `eval/check_evidence_coverage.py` to measure Evidence+Mapping compliance in response markdown files.
- Added full40 evaluation comparison (`v1.1.0` vs `v1.0.0`) showing citation-hit improvement.

## v1.0.1 - 2026-06-01

- Added evaluation suite under `eval/` without changing skill behavior.
- Added 40 prompt benchmark set across four skill modes.
- Added manual scoring rubric and result schema.
- Added result templating script and summary report generator.

## v1.0.0 - 2026-06-01

- Initial open-source JEPA skill scaffold.
- Added `jepa-research/SKILL.md` with four core modes:
  - research Q&A
  - reproduction plan
  - debug triage
  - intro/related-work drafting
- Added helper references and citation candidate script.
- Added metadata templates for evidence index, eval protocol, and citation candidates.
- Added project-level README, MIT license, and third-party content disclaimer.
- Added `.gitignore` rules to keep large local corpus data out of Git by default.
