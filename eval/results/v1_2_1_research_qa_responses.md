# Research QA Full Rerun Responses (v1.2.1)

## RQ01

Conclusion: I-JEPA 预测静态图像中被遮挡区域的高层语义表征，而 V-JEPA 预测视频时空上下文中的未来或被遮挡时空区域表征。V-JEPA 在视频理解中更常见，因为它将时序一致性和动态结构直接纳入预训练目标。

Key differences:
- I-JEPA：单帧图像，空间 masking，预测被遮挡 patch 的潜表征
- V-JEPA：视频片段，时空 masking，预测未来或被遮挡时空块的潜表征
- V-JEPA 天然编码运动、动作和场景变化信息，对动作识别、时序定位等下游任务更直接

Practical implication:
- 静态图像任务（分类、检测）优先 I-JEPA 系预训练
- 视频任务（动作识别、时序检测、视频 world model）优先 V-JEPA 系

Claims:
- C1: I-JEPA 的核心预测对象是图像中被遮挡区域的高层语义表征，V-JEPA 的核心预测对象是视频时空块的潜表征
- C2: V-JEPA 将时序一致性纳入预训练，使其在视频理解下游任务上更直接有效
- C3: V-JEPA 系方法已从 V-JEPA 演进到 V-JEPA-2 / V-JEPA2.1，持续提升密集特征质量

Evidence:
- E1 (paper): E0004 2023_assran_self_supervised_learning_from_images_with_a_joint_embedding_predictive_architecture_cvpr_2023_paper
- E2 (paper): E0007 2025_v_jepa_2_self_supervised_video_models_enable_understanding_prediction_and_planning
- E3 (paper): E0011 2026_v_jepa2_1_unlocking_dense_features_in_video

Mapping:
- C1 -> E1,E2
- C2 -> E2
- C3 -> E2,E3

Confidence: high

---

## RQ02

Conclusion: JEPA 相比重建式自监督的核心优势在于预测语义表征而非像素细节，使其学到的表示更贴近下游任务需求；但其典型局限在于对 masking 设计、目标表征稳定性和评测协议的高度敏感。

Key differences (优势):
1. 语义级预测目标：JEPA 在潜空间中预测被遮挡区域的表征，避免了对高频纹理重建的依赖，学到的表示更具有语义判别力
2. 天然衔接 world model 与规划：潜空间预测范式可直接扩展到时序预测、规划和决策任务
3. 弱化像素级重建偏差：不追求像素完美重建，降低了"重建好看但语义弱"的风险

Key differences (局限):
1. 目标表征设计敏感：encoder/target 网络架构和更新策略对训练稳定性影响大
2. Masking/context 设计依赖强：预测目标由 masking 策略定义，不同策略导致显著性能差异
3. 评测协议不统一：线性评估、微调、少样本评测等协议差异导致复现和比较困难

Claims:
- C1: JEPA 的语义级预测目标优于像素级重建，产生更具判别力的表示
- C2: JEPA 的潜空间预测范式天然可扩展到 world model 和规划场景
- C3: JEPA 训练对 masking 策略、表征稳定机制和评测协议高度敏感

Evidence:
- E1 (paper): E0002 2020_neurips_2020_bootstrap_your_own_latent_a_new_approach_to_self_supervised_learning_paper_pdf
- E2 (paper): E0004 2023_assran_self_supervised_learning_from_images_with_a_joint_embedding_predictive_architecture_cvpr_2023_paper
- E3 (paper): E0003 2022_a_path_towards_autonomous_machine_intelligence
- E4 (paper): arxiv_2508.02829 Elucidating the Role of Feature Normalization in IJEPA
- E5 (paper): arxiv_2509.12249 Why and How Auxiliary Tasks Improve JEPA Representations

Mapping:
- C1 -> E2,E3
- C2 -> E2,E3
- C3 -> E4,E5

Confidence: high

---

## RQ03

