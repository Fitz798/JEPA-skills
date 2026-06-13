# v1.2.0 Benchmark Comparison

## Scope

This comparison combines:

- historical judged benchmark summaries already in `eval/results/`
- the QA-only slice used for `JEPA-206` and `JEPA-207`
- new metadata quality gates added for `v1.2.0`

## Judged Benchmark Snapshot

| Metric | v1.0.0 Full40 | Current Full40 Reference | Delta |
|---|---:|---:|---:|
| Factual correctness | 92.5% | 92.5% | +0.0% |
| Citation hit | 65.0% | 95.0% | +30.0% |
| Executability | 90.0% | 90.0% | +0.0% |
| Debug hit | 90.0% | 90.0% | +0.0% |
| Hallucination rate | 0.0% | 0.0% | +0.0% |

Reference files:

- `eval/results/baseline_v1_0_0_full40_summary.md`
- `eval/results/v1_1_0_full40_summary.md`

## Research QA Slice

| Metric | v1.0.0 QA | Current QA Reference | Delta |
|---|---:|---:|---:|
| Factual correctness | 90.0% | 90.0% | +0.0% |
| Citation hit | 80.0% | 80.0% | +0.0% |
| Hallucination rate | 0.0% | 0.0% | +0.0% |

Interpretation:

- `JEPA-206` ranking changes and `JEPA-207` QA slicing infrastructure are in place.
- On the existing judged `research_qa` slice, citation hit did not improve.
- `v1.2.0` should therefore claim better metadata structure and release hygiene, not a proven QA retrieval gain.

Reference files:

- `eval/results/baseline_v1_0_0_research_qa_summary.md`
- `eval/results/v1_1_0_research_qa_summary.md`

## Data Quality Gates Added In v1.2.0

| Gate | Result |
|---|---|
| Evidence index validation | PASS |
| Core metadata completeness gate | PASS |
| Core modality coverage | 11/11 |
| Core task coverage | 11/11 |
| Core evidence level coverage | 11/11 |
| Core code link status coverage | 11/11 |
| Core link confidence coverage | 11/11 |

Reference files:

- `eval/results/evidence_index_validation.json`
- `eval/results/metadata_completeness_report.json`

## Regressions Or Gaps

- No judged improvement yet on the historical `research_qa` citation-hit slice.
- Long-tail metadata coverage is still intentionally sparse:
  - modality coverage: `11/148`
  - task coverage: `11/148`
  - evidence level coverage: `11/148`
- Core rows have explicit linkage status, but only `3/11` core papers have a confirmed local `code_id`.

## Changelog-Ready Release Bullets

- added a production `evidence_index.csv` plus schema and validator
- added rerunnable metadata completeness checks with machine-readable output
- encoded core paper metadata and conservative paper-to-code linkage into the catalog build path
- documented the `v1.2.0` release and eval workflow end to end
- established that current QA retrieval quality is stable on the judged slice, but not yet improved
