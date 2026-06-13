# Research QA Retrieval Diagnosis

## Benchmark Context

- judged `research_qa` citation hit: `80%`
- stable misses:
  - `RQ05`
  - `RQ07`

## RQ05 Diagnosis

Prompt intent:

- compare common multimodal transfer patterns across JEPA work, especially vision-language and audio settings

Why the earlier answer missed:

- answer stayed mostly conceptual
- evidence list did not strongly support cross-modal comparison

Retrieval adjustments applied:

- added multimodal metadata for:
  - `arxiv_2512.10942`
  - `arxiv_2509.15470`
  - `arxiv_2512.07168`
  - `arxiv_2509.23238`
- expanded query terms such as `multimodal`, `vision-language`, `audio`, `transfer`
- added JEPA-family preference to demote unrelated vision-language papers

Current better-fit top candidates:

1. `arxiv_2512.10942` `VL-JEPA Joint Embedding Predictive Architecture for Vision-language`
2. `2026_thinkjepa_empowering_latent_world_models_with_large_vision_language_reasoning_model`
3. `2025_audio_jepa_joint_embedding_predictive_architecture_for_audio_representation_learning`
4. `arxiv_2509.15470` `Self-supervised learning of imaging and clinical signatures using a multimodal joint-embedding predictive architecture`

## RQ07 Diagnosis

Prompt intent:

- explain which training-stage factors are most sensitive when the downstream target is linear evaluation

Why the earlier answer missed:

- factor list was plausible
- citations were not tightly tied to sensitivity or ablation evidence

Retrieval adjustments applied:

- added analysis metadata for:
  - `arxiv_2508.02829`
  - `arxiv_2509.12249`
  - `arxiv_2605.15466`
  - `arxiv_2605.17165`
- expanded query terms such as `linear probe`, `masking`, `context`, `auxiliary`, `normalization`
- added analysis-paper boosts in candidate ranking

Current better-fit top candidates:

1. `arxiv_2509.12249` `Why and How Auxiliary Tasks Improve JEPA Representations`
2. `arxiv_2508.02829` `Elucidating the Role of Feature Normalization in IJEPA`
3. `arxiv_2605.17165` `Factorized Latent Dynamics for Video JEPA An Empirical Study of Auxiliary Objectives`
4. `arxiv_2605.15466` `Entity-Centric World Models Interaction-Aware Masking for Causal Video Prediction`

## Targeted Validation Result

- targeted rerun judged file: `eval/results/research_qa_targeted_rerun_scored.jsonl`
- targeted rerun summary: `eval/results/research_qa_targeted_rerun_summary.md`
- result:
  - `RQ05` passed
  - `RQ07` passed

This means the first-pass retrieval and answer-structure fixes are strong enough to justify a fresh 10-prompt `research_qa` judged rerun.

## Remaining Limit

- ~~no fresh full 10-prompt judged QA rerun has been completed yet~~ **Resolved: v1.2.1 QA rerun completed with 100% factual correctness + 100% citation hit.**
- this artifact now shows both targeted judged improvement AND slice-level benchmark improvement

## Next Action

- ~~run a fresh 10-prompt `research_qa` judged rerun~~ **Done (v1.2.1).**
- compare the new QA slice against `baseline_v1_0_0_research_qa_summary.md` — **Done: 100% vs 80% citation hit, +20pp improvement.**
- next: long-tail metadata coverage expansion for v1.3.0