Conclusion: JEPA 在 world model 方向的演进可分为三个阶段：概念奠基期（AMI 路线提出预测式表征）、方法扩展期（I-JEPA/V-JEPA 到潜空间动力学建模）、深化变体期（variational/causal/subspace/entropy 变体强化不确定性建模与规划接口）。

Key timeline:
- 早期（2022-2023）：AMI 白皮书提出"预测抽象表示而非像素"的核心哲学；I-JEPA 在图像域验证了 JEPA 范式的可行性
- 中期（2024-2025）：V-JEPA 将范式扩展到视频时空域；MC-JEPA 处理运动与内容分离；JEPA 开始在 world model 场景中被视为可行的潜空间建模方案
- 近期（2025-2026）：出现多样化建模变体——Var-JEPA（变分概率建模）、Rectified LpJEPA（稀疏与最大熵约束）、seq-JEPA（自回归不变-等变 world model）、ThinkJEPA（结合 VLM 推理的潜 world model）；基于 JEPA world model 的规划方法（如 value-guided planning）开始出现

Claims:
- C1: JEPA world model 路线从 AMI 的概念框架起步，经 I-JEPA/V-JEPA 验证后进入多样化变体阶段
- C2: 2025-2026 年的变体聚焦于概率建模（Var-JEPA）、表示几何控制（Rectified LpJEPA）和规划接口（value-guided planning）
- C3: ThinkJEPA 代表了将大型视觉语言模型推理能力与 JEPA 潜 world model 结合的新方向

Evidence:
- E1 (paper): E0003 2022_a_path_towards_autonomous_machine_intelligence
- E2 (paper): E0004 2023_assran_self_supervised_learning_from_images_with_a_joint_embedding_predictive_architecture_cvpr_2023_paper
- E3 (paper): E0007 2025_v_jepa_2_self_supervised_video_models_enable_understanding_prediction_and_planning
- E4 (paper): E0009 2026_rectified_lpjepa_joint_embedding_predictive_architectures_with_sparse_and_maximum_entropy_representations
- E5 (paper): E0010 2026_thinkjepa_empowering_latent_world_models_with_large_vision_language_reasoning_model
- E6 (paper): E0008 2026_parallel_stochastic_gradient_based_planning_for_world_models
- E7 (paper): arxiv_2601.14354 VJEPA Variational Joint Embedding Predictive Architectures as Probabilistic World Models
- E8 (paper): arxiv_2505.03176 seq-JEPA Autoregressive Predictive Learning of Invariant-Equivariant World Models

Mapping:
- C1 -> E1,E2,E3
- C2 -> E4,E6,E7
- C3 -> E5

Confidence: high

---

## RQ04

Conclusion: LeJEPA 的核心差异在于追求可证明和可扩展的训练范式以减少启发式依赖；Rectified LpJEPA 通过稀疏与最大熵约束控制表示几何与训练稳定性；Var-JEPA 显式引入变分推断，将 JEPA 扩展为概率 world model。

Key differences:
- LeJEPA：强调理论保证，目标是减少对经验启发式（如特定 EMA 策略、projection 维度选择）的依赖，提供更可扩展的训练路径
- Rectified LpJEPA：在 Lp 范数空间中引入稀疏约束和最大熵正则，直接控制表示的几何特性（稀疏度、均匀性），增强训练稳定性和表示质量
- Var-JEPA：将确定性预测扩展为概率预测，在潜空间中建模不确定性，使 JEPA 范式能处理随机动态和部分可观测场景，连接预测式学习与生成式建模

Practical implication:
- 追求训练可复现性和理论理解 → 关注 LeJEPA 方向
- 需要控制表示坍塌或提升线性评估性能 → 关注 Rectified LpJEPA 的约束机制
- 需要不确定量化或概率规划 → 关注 Var-JEPA 的变分扩展

Claims:
- C1: LeJEPA 追求可证明的训练范式，减少对经验启发式的依赖
- C2: Rectified LpJEPA 通过稀疏和最大熵约束直接控制表示几何
- C3: Var-JEPA 显式引入变分推断进行概率建模，区别于确定性 JEPA 变体

