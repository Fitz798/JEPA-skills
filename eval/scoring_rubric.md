# Scoring Rubric

Use this rubric to score each response row in `eval/results/*.jsonl`.

## 1) Factual Correctness (`factual_correct`)

Set `1` only if all major claims are consistent with available papers/metadata/code context.

Set `0` when response includes at least one major incorrect claim.

## 2) Citation Hit (`citation_hit`)

Set `1` when citations/evidence references support the stated claim and are traceable.

Set `0` when references are missing, irrelevant, or untraceable.

## 3) Executability (`executable`)

For reproduction prompts only.

Set `1` when plan includes concrete runnable steps (env/data/command/check criteria).

Set `0` when steps are too vague or cannot be executed.

## 4) Debug Hit (`debug_hit`)

For debug prompts only.

Set `1` when top-1 diagnosis/fix is plausible and ordered before lower-probability fixes.

Set `0` when primary diagnosis is likely wrong or unsafe.

## 5) Hallucination (`hallucination`)

Set `1` if response invents paper identities, code artifacts, metrics, or commands.

Set `0` if no clear hallucination is found.

## Acceptance targets for v1 baseline

- Factual correctness >= 0.75
- Citation hit >= 0.70
- Executability >= 0.70
- Debug hit >= 0.60
- Hallucination rate <= 0.15

