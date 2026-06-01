# Baseline Responses (RP/DBG/WRT)

## RP01
最小复现 I-JEPA：  
1) 环境：固定 PyTorch/CUDA 版本并记录 seed。  
2) 数据：先用可下载公开子集跑通输入管线。  
3) 训练：从官方或高可信实现的默认配置开始，不先改模型结构。  
4) 验证：先看 loss 曲线稳定，再跑线性评估。  
Evidence: `2023_assran_self_supervised_learning_from_images_with_a_joint_embedding_predictive_architecture_cvpr_2023_paper`, `metadata/code_index.csv`

## RP02
paper->config checklist：  
- 任务定义（视频表征）  
- 输入采样（帧率/clip 长度）  
- masking/context 策略  
- encoder/predictor 维度  
- optimizer/lr/warmup/wd  
- eval protocol（线性探测或下游任务）  
Evidence: `2025_v_jepa_2_self_supervised_video_models_enable_understanding_prediction_and_planning`, `2026_v_jepa2_1_unlocking_dense_features_in_video`

## RP03
2x24GB 复现建议：  
- 降 batch，用梯度累积补有效 batch。  
- 先缩短 clip 或降分辨率，再恢复。  
- 开 mixed precision。  
- 固定同一评测协议保持可比性。  
Evidence: `2025_v_jepa_2_self_supervised_video_models_enable_understanding_prediction_and_planning`

## RP04
最小消融矩阵（示例）：  
1) baseline  
2) 改 masking 比例  
3) 改 predictor 宽度  
4) 加/不加表示正则  
指标：线性评估、下游任务、训练稳定性。  
Evidence: `arxiv_2603.20111`, `arxiv_2602.01456`

## RP05
本地 zip 映射流程：  
1) 按 `metadata/code_index.csv` 定位候选 zip。  
2) 解压后搜 `train`, `main`, `config`, `yaml`。  
3) 映射到 `paper_id` 并记录入口命令。  
Evidence: `metadata/code_index.csv`, `metadata/paper_catalog.csv`

## RP06
48 小时冲刺：  
- 0-6h：环境与数据验通  
- 6-18h：baseline 训练跑通  
- 18-30h：第一次评测  
- 30-42h：单因素调参  
- 42-48h：整理结果与证据索引  
Evidence: `metadata/eval_protocol_template.md`

## RP07
公平对比原则：  
- 同数据划分  
- 同训练预算  
- 同评测协议  
- 报告方差与多次 seed  
Evidence: `metadata/eval_protocol_template.md`, `2023_assran_self_supervised_learning_from_images_with_a_joint_embedding_predictive_architecture_cvpr_2023_paper`

## RP08
复现前风险清单（优先级）：  
P0: 依赖版本冲突  
P0: 数据 schema 不匹配  
P1: 显存预算不足  
P1: 评测脚本与论文协议偏差  
Evidence: `metadata/eval_protocol_template.md`, `metadata/code_index.csv`

## RP09
适合新手复现的 5 篇（示例）：  
1) I-JEPA 2023（基础路线清晰）  
2) V-JEPA2 2025（视频主线）  
3) Audio-JEPA 2025（跨模态对照）  
4) AMI 2022（方法框架）  
5) MC-JEPA 2023（motion/content 思路）  
Evidence: `2023_assran_self_supervised_learning_from_images_with_a_joint_embedding_predictive_architecture_cvpr_2023_paper`, `2025_v_jepa_2_self_supervised_video_models_enable_understanding_prediction_and_planning`, `2025_audio_jepa_joint_embedding_predictive_architecture_for_audio_representation_learning`, `2022_a_path_towards_autonomous_machine_intelligence`, `2023_mc_jepa_a_joint_embedding_predictive_architecture_for_self_supervised_learning_of_motion_and_content_features`

## RP10
训练到证据沉淀模板：  
- run_id / commit / config hash  
- train/eval 命令  
- 指标曲线与最佳 checkpoint  
- 失败症状->修复动作->复测结果  
Evidence: `metadata/evidence_index_template.csv`, `metadata/eval_protocol_template.md`

## DBG01
OOM 排查顺序：  
1) 降 batch / clip / 分辨率  
2) 开 AMP  
3) 梯度累积  
4) 检查 dataloader 预取与缓存  
Verify: 逐项记录 max memory。  
Evidence: `metadata/eval_protocol_template.md`

## DBG02
loss 震荡：  
优先查 lr、warmup、wd；再查 augment 强度；最后查 batch norm 与分布式同步。  
Verify: 固定 seed 做单变量实验。  
Evidence: `2023_assran_self_supervised_learning_from_images_with_a_joint_embedding_predictive_architecture_cvpr_2023_paper`

## DBG03
shape mismatch：先统一 encoder 输出维度与 predictor 输入维度；检查 projection head 配置。  
Verify: 打印关键 tensor shape。  
Evidence: `metadata/code_index.csv`

## DBG04
预训练 loss 正常但线评低：  
常见是评测协议不一致、特征抽取层不一致、数据预处理偏差。  
Evidence: `metadata/eval_protocol_template.md`

## DBG05
多卡不稳：  
统一 seed、开启确定性设置、核对 all-reduce/bn 同步、检查每卡 batch 是否过小。  
Evidence: `metadata/eval_protocol_template.md`

## DBG06
GPU 利用率低：  
先看 dataloader（num_workers/pin_memory），再看 IO 瓶颈，再看过小模型导致算力吃不满。  
Evidence: `metadata/eval_protocol_template.md`

