# Output Templates

## A) Paper Comparison

```markdown
Question:

Answer:
- ...

Comparison:
- Method objective: ...
- Prediction target: ...
- Masking/context strategy: ...
- Typical downstream tasks: ...

Evidence:
- [paper_id] filename
Confidence: high|medium|low
```

## B) Reproduction Planning

```markdown
Target paper:
Code candidates:

Environment:
Dataset:
Train command:
Eval command:

Risks:
- ...

Validation:
- ...

Evidence:
- E1 (paper): ...
- E2 (code/protocol): ...

Mapping:
- A1 -> E2
- A2 -> E2
- A3 -> E1,E2
- A4 -> E1,E2
```

## C) Debug Plan

```markdown
Observed error:

Likely root cause:
- ...

Fix sequence:
1. A1 ...
2. A2 ...

Checks:
- ...

Evidence:
- E1 (code/protocol): ...
- E2 (paper, optional): ...

Mapping:
- A1 -> E1
- A2 -> E1,E2

Confidence: high|medium|low
```

## D) Intro Draft

```markdown
Paragraph 1 (context and motivation):
Paragraph 2 (limits of prior SSL):
Paragraph 3 (JEPA angle and gap):
Paragraph 4 (your contribution setup):

Claim-to-citation map:
- C1 -> [paper_id]
- C2 -> [paper_id]
```
