# Changelog

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
