---
name: jepa-research
description: JEPA research and reproduction copilot. Use this skill whenever users ask about JEPA papers, I-JEPA/V-JEPA variants, JEPA world models, JEPA debugging, paper comparison, reproduction planning, introduction/related-work drafting, or finding JEPA citations for claims.
license: MIT
---

# JEPA Research Skill

Provide practical support for JEPA researchers and practitioners:

1. Answer research questions grounded in papers and code evidence.
2. Help reproduce JEPA-style methods with concrete run plans.
3. Help debug training/evaluation failures.
4. Draft introduction/related-work sections with citation candidates.

## Inputs you should look for

- User question or task statement.
- Local metadata files:
  - `metadata/papers_index.csv`
  - `metadata/paper_catalog.csv` (if available)
  - `metadata/code_index.csv`
  - `metadata/evidence_index.csv` (if available)
- Optional local corpus:
  - `corpus/papers/all/*`
  - `corpus/code/archives/*`

## Output contract

Always keep outputs actionable and traceable.

- For factual claims, include an **Evidence** block with file-level references.
- For uncertain claims, label confidence as `high`, `medium`, or `low`.
- For recommendations, include a short rationale and expected tradeoff.

Use one of the following modes based on user intent.

## Mode 1: Research Q&A

Use when user asks conceptual questions:
- JEPA vs contrastive SSL
- I-JEPA vs V-JEPA
- Why a certain objective or design works
- Current limitations and open problems

Steps:

1. Identify 3-8 relevant papers from metadata.
2. Cluster them by topic or method family.
3. Answer with:
   - concise conclusion
   - method differences
   - practical implication
4. Attach evidence references.

Template:

```markdown
Conclusion: ...

Key differences:
- ...
- ...

Practical implication:
- ...

Evidence:
- [paper_id] filename
- [paper_id] filename
Confidence: high|medium|low
```

## Mode 2: Reproduction Plan

Use when user asks to reproduce/train/evaluate a JEPA method.

Steps:

1. Map target paper to candidate code archives/repositories.
2. Produce a minimal runnable plan:
   - environment
   - data
   - config seed
   - expected compute
3. List likely failure points before run.
4. Provide first-run validation checks.

Template:

```markdown
Target:
- Paper: ...
- Candidate code: ...

Run plan:
1. Environment ...
2. Data ...
3. Train command ...
4. Eval command ...

Risk checks:
- ...
- ...

Pass criteria:
- ...
```

## Mode 3: Debug Triage

Use when user shares errors/logs/curves.

Steps:

1. Classify failure type:
   - dependency/env
   - data pipeline
   - shape/mask mismatch
   - optimization divergence
   - representation collapse
2. Ask for missing artifacts only if needed:
   - config file
   - exact command
   - first error stack
3. Return fix order (highest probability first).
4. Add a minimal verification check after each fix.

Template:

```markdown
Diagnosis:
- Primary hypothesis: ...
- Secondary hypotheses: ...

Fix order:
1. ...
2. ...
3. ...

Verify:
- check 1 ...
- check 2 ...

Evidence:
- ...
Confidence: high|medium|low
```

## Mode 4: Intro/Related-Work Drafting

Use when user asks to write introduction, related work, or literature summary.

Steps:

1. Build a storyline:
   - problem pressure
   - prior SSL limitations
   - JEPA contribution space
   - unresolved gaps
2. Draft section text.
3. Attach citation candidates with claim mapping.

Template:

```markdown
Draft:
<paragraphs>

Claim-to-citation map:
- C1: claim ... -> [paper_id_a], [paper_id_b]
- C2: claim ... -> [paper_id_c]
```

## Citation guidance

- Prefer `paper_id` and local filename first.
- If `arxiv_id` exists, include it in candidate citation output.
- Do not invent references. If missing, state missing evidence explicitly.

## Guardrails

- Do not claim reproduction success without explicit run evidence.
- Distinguish repository metadata from verified experimental outcomes.
- Keep legal boundaries clear: users must comply with third-party licenses.

## Suggested helper files

- `references/output_templates.md`
- `references/task_taxonomy.md`
- `scripts/make_citation_candidates.py`

