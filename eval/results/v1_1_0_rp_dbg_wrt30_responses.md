# v1.1.0 Responses (RP/DBG/WRT with Evidence Mapping)

## RP01
Target: I-JEPA minimal runnable reproduction.
Actions:
- A1: Freeze environment and seed.
- A2: Validate dataset pipeline with a small subset.
- A3: Run baseline training config first.
- A4: Run linear evaluation and compare trend, not only final metric.
Evidence:
- E1 (paper): 2023_assran_self_supervised_learning_from_images_with_a_joint_embedding_predictive_architecture_cvpr_2023_paper
- E2 (protocol): metadata/eval_protocol_template.md
- E3 (code): metadata/code_index.csv
Mapping:
- A1 -> E2
- A2 -> E2,E3
- A3 -> E1,E3
- A4 -> E1,E2

## RP02
Paper->config checklist for video representation:
Actions:
- A1: Define task/dataset/split/metric.
- A2: Set clip length + temporal sampling.
- A3: Set masking-context policy.
- A4: Set optimizer/lr/warmup/wd and eval schedule.
Evidence:
- E1 (paper): 2025_v_jepa_2_self_supervised_video_models_enable_understanding_prediction_and_planning
- E2 (paper): 2026_v_jepa2_1_unlocking_dense_features_in_video
- E3 (protocol): metadata/eval_protocol_template.md
Mapping:
- A1 -> E3
- A2 -> E1,E2
- A3 -> E1,E2
- A4 -> E1,E3

## RP03
For 2x24GB GPUs (cost down, comparability kept):
Actions:
- A1: Reduce per-GPU batch and use gradient accumulation.
- A2: Start with lower resolution/shorter clip then restore.
- A3: Enable AMP and activation checkpointing.
- A4: Keep identical eval protocol to baseline.
Evidence:
- E1 (paper): 2025_v_jepa_2_self_supervised_video_models_enable_understanding_prediction_and_planning
- E2 (protocol): metadata/eval_protocol_template.md
Mapping:
- A1 -> E1
- A2 -> E1
- A3 -> E1
- A4 -> E2

## RP04
World-model minimal ablation matrix:
Actions:
- A1: Baseline config.
- A2: Masking ratio ablation.
- A3: Predictor width ablation.
- A4: Representation regularization on/off.
Evidence:
- E1 (paper): arxiv_2603.20111
- E2 (paper): arxiv_2602.01456
- E3 (protocol): metadata/eval_protocol_template.md
Mapping:
- A1 -> E3
- A2 -> E1,E2
- A3 -> E1
- A4 -> E2

## RP05
Map paper method to local zip code:
Actions:
- A1: Select candidate zip via code_index.
- A2: Locate `train/main/config` entrypoints after unzip.
- A3: Build paper->entrypoint mapping table.
- A4: Record exact command and config hash.
Evidence:
- E1 (code): metadata/code_index.csv
- E2 (protocol): metadata/eval_protocol_template.md
- E3 (catalog): metadata/paper_catalog.csv
Mapping:
- A1 -> E1
- A2 -> E1
- A3 -> E1,E3
- A4 -> E2

## RP06
48-hour reproduction sprint:
Actions:
- A1: 0-6h env/data sanity.
- A2: 6-24h first training run.
- A3: 24-36h first eval + error triage.
- A4: 36-48h single-factor tuning + evidence write-up.
Evidence:
- E1 (protocol): metadata/eval_protocol_template.md
- E2 (template): metadata/evidence_index_template.csv
Mapping:
- A1 -> E1
- A2 -> E1
- A3 -> E1
- A4 -> E1,E2

## RP07
Fair JEPA vs contrastive baseline protocol:
Actions:
- A1: Same data split + preprocessing.
- A2: Same training budget (epochs/steps/compute).
- A3: Same downstream evaluation and seeds.
- A4: Report mean/std across runs.
Evidence:
- E1 (paper): 2023_assran_self_supervised_learning_from_images_with_a_joint_embedding_predictive_architecture_cvpr_2023_paper
- E2 (protocol): metadata/eval_protocol_template.md
Mapping:
- A1 -> E2
- A2 -> E2
- A3 -> E2
- A4 -> E1,E2

