# Research QA Targeted Rerun Workflow

This workflow validates the first two targeted fixes before committing to a full `research_qa` rerun.

## Scope

- `RQ05`
- `RQ07`

## Inputs

- responses: `eval/results/research_qa_targeted_rerun_responses.md`
- scoring template: `eval/results/research_qa_targeted_rerun_scoring_template.jsonl`
- candidate snapshots:
  - `eval/results/rq05_targeted_candidates.csv`
  - `eval/results/rq07_targeted_candidates.csv`
- rubric: `eval/scoring_rubric.md`

## Manual Judgment Steps

1. Read the response section for `RQ05` or `RQ07`.
2. Cross-check the cited paper IDs against the targeted candidate CSV.
3. Score `factual_correct`.
4. Score `citation_hit`.
5. Leave `executable` and `debug_hit` as `null`.
6. Set `hallucination` to `0` unless a claim or paper is invented.
7. Replace the `null` fields in `research_qa_targeted_rerun_scoring_template.jsonl`.

## Pass Condition

- both `RQ05` and `RQ07` receive:
  - `factual_correct = 1`
  - `citation_hit = 1`
  - `hallucination = 0`

## If Passes

- proceed to a fresh 10-prompt `research_qa` judged rerun

## If Fails

- inspect whether the problem was:
  - weak retrieval candidate choice
  - too-abstract answer wording
  - unsupported cross-paper synthesis

Then revise ranking or answer structure before attempting the full rerun.