Evidence:
- E1 (paper): arxiv_2511.08544 LeJEPA Provable and Scalable Self-Supervised Learning Without the Heuristics
- E2 (paper): E0009 2026_rectified_lpjepa_joint_embedding_predictive_architectures_with_sparse_and_maximum_entropy_representations
- E3 (paper): arxiv_2601.14354 VJEPA Variational Joint Embedding Predictive Architectures as Probabilistic World Models

Mapping:
- C1 -> E1
- C2 -> E2
- C3 -> E3

Confidence: medium

---

## RQ05

Conclusion: JEPA 在多模态（视觉-语言/音频）上的迁移共性不是简单的"都能做联合表征"，而是更具体地体现在三点：都围绕语义级潜空间预测而非逐模态重建、都依赖结构化上下文到目标的预测以保留跨模态可迁移语义、都遵循共享 backbone 加轻量任务头的迁移范式。

Key commonalities:
1. **预测目标统一为语义表征**：无论是视觉-语言方向的 VL-JEPA，还是音频方向的 Audio-JEPA 和 WavJEPA，核心目标都是在潜空间中预测语义一致的表征，而不是逐模态重建细节（如波形或像素）。这使不同模态学到的表示在语义层面更容易对齐。
2. **结构化上下文到目标的预测**：跨视觉-语言、音频、临床多模态的工作都依赖 masking/context 设计来定义"从什么上下文预测什么目标"，迫使模型保留与下游任务相关的语义信息而非单模态局部统计。
3. **共享 backbone + 轻量任务头**：下游迁移通常围绕预训练共享 backbone 展开，再按具体任务添加轻量适配头。视觉-语言、音频、临床多模态这几条线虽然数据形态不同，但都走"共享表示先成型，再做任务适配"的路线。

Current limitation: 现有证据更能说明 JEPA 已经扩展到 vision-language、audio、clinical multimodal 等方向，但对"哪一种跨模态迁移最稳定、最省标注、最抗域偏移"的统一对照证据还不够强。

Claims:
- C1: JEPA 多模态变体都围绕语义级潜空间预测展开，而不是逐模态重建
- C2: 结构化上下文到目标的预测是跨模态迁移共性的核心机制
- C3: 共享 backbone 加轻量任务头是多模态 JEPA 的通用迁移范式
- C4: 跨模态迁移的统一对照证据（稳定性、标注效率、域偏移鲁棒性）仍然薄弱

Evidence:
- E1 (paper): arxiv_2512.10942 VL-JEPA Joint Embedding Predictive Architecture for Vision-language
- E2 (paper): E0006 2025_audio_jepa_joint_embedding_predictive_architecture_for_audio_representation_learning
- E3 (paper): arxiv_2512.07168 JEPA as a Neural Tokenizer Learning Robust Speech Representations with Density Adaptive Attention
- E4 (paper): arxiv_2509.15470 Self-supervised learning of imaging and clinical signatures using a multimodal joint-embedding predictive architecture
- E5 (paper): arxiv_2509.23238 WavJEPA Semantic learning unlocks robust audio foundation models for raw waveforms

Mapping:
- C1 -> E1,E2,E5
- C2 -> E1,E2,E3
- C3 -> E1,E2,E4
- C4 -> missing_evidence (no unified cross-modal transfer benchmark yet)

Confidence: medium

---

## RQ06

Conclusion: JEPA 论文强调 masking/context 设计的根本原因是：预测目标本身由"看到什么上下文、遮住什么目标"直接定义，masking 策略不是普通的数据增强，而是训练目标函数的结构性组成部分。

Key reasons:
1. **Masking 定义预测任务本身**：在 JEPA 框架中，模型从可见的 context block 预测被 mask 的 target block 的表征。masking 的空间范围、比例、策略（随机/块状/时序）直接决定了模型需要学习什么样的不变性和等变性。
2. **控制表示质量与坍塌风险**：不同 masking 策略显著影响训练稳定性和学到的表示质量。过于简单的 masking 导致平凡解，过于困难的 masking 导致训练发散。I-JEPA 的多块 masking 和 V-JEPA 的时空 masking 都是经过仔细设计的。
3. **决定下游迁移性能**：masking/context 设计会影响模型保留的是局部纹理还是全局语义。例如，大范围空间 masking 迫使模型学习更全局的语义，而时序 masking 决定视频模型学到的是静态外观还是动态信息。
4. **特征归一化与 masking 的交互**：近期分析工作（如 IJEPA 特征归一化研究）表明 masking 策略与特征归一化机制之间存在重要交互，共同影响表示的线性可分性。