## RP08
Pre-run risk checklist:
Actions:
- A1: Dependency lock check.
- A2: Data schema/shape check.
- A3: Memory budget dry run.
- A4: Eval protocol consistency check.
Evidence:
- E1 (protocol): metadata/eval_protocol_template.md
- E2 (code): metadata/code_index.csv
Mapping:
- A1 -> E2
- A2 -> E2
- A3 -> E1,E2
- A4 -> E1

## RP09
Five beginner-friendly candidates:
Actions:
- A1: Start with I-JEPA 2023 for core concept.
- A2: Add MC-JEPA for motion/content decomposition.
- A3: Add V-JEPA2 for video pipeline.
- A4: Add Audio-JEPA for modality transfer.
- A5: Keep AMI for conceptual framing.
Evidence:
- E1 (paper): 2023_assran_self_supervised_learning_from_images_with_a_joint_embedding_predictive_architecture_cvpr_2023_paper
- E2 (paper): 2023_mc_jepa_a_joint_embedding_predictive_architecture_for_self_supervised_learning_of_motion_and_content_features
- E3 (paper): 2025_v_jepa_2_self_supervised_video_models_enable_understanding_prediction_and_planning
- E4 (paper): 2025_audio_jepa_joint_embedding_predictive_architecture_for_audio_representation_learning
- E5 (paper): 2022_a_path_towards_autonomous_machine_intelligence
Mapping:
- A1 -> E1
- A2 -> E2
- A3 -> E3
- A4 -> E4
- A5 -> E5

## RP10
Train-to-evidence template:
Actions:
- A1: Save run_id, commit, config hash.
- A2: Save train/eval commands.
- A3: Save best metrics + curve artifact.
- A4: Save symptom->fix->recheck chain.
Evidence:
- E1 (protocol): metadata/eval_protocol_template.md
- E2 (template): metadata/evidence_index_template.csv
Mapping:
- A1 -> E1,E2
- A2 -> E1
- A3 -> E1
- A4 -> E2

## DBG01
OOM troubleshooting order:
Actions:
- A1: Lower batch/clip/resolution.
- A2: Enable AMP.
- A3: Use gradient accumulation.
- A4: Profile dataloader memory overhead.
Evidence:
- E1 (protocol): metadata/eval_protocol_template.md
- E2 (code): metadata/code_index.csv
Mapping:
- A1 -> E1
- A2 -> E1
- A3 -> E1
- A4 -> E1,E2

## DBG02
Loss oscillation:
Actions:
- A1: Re-scan lr/warmup/wd.
- A2: Reduce aggressive augmentations.
- A3: Check distributed sync and BN behavior.
Evidence:
- E1 (paper): 2023_assran_self_supervised_learning_from_images_with_a_joint_embedding_predictive_architecture_cvpr_2023_paper
- E2 (protocol): metadata/eval_protocol_template.md
Mapping:
- A1 -> E1,E2
- A2 -> E1
- A3 -> E2

## DBG03
Shape mismatch `[B,256]` vs `[B,384]`:
Actions:
- A1: Align predictor output dim with target encoder dim.
- A2: Verify projection head config.
- A3: Print tensor shapes at forward boundaries.
Evidence:
- E1 (code): metadata/code_index.csv
- E2 (protocol): metadata/eval_protocol_template.md
Mapping:
- A1 -> E1
- A2 -> E1
- A3 -> E2

## DBG04
Normal pretrain loss but low linear eval:
Actions:
- A1: Verify feature layer used for eval.
- A2: Verify eval split/metric matches protocol.
- A3: Check augmentation mismatch between pretrain/eval.
Evidence:
- E1 (protocol): metadata/eval_protocol_template.md
- E2 (paper): 2023_assran_self_supervised_learning_from_images_with_a_joint_embedding_predictive_architecture_cvpr_2023_paper
Mapping:
- A1 -> E1,E2
- A2 -> E1
- A3 -> E2

## DBG05
Multi-GPU instability:
Actions:
- A1: Fix seeds and deterministic flags.
- A2: Check effective per-GPU batch size.
- A3: Validate sync behavior and grad scaling.
Evidence:
- E1 (protocol): metadata/eval_protocol_template.md
- E2 (code): metadata/code_index.csv
Mapping:
- A1 -> E1
- A2 -> E1
- A3 -> E1,E2

