# Eval Suite (v1.0.1)

This folder validates JEPA skill v1 capabilities without changing skill behavior.

## Files

- `test_prompts_v1.jsonl`: 40 evaluation prompts (4 modes x 10 each).
- `scoring_rubric.md`: manual judging rubric.
- `results_schema.md`: expected result JSONL schema.
- `summarize_eval.py`: aggregate score report from judged results.

## Workflow

1. Run each prompt against the skill and save model outputs.
2. Judge each output using `scoring_rubric.md`.
3. Save judged rows into `eval/results/<run_name>.jsonl`.
4. Generate summary:

```powershell
python eval/summarize_eval.py --input eval/results/baseline_v1_0_0.jsonl --output eval/results/baseline_v1_0_0_summary.md
```

## Recommended baseline runs

- `baseline_v1_0_0`: tag `v1.0.0`
- `baseline_v1_0_1_eval`: same skill behavior, eval assets added