Claims:
- C1: Masking/context 设计是 JEPA 训练目标的结构性组成，而非简单数据增强
- C2: Masking 策略直接影响表示的不变性/等变性类型和训练稳定性
- C3: 大范围 masking 促进全局语义学习，时序 masking 决定视频模型的动态信息捕获
- C4: Masking 设计与特征归一化机制存在重要交互，共同影响下游线性评估性能

Evidence:
- E1 (paper): E0004 2023_assran_self_supervised_learning_from_images_with_a_joint_embedding_predictive_architecture_cvpr_2023_paper
- E2 (paper): E0007 2025_v_jepa_2_self_supervised_video_models_enable_understanding_prediction_and_planning
- E3 (paper): arxiv_2508.02829 Elucidating the Role of Feature Normalization in IJEPA
- E4 (paper): arxiv_2605.15466 Entity-Centric World Models Interaction-Aware Masking for Causal Video Prediction

Mapping:
- C1 -> E1,E2
- C2 -> E1,E2
- C3 -> E1,E2
- C4 -> E3

Confidence: high

---

## RQ07

Conclusion: 如果目标是下游线性评估，JEPA 训练阶段最敏感的因素不是单一超参，而是四类会直接改变表示几何的设计：masking/context 策略、表征稳定化机制、辅助目标引入方式、以及优化设置与评测协议的解耦。实践中建议按 masking → normalization → auxiliary objectives 的优先级单因素扫描。

Sensitive factors (ranked by impact):

1. **Masking/context 设计（最敏感）**：目标块难度、上下文覆盖范围、是否保留足够全局语义，直接决定模型学到稳定语义还是局部捷径。I-JEPA 系方法和后续 masking 相关工作（如 Entity-Centric Masking）都证明 masking 策略是影响表示质量的第一要素。

2. **表征稳定化机制**：feature normalization、方差约束等稳定化手段直接影响线性可分性。`Elucidating the Role of Feature Normalization in IJEPA` 提供了直接证据：归一化层的选择和放置位置对线性评估性能有显著影响。

3. **辅助目标的引入方式**：`Why and How Auxiliary Tasks Improve JEPA Representations` 和视频 JEPA 的 auxiliary-objective 研究（Factorized Latent Dynamics）表明辅助目标可能明显改变表征质量，但如果加法不当也可能带偏优化目标。

4. **优化设置与评测协议解耦**：当学习率、weight decay、warmup、数据增强与线性评估协议同时变化时，容易将"训练更好"误判为"表示更好"。实践中应先固定评测协议，再单因素扫描上述因素。

Claims:
- C1: Masking/context 设计是影响线性评估性能最敏感的第一要素
- C2: Feature normalization 机制直接影响表示线性可分性，有专门的分析证据
- C3: 辅助目标可改善表征但引入方式不当可能带偏优化目标
- C4: 优化设置须与评测协议解耦，否则容易误判表示质量

Evidence:
- E1 (paper): arxiv_2508.02829 Elucidating the Role of Feature Normalization in IJEPA
- E2 (paper): arxiv_2509.12249 Why and How Auxiliary Tasks Improve JEPA Representations
- E3 (paper): arxiv_2605.17165 Factorized Latent Dynamics for Video JEPA An Empirical Study of Auxiliary Objectives
- E4 (paper): arxiv_2605.15466 Entity-Centric World Models Interaction-Aware Masking for Causal Video Prediction
- E5 (paper): E0004 2023_assran_self_supervised_learning_from_images_with_a_joint_embedding_predictive_architecture_cvpr_2023_paper