## DBG06
Low GPU utilization:
Actions:
- A1: Tune dataloader workers/pin_memory/prefetch.
- A2: Check storage IO bottleneck.
- A3: Confirm model/sequence length saturates compute.
Evidence:
- E1 (protocol): metadata/eval_protocol_template.md
- E2 (code): metadata/code_index.csv
Mapping:
- A1 -> E2
- A2 -> E1,E2
- A3 -> E1

## DBG07
Representation collapse:
Actions:
- A1: Increase masking difficulty or diversity.
- A2: Re-check regularization/variance constraints.
- A3: Inspect predictor architecture bottleneck.
Evidence:
- E1 (paper): arxiv_2602.01456
- E2 (paper): arxiv_2509.12249
- E3 (protocol): metadata/eval_protocol_template.md
Mapping:
- A1 -> E2
- A2 -> E1
- A3 -> E1,E3

## DBG08
Eval below paper due to protocol mismatch:
Actions:
- A1: Match split/metric exactly.
- A2: Match checkpoint selection rule.
- A3: Match feature extraction layer and preprocessing.
Evidence:
- E1 (protocol): metadata/eval_protocol_template.md
- E2 (paper): 2025_v_jepa_2_self_supervised_video_models_enable_understanding_prediction_and_planning
Mapping:
- A1 -> E1,E2
- A2 -> E1
- A3 -> E1,E2

## DBG09
Augmentation instability (minimal rollback):
Actions:
- A1: Disable one augmentation at a time.
- A2: Run short controlled comparisons.
- A3: Keep best stable subset and re-expand.
Evidence:
- E1 (paper): 2023_assran_self_supervised_learning_from_images_with_a_joint_embedding_predictive_architecture_cvpr_2023_paper
- E2 (protocol): metadata/eval_protocol_template.md
Mapping:
- A1 -> E2
- A2 -> E2
- A3 -> E1,E2

## DBG10
Cross-machine drift:
Actions:
- A1: Align driver/CUDA/cuDNN/PyTorch versions.
- A2: Verify dataset checksum/version.
- A3: Compare launch flags and env vars.
- A4: Run same seed smoke test.
Evidence:
- E1 (protocol): metadata/eval_protocol_template.md
- E2 (code): metadata/code_index.csv
Mapping:
- A1 -> E1
- A2 -> E1
- A3 -> E2
- A4 -> E1

## WRT01
Draft intro (200-300 chars omitted for brevity in eval):
Claims:
- C1: JEPA predicts semantic latent targets rather than full pixel reconstruction.
- C2: JEPA scales from image to video and planning-linked settings.
Evidence:
- E1 (paper): 2023_assran_self_supervised_learning_from_images_with_a_joint_embedding_predictive_architecture_cvpr_2023_paper
- E2 (paper): 2025_v_jepa_2_self_supervised_video_models_enable_understanding_prediction_and_planning
- E3 (paper): arxiv_2601.00844
Mapping:
- C1 -> E1
- C2 -> E2,E3

## WRT02
Related-work framing:
Claims:
- C1: Contrastive SSL emphasizes instance discrimination.
- C2: Reconstruction SSL emphasizes input recovery fidelity.
- C3: JEPA emphasizes predictable semantic latent structure.
Evidence:
- E1 (paper): 2020_neurips_2020_bootstrap_your_own_latent_a_new_approach_to_self_supervised_learning_paper_pdf
- E2 (paper): 2023_assran_self_supervised_learning_from_images_with_a_joint_embedding_predictive_architecture_cvpr_2023_paper
Mapping:
- C1 -> E1
- C2 -> E1
- C3 -> E2

## WRT03
Video world-model motivation:
Claims:
- C1: Temporal predictive latent objectives align with video understanding.
- C2: Latent JEPA models can interface with planning modules.
Evidence:
- E1 (paper): 2025_v_jepa_2_self_supervised_video_models_enable_understanding_prediction_and_planning
- E2 (paper): arxiv_2601.00844
- E3 (paper): arxiv_2605.25313
Mapping:
- C1 -> E1
- C2 -> E2,E3

