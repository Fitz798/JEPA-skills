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
```

## C) Debug Plan

```markdown
Observed error:

Likely root cause:
- ...

Fix sequence:
1. ...
2. ...

Checks:
- ...

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