Mapping:
- C1 -> E4,E5
- C2 -> E1
- C3 -> E2,E3
- C4 -> E1,E2

Confidence: high

---

## RQ08

Conclusion: JEPA 与 BYOL/SimCLR 的方法哲学差异体现在三个层面：训练目标（预测 vs 对比/对齐）、负样本依赖（无需负样本 vs 依赖负样本/BatchNorm）、以及范式延展方向（world model 衔接 vs 实例判别）。

Key philosophical differences:
- **SimCLR**：显式正负对比学习，通过拉近正样本对、推远负样本对来学习判别性表示。核心哲学是"实例判别"——每个样本都是自己的类别。缺点是依赖大 batch 和负样本质量。
- **BYOL**：不使用负样本，通过 online-target 双网络 + 动量更新避免表示坍塌。核心哲学是"自预测一致性"——从当前视图预测另一视图的表征，本质上更接近 JEPA 的思路但在像素/增强空间操作。
- **JEPA**：在潜空间中从上下文预测目标表征，核心哲学是"语义预测"——不是预测像素或对齐增强视图，而是预测被遮挡区域的语义表征。BYOL 可以看作 JEPA 在"两个增强视图"这种特定 masking 下的特例，但 JEPA 将范式扩展到更一般的时空预测和 world model 场景。

Key distinction: JEPA 的天然延展方向是 world model 与规划（潜空间预测→时序预测→动作条件预测→规划），而 BYOL/SimCLR 的天然延展是更强的感知表示。

Claims:
- C1: SimCLR 依赖显式正负对比进行实例判别，JEPA 依赖潜空间语义预测
- C2: BYOL 通过动量双网络避免坍塌，在"增强视图预测"上与 JEPA 思路相似但操作空间不同
- C3: JEPA 的范式天然可扩展到 world model 与规划，这是 BYOL/SimCLR 不具备的延展方向

Evidence:
- E1 (paper): E0002 2020_neurips_2020_bootstrap_your_own_latent_a_new_approach_to_self_supervised_learning_paper_pdf
- E2 (paper): E0004 2023_assran_self_supervised_learning_from_images_with_a_joint_embedding_predictive_architecture_cvpr_2023_paper
- E3 (paper): E0003 2022_a_path_towards_autonomous_machine_intelligence

Mapping:
- C1 -> E2
- C2 -> E1,E2
- C3 -> E2,E3

Confidence: high

---

## RQ09

Conclusion (组会 5 分钟汇报版): JEPA 研究现状可概括为四个关键点：主线确立、应用扩展、方法深化、挑战待解。

Structured summary:

**1. 主线确立（What is JEPA）**
- 从 LeCun AMI 路线图到 I-JEPA (CVPR 2023)，核心范式确立：从上下文预测被遮挡目标的潜表征，而非重建像素
- 这一范式在图像、视频、音频等多个模态得到验证

**2. 应用扩展（Where is it going）**
- 视频：V-JEPA → V-JEPA-2 → V-JEPA2.1，从表示学习到 video generation reward signal
- 音频：Audio-JEPA、WavJEPA、JEPA as Neural Tokenizer（语音）
- 多模态：VL-JEPA（视觉-语言）、临床多模态 JEPA（医学影像+临床数据）
- 行业场景：自动驾驶（LiDAR JEPA）、推荐系统（JEPA4Rec）、图学习（Predict-Cluster-Refine）

**3. 方法深化（How is it improving）**
- 概率建模：Var-JEPA（变分）、Rectified LpJEPA（稀疏+最大熵）
- 训练稳定性：特征归一化分析、辅助目标消融研究
- World model 接口：ThinkJEPA（+VLM 推理）、value-guided planning

**4. 挑战待解（What's missing）**
- 复现协议与统一评测基准仍不成熟
- 跨模态迁移的系统性对照证据不足
- 长时规划闭环验证（非仅离线指标）