## DBG07
表示塌陷：  
先查 masking/context 是否过易；再查正则和 predictor；必要时提高目标多样性。  
Evidence: `arxiv_2602.01456`, `arxiv_2509.12249`

## DBG08
评测远低于论文：  
优先核对 split、指标定义、checkpoint 选择、特征抽取层。  
Evidence: `metadata/eval_protocol_template.md`

## DBG09
增强导致不稳：  
最小回退：一次只回退一项增强，保留其余不变，比较 2-3 组短跑曲线。  
Evidence: `2023_assran_self_supervised_learning_from_images_with_a_joint_embedding_predictive_architecture_cvpr_2023_paper`

## DBG10
双机结果差异：  
对齐 driver/CUDA/cuDNN/PyTorch、数据版本、随机种子、启动命令。  
Evidence: `metadata/eval_protocol_template.md`

## WRT01
JEPA 背景引言（示例）：  
“近年来，自监督学习从对比式与重建式两条主线并行发展。JEPA 路线强调在潜空间中预测语义相关表征，而非逐像素重建，从而更贴近下游理解任务的表示需求 [C1]。在图像和视频场景中，该范式展现出较强扩展性，并逐步连接到 world model 与规划问题 [C2][C3]。”  
Claims: C1->`2023_assran_self_supervised_learning_from_images_with_a_joint_embedding_predictive_architecture_cvpr_2023_paper`; C2->`2025_v_jepa_2_self_supervised_video_models_enable_understanding_prediction_and_planning`; C3->`arxiv_2601.00844`

## WRT02
Related work 结构：  
- 对比式 SSL：依赖样本关系学习判别表示。  
- 重建式 SSL：强调输入重构。  
- JEPA：强调预测语义表征，减少对像素重建依赖。  
Evidence: `2020_neurips_2020_bootstrap_your_own_latent_a_new_approach_to_self_supervised_learning_paper_pdf`, `2023_assran_self_supervised_learning_from_images_with_a_joint_embedding_predictive_architecture_cvpr_2023_paper`

## WRT03
Video world model 动机：  
JEPA 在时空上下文中学习可预测潜变量，可更自然地连接动作条件规划与长期预测。  
Evidence: `2025_v_jepa_2_self_supervised_video_models_enable_understanding_prediction_and_planning`, `arxiv_2601.00844`, `arxiv_2605.25313`

## WRT04
8 篇必引（用途）：  
AMI 2022（方法愿景）、I-JEPA 2023（图像基线）、V-JEPA2 2025（视频主线）、Audio-JEPA 2025（音频扩展）、LeJEPA（稳定/可扩展）、Rectified LpJEPA（表示约束）、Var-JEPA（概率化）、Value-guided WM（规划接口）。  
Evidence: 对应 `paper_id` 列表见 `metadata/paper_catalog.csv`

## WRT05
Claim 拆分：  
1) JEPA 已扩展到多模态任务。  
2) 不同模态共享“潜空间预测”训练范式。  
3) 多模态扩展仍面临统一评测不足。  
Evidence: `2025_audio_jepa_joint_embedding_predictive_architecture_for_audio_representation_learning`, `arxiv_2512.10942`, `arxiv_2512.07168`

## WRT06
局限性讨论：  
1) 训练稳定性依赖 masking/context 超参 [C1]。  
2) 跨任务评测协议尚不统一 [C2]。  
3) world-model 闭环验证仍不足 [C3]。  
Claims: C1->`arxiv_2602.01456`; C2->`metadata/eval_protocol_template.md`; C3->`arxiv_2605.25313`

## WRT07
Proposal related-work 框架：  
1) JEPA 基础范式  
2) 视频与世界模型扩展  
3) 稳定性与概率建模变体  
4) 现实部署与评测缺口  
Evidence: `2022_a_path_towards_autonomous_machine_intelligence`, `2025_v_jepa_2_self_supervised_video_models_enable_understanding_prediction_and_planning`, `arxiv_2603.20111`, `arxiv_2602.01456`

## WRT08
综述摘要（示例）：  
JEPA 研究已从图像自监督扩展到视频、音频与多模态场景，并逐步与 world model 规划任务对接。近期工作通过变分化、因果化和结构正则强化稳定性与可解释性，但跨数据集复现与统一基准评测仍是主要瓶颈。  
Evidence: `2023_assran_self_supervised_learning_from_images_with_a_joint_embedding_predictive_architecture_cvpr_2023_paper`, `2025_v_jepa_2_self_supervised_video_models_enable_understanding_prediction_and_planning`, `2025_audio_jepa_joint_embedding_predictive_architecture_for_audio_representation_learning`, `arxiv_2512.10942`, `arxiv_2603.20111`

## WRT09
“JEPA 不是简单生成模型替代”的论证：  
JEPA 的核心目标是学习可预测的抽象表征，重点在语义结构建模与下游可迁移表示，而非直接最大化像素生成质量；它与生成模型在目标函数和评估重点上不同，但可互补。  
Evidence: `2022_a_path_towards_autonomous_machine_intelligence`, `arxiv_2603.20111`

## WRT10
主张配引用（masking 决定迁移上限）：  
建议把原句改为“masking/context 设计显著影响 JEPA 表征迁移性能”，更稳健。  
Citation candidates: `2023_assran_self_supervised_learning_from_images_with_a_joint_embedding_predictive_architecture_cvpr_2023_paper`, `2025_v_jepa_2_self_supervised_video_models_enable_understanding_prediction_and_planning`, `arxiv_2508.02829`, `arxiv_2509.12249`
