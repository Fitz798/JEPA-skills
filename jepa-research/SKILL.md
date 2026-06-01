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
- For `reproduction_plan` and `debug_triage`, every major action item must map to at least one evidence ID.

Use one of the following modes based on user intent.

## Evidence binding format (required)

For non-trivial answers, include:

1. **Action/Claim list** with IDs (`A1`, `A2`, ... or `C1`, `C2`, ...).
2. **Evidence table** with IDs (`E1`, `E2`, ...), each with:
   - source type: `paper` | `code` | `protocol` | `log`
   - pointer: paper_id/filename, file path, or log artifact
3. **Mapping line**: `A# -> E#`

If evidence is missing, explicitly mark:

`A# -> missing_evidence`

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

Claims:
- C1: ...
- C2: ...

Evidence:
- E1 (paper): [paper_id] filename
- E2 (paper): [paper_id] filename
Mapping:
- C1 -> E1
- C2 -> E2
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
1. A1 Environment ...
2. A2 Data ...
3. A3 Train command ...
4. A4 Eval command ...

Risk checks:
- ...
- ...

Pass criteria:
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
1. A1 ...
2. A2 ...
3. A3 ...

Verify:
- check 1 ...
- check 2 ...

Evidence:
- E1 (code/protocol): ...
- E2 (paper): ...
Mapping:
- A1 -> E1
- A2 -> E1,E2
- A3 -> E1
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
- C1: claim ... -> E1,E2
- C2: claim ... -> E3

Evidence:
- E1 (paper): [paper_id_a]
- E2 (paper): [paper_id_b]
- E3 (paper): [paper_id_c]
```

## Citation guidance

- Prefer `paper_id` and local filename first.
- If `arxiv_id` exists, include it in candidate citation output.
- Do not invent references. If missing, state missing evidence explicitly.
- For debugging answers, cite at least one `code` or `protocol` evidence item.

## Guardrails

- Do not claim reproduction success without explicit run evidence.
- Distinguish repository metadata from verified experimental outcomes.
- Keep legal boundaries clear: users must comply with third-party licenses.
- Do not present advice-only responses without evidence mapping when user asks for concrete actions.

## Suggested helper files

- `references/output_templates.md`
- `references/task_taxonomy.md`
- `references/evidence_binding_rules.md`
- `scripts/make_citation_candidates.py`