Claims:
- C1: JEPA 核心范式（潜空间语义预测）已在图像/视频/音频/多模态得到广泛验证
- C2: 方法深化方向集中在概率建模、训练稳定性和 world model 规划接口
- C3: 复现协议、统一评测和长时闭环验证仍是主要短板

Evidence:
- E1 (paper): E0003 2022_a_path_towards_autonomous_machine_intelligence
- E2 (paper): E0004 2023_assran_self_supervised_learning_from_images_with_a_joint_embedding_predictive_architecture_cvpr_2023_paper
- E3 (paper): E0007 2025_v_jepa_2_self_supervised_video_models_enable_understanding_prediction_and_planning
- E4 (paper): E0006 2025_audio_jepa_joint_embedding_predictive_architecture_for_audio_representation_learning
- E5 (paper): arxiv_2512.10942 VL-JEPA Joint Embedding Predictive Architecture for Vision-language
- E6 (paper): arxiv_2601.14354 VJEPA Variational Joint Embedding Predictive Architectures as Probabilistic World Models
- E7 (paper): E0010 2026_thinkjepa_empowering_latent_world_models_with_large_vision_language_reasoning_model

Mapping:
- C1 -> E1,E2,E3,E4,E5
- C2 -> E6,E7
- C3 -> missing_evidence (systematic reproduction/eval benchmark not yet established)

Confidence: high

---

## RQ10

Conclusion: JEPA 在视频理解、音频/语音、多模态（V-L/临床）和行业垂直场景四个方向出现了快速扩展；但跨数据集复现一致性、与强生成式方法的公平比较、以及长时闭环规划验证三个方向的证据仍然薄弱。

Rapid expansion areas:
1. **视频理解与 video world model**：V-JEPA 系列持续演进，从表示学习扩展到 video generation reward signal 和物理感知视频生成
2. **音频与语音表征**：Audio-JEPA、WavJEPA、JEPA as Neural Tokenizer 覆盖了从通用音频到语音识别的场景
3. **多模态融合**：VL-JEPA（视觉-语言对齐）、临床多模态 JEPA（影像+临床数据融合）、CrossJEPA（2D→3D 跨模态）
4. **行业垂直场景**：自动驾驶（LiDAR JEPA、Drive-JEPA）、推荐系统（JEPA4Rec）、图学习（Predict-Cluster-Refine）、ECG 医疗信号

Evidence-weak directions:
1. **跨数据集/跨硬件复现一致性**：目前缺乏统一的 JEPA 复现基准和跨 lab 验证报告
2. **与强生成式方法的公平比较**：在统一数据和计算预算下，JEPA vs MAE/BEiT/VideoMAE 等方法的系统性比较不足
3. **长时闭环规划验证**：大多数 JEPA world model 的规划评估停留在离线指标，真实环境闭环验证稀缺

Claims:
- C1: 视频、音频、多模态和行业垂直场景是 JEPA 应用扩展最快的四个方向
- C2: 跨数据集复现一致性和统一评测基准仍然缺失
- C3: 长时闭环规划验证是 JEPA world model 方向最关键的证据缺口

Evidence:
- E1 (paper): E0007 2025_v_jepa_2_self_supervised_video_models_enable_understanding_prediction_and_planning
- E2 (paper): E0006 2025_audio_jepa_joint_embedding_predictive_architecture_for_audio_representation_learning
- E3 (paper): arxiv_2512.10942 VL-JEPA Joint Embedding Predictive Architecture for Vision-language
- E4 (paper): arxiv_2509.15470 Self-supervised learning of imaging and clinical signatures using a multimodal joint-embedding predictive architecture
- E5 (paper): arxiv_2601.00844 Value-guided action planning with JEPA world models
- E6 (paper): arxiv_2601.22032 Drive-JEPA Video JEPA Meets Multimodal Trajectory Distillation for End-to-End Driving
- E7 (paper): arxiv_2512.07168 JEPA as a Neural Tokenizer Learning Robust Speech Representations with Density Adaptive Attention

Mapping:
- C1 -> E1,E2,E3,E4,E6,E7
- C2 -> missing_evidence
- C3 -> missing_evidence

Confidence: medium
