# Research QA Full Rerun Checklist

Use this after the targeted `RQ05` and `RQ07` validation has passed.

## Goal

- refresh the 10-prompt `research_qa` judged slice
- verify whether citation hit rises above the current `80%`

## Inputs

- prompts: `eval/results/research_qa_prompts_v1.jsonl`
- baseline reference: `eval/results/baseline_v1_0_0_research_qa_summary.md`
- targeted validation proof:
  - `eval/results/research_qa_targeted_rerun_scored.jsonl`
  - `eval/results/research_qa_targeted_rerun_summary.md`

## Execution Steps

1. Run the 10 `research_qa` prompts against the updated skill.
2. Save raw responses to a new markdown artifact.
3. Judge each of the 10 outputs using `eval/scoring_rubric.md`.
4. Save judged rows as a new JSONL result file.
5. Generate a summary with `python eval/summarize_eval.py`.
6. Compare the new summary against:
   - `eval/results/baseline_v1_0_0_research_qa_summary.md`
   - `eval/results/v1_1_0_research_qa_summary.md`

## Required Output Files

- `eval/results/<new_run_name>_research_qa_responses.md`
- `eval/results/<new_run_name>_research_qa_scored.jsonl`
- `eval/results/<new_run_name>_research_qa_summary.md`

## Success Condition

- citation hit is greater than `80%`

## Failure Condition

- citation hit remains `80%` or below

If failure happens:

- inspect whether misses are still concentrated in synthesis-heavy prompts
- decide whether the next move is:
  - more retrieval metadata
  - answer-format constraints
  - stronger claim-to-citation mapping rules
