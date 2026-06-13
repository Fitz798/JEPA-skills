# Eval Suite (v1.0.1)

This folder validates JEPA skill v1 capabilities without changing skill behavior.

## Files

- `test_prompts_v1.jsonl`: 40 evaluation prompts (4 modes x 10 each).
- `scoring_rubric.md`: manual judging rubric.
- `results_schema.md`: expected result JSONL schema.
- `summarize_eval.py`: aggregate score report from judged results.
- `filter_eval_by_mode.py`: extracts a mode-specific JSONL slice for prompts or judged results.
- `check_evidence_coverage.py`: checks whether responses include Evidence+Mapping blocks.
- `../scripts/check_metadata_completeness.py`: checks `paper_catalog.csv` coverage for release gating.

## Workflow

1. Run each prompt against the skill and save model outputs.
2. Judge each output using `scoring_rubric.md`.
3. Save judged rows into `eval/results/<run_name>.jsonl`.
4. Generate summary:

```powershell
python eval/summarize_eval.py --input eval/results/baseline_v1_0_0.jsonl --output eval/results/baseline_v1_0_0_summary.md
```

5. (Optional) check evidence-format compliance from markdown responses:

```powershell
python eval/check_evidence_coverage.py --responses eval/results/baseline_v1_0_0_rp_dbg_wrt30_responses.md --output eval/results/coverage_rp_dbg_wrt30.json
```

## QA-only workflow

Extract the `research_qa` prompt slice:

```powershell
python eval/filter_eval_by_mode.py --input eval/test_prompts_v1.jsonl --mode research_qa --output eval/results/research_qa_prompts_v1.jsonl
```

Extract the `research_qa` judged-result slice and summarize it:

```powershell
python eval/filter_eval_by_mode.py --input eval/results/v1_1_0_full40_scored.jsonl --mode research_qa --output eval/results/v1_1_0_research_qa_scored.jsonl
python eval/summarize_eval.py --input eval/results/v1_1_0_research_qa_scored.jsonl --output eval/results/v1_1_0_research_qa_summary.md
```

Use the same flow for baseline comparisons, for example:

```powershell
python eval/filter_eval_by_mode.py --input eval/results/baseline_v1_0_0_full40_scored.jsonl --mode research_qa --output eval/results/baseline_v1_0_0_research_qa_scored.jsonl
python eval/summarize_eval.py --input eval/results/baseline_v1_0_0_research_qa_scored.jsonl --output eval/results/baseline_v1_0_0_research_qa_summary.md
```

## Metadata Release Gate

Before a public `v1.2.0` release, run:

```powershell
python scripts/build_paper_catalog.py --input metadata/papers_index.csv --output metadata/paper_catalog.csv
python scripts/check_metadata_completeness.py --input metadata/paper_catalog.csv --json eval/results/metadata_completeness_report.json
```

The release gate passes only if the report says the core metadata gate passed.

## Recommended baseline runs

- `baseline_v1_0_0`: tag `v1.0.0`
- `baseline_v1_0_1_eval`: same skill behavior, eval assets added
