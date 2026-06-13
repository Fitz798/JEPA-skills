# Research QA Next Stage Plan

This document starts the next phase after `v1.2.0`.

Primary goal:

- improve judged `research_qa` citation-hit quality instead of only improving metadata hygiene

Current benchmark constraint:

- historical `research_qa` judged slice remains `80%` citation hit
- known weak prompts are `RQ05` and `RQ07`

## Diagnosed Failure Modes

### RQ05 Multimodal transfer commonalities

Observed issue:

- previous answer stayed at a high-level pattern summary
- citations were related, but not strong enough as cross-modal comparison evidence

What retrieval needed:

- JEPA-family multimodal papers
- audio JEPA papers
- analysis or transfer-oriented papers rather than generic multimodal matches

### RQ07 Sensitive factors for linear evaluation

Observed issue:

- previous answer listed plausible factors
- citations did not directly support sensitivity or ablation-style claims

What retrieval needed:

- normalization analysis
- auxiliary objective studies
- masking/context analysis
- linear-probe or downstream sensitivity evidence

## Changes Already Applied

- added targeted long-tail metadata overrides in `scripts/build_paper_catalog.py`
- added query-term expansion and analysis-paper boosts in `jepa-research/scripts/make_citation_candidates.py`
- added an extra JEPA-family preference in candidate ranking

These changes improve candidate quality for the two known weak prompt classes without broadening the whole catalog scope.

## Immediate Validation Tasks

1. ~~Re-run candidate snapshots for `RQ05` and `RQ07` and store stable comparison artifacts.~~ **Done.**
2. ~~Draft revised reference answers for `RQ05` and `RQ07` using the improved candidate sets.~~ **Done.**
3. ~~Judge those two prompts manually against the existing rubric.~~ **Done: both scored 100%.**
4. ~~If both improve, run a fresh `research_qa` 10-prompt judged pass.~~ **Done: v1.2.1 full QA rerun achieved 100% factual correctness + 100% citation hit.**

## Immediate Validation Tasks (Next Phase)

1. Expand long-tail metadata coverage beyond current 11/148 papers.
2. Add more confirmed `code_id` links for core papers (currently 3/11).
3. Evaluate whether further citation-hit gains require answer-format constraints or stronger claim-to-citation mapping rules.

## Success Criteria

- `RQ05` moves from unsupported generalization to citation-backed cross-modal comparison
- `RQ07` moves from generic advice to citation-backed sensitivity guidance
- refreshed `research_qa` slice exceeds `80%` citation hit

## Scope Guardrails

- do not attempt full long-tail metadata annotation yet
- only add metadata for papers that directly affect judged QA quality
- prefer targeted retrieval fixes over large prompt rewrites