## WRT04
Eight must-cite papers + usage:
Claims:
- C1: Core conceptual lineage needs AMI + I-JEPA + V-JEPA.
- C2: Stability/probabilistic branch needs LeJEPA/Rectified/Var-JEPA.
- C3: Modality and planning branch needs Audio-JEPA + value-guided WM.
Evidence:
- E1 (paper): 2022_a_path_towards_autonomous_machine_intelligence
- E2 (paper): 2023_assran_self_supervised_learning_from_images_with_a_joint_embedding_predictive_architecture_cvpr_2023_paper
- E3 (paper): 2025_v_jepa_2_self_supervised_video_models_enable_understanding_prediction_and_planning
- E4 (paper): arxiv_2511.08544
- E5 (paper): arxiv_2602.01456
- E6 (paper): arxiv_2603.20111
- E7 (paper): 2025_audio_jepa_joint_embedding_predictive_architecture_for_audio_representation_learning
- E8 (paper): arxiv_2601.00844
Mapping:
- C1 -> E1,E2,E3
- C2 -> E4,E5,E6
- C3 -> E7,E8

## WRT05
Three citable claims for multimodal expansion:
Claims:
- C1: JEPA methods have extended beyond vision into audio.
- C2: JEPA has explicit vision-language variants.
- C3: Cross-modal transfer still needs stronger unified benchmarks.
Evidence:
- E1 (paper): 2025_audio_jepa_joint_embedding_predictive_architecture_for_audio_representation_learning
- E2 (paper): arxiv_2512.10942
- E3 (paper): arxiv_2512.07168
Mapping:
- C1 -> E1
- C2 -> E2
- C3 -> E2,E3

## WRT06
Limitation paragraph with citations:
Claims:
- C1: Stability remains sensitive to objective/regularization design.
- C2: Cross-task protocol consistency is still a bottleneck.
- C3: Closed-loop world-model validation is under-reported.
Evidence:
- E1 (paper): arxiv_2602.01456
- E2 (protocol): metadata/eval_protocol_template.md
- E3 (paper): arxiv_2605.25313
Mapping:
- C1 -> E1
- C2 -> E2
- C3 -> E3

## WRT07
Proposal related-work outline:
Claims:
- C1: JEPA baseline lineages should be separated by modality and objective.
- C2: World-model branch should be discussed as planning interface.
- C3: Stability branch should be discussed as enabler for reproducibility.
Evidence:
- E1 (paper): 2022_a_path_towards_autonomous_machine_intelligence
- E2 (paper): 2025_v_jepa_2_self_supervised_video_models_enable_understanding_prediction_and_planning
- E3 (paper): arxiv_2603.20111
- E4 (paper): arxiv_2602.01456
Mapping:
- C1 -> E1,E2
- C2 -> E2,E3
- C3 -> E4

## WRT08
Survey abstract + 5 traceable references:
Claims:
- C1: JEPA evolved from image representation to video/multimodal settings.
- C2: Recent work pushes probabilistic/causal/stability variants.
- C3: Unified reproducibility standards remain weak.
Evidence:
- E1 (paper): 2023_assran_self_supervised_learning_from_images_with_a_joint_embedding_predictive_architecture_cvpr_2023_paper
- E2 (paper): 2025_v_jepa_2_self_supervised_video_models_enable_understanding_prediction_and_planning
- E3 (paper): 2025_audio_jepa_joint_embedding_predictive_architecture_for_audio_representation_learning
- E4 (paper): arxiv_2512.10942
- E5 (paper): arxiv_2603.20111
Mapping:
- C1 -> E1,E2,E3,E4
- C2 -> E5
- C3 -> E5

## WRT09
Why JEPA is not a simple generative-model replacement:
Claims:
- C1: JEPA optimizes predictive latent semantics rather than pixel likelihood.
- C2: JEPA and generative models are complementary in many pipelines.
Evidence:
- E1 (paper): 2022_a_path_towards_autonomous_machine_intelligence
- E2 (paper): arxiv_2603.20111
Mapping:
- C1 -> E1,E2
- C2 -> E2

## WRT10
Claim rewriting + citation:
Claims:
- C1: Stronger wording should be softened to “masking/context strongly influences transferability.”
- C2: Multiple JEPA works support sensitivity to masking/feature normalization.
Evidence:
- E1 (paper): 2023_assran_self_supervised_learning_from_images_with_a_joint_embedding_predictive_architecture_cvpr_2023_paper
- E2 (paper): 2025_v_jepa_2_self_supervised_video_models_enable_understanding_prediction_and_planning
- E3 (paper): arxiv_2508.02829
- E4 (paper): arxiv_2509.12249
Mapping:
- C1 -> E1,E2
- C2 -> E3,E4
