# Baseline Responses (RQ01-RQ10)

## RQ01
I-JEPA 主要在静态图像上做“上下文到目标块”的语义级预测，核心是预测被遮挡区域的高层表征；V-JEPA 则扩展到视频时空上下文，预测未来或被遮挡时空区域的表征，因此更贴合视频理解里“时序+动作+场景变化”的需求。  
V-JEPA 在视频任务更常见的原因是：它把时间一致性和动态结构纳入预训练目标，通常对动作识别、视频检索、时序理解更直接。  
Evidence: `2023_assran_self_supervised_learning_from_images_with_a_joint_embedding_predictive_architecture_cvpr_2023_paper`, `2025_v_jepa_2_self_supervised_video_models_enable_understanding_prediction_and_planning`, `2026_v_jepa2_1_unlocking_dense_features_in_video`

## RQ02
相对重建式自监督，JEPA 的常见优势有三点：  
1) 更关注预测语义表征而非像素细节，目标更贴近下游表示学习。  
2) 通常减少对高频纹理重建的依赖，能弱化“重建好看但语义弱”的问题。  
3) 在 world-model 和规划场景中，潜空间预测更利于接动作与决策模块。  
典型局限也至少三点：  
1) 目标表征设计和稳定训练策略敏感。  
2) 对 masking/context 设计依赖大。  
3) 评测协议不统一时，复现差异会较大。  
Evidence: `2022_a_path_towards_autonomous_machine_intelligence`, `2023_assran_self_supervised_learning_from_images_with_a_joint_embedding_predictive_architecture_cvpr_2023_paper`, `arxiv_2603.20111`, `arxiv_2602.01456`

## RQ03
JEPA 在 world model 的主线可概括为：  
早期：提出“预测抽象表示而非像素重建”的路线（AMI 路线）。  
中期：从图像/视频表征扩展到可用于预测与规划的潜空间动力学。  
近期：出现 variational、causal、subspace 等建模变体，强化不确定性建模、稳定性和规划接口。  
Evidence: `2022_a_path_towards_autonomous_machine_intelligence`, `2025_v_jepa_2_self_supervised_video_models_enable_understanding_prediction_and_planning`, `arxiv_2601.00844`, `arxiv_2602.11389`, `arxiv_2603.20111`, `arxiv_2605.25313`

## RQ04
LeJEPA、Rectified LpJEPA、Var-JEPA 的区别可按“稳定性机制 vs 概率建模”看：  
- LeJEPA：强调更可扩展/更可证明的训练范式，目标是减少启发式依赖。  
- Rectified LpJEPA：引入稀疏与高熵约束，偏向控制表示几何与训练稳定性。  
- Var-JEPA：显式变分化，强化不确定性表达，连接预测式与生成式建模。  
Evidence: `arxiv_2511.08544`, `arxiv_2602.01456`, `arxiv_2603.20111`, `2026_rectified_lpjepa_joint_embedding_predictive_architectures_with_sparse_and_maximum_entropy_representations`

## RQ05
多模态迁移的共性通常是：  
1) 统一潜表征空间：不同模态映射到可对齐语义空间。  
2) 预测式目标替代纯重建：关注跨模态可预测结构。  
3) 下游适配时保留 backbone，轻量头部微调。  
在 JEPA 语境下，音频和视觉-语言工作都体现了“以预测表征为中心”的训练偏好。  
Evidence: `2025_audio_jepa_joint_embedding_predictive_architecture_for_audio_representation_learning`, `arxiv_2512.10942`, `arxiv_2512.07168`

## RQ06
JEPA 强调 masking/context 设计的原因是：预测目标本身由“看见什么上下文、遮住什么目标”定义。  
不同 masking 策略会直接影响：  
1) 学到的 invariance/equivariance 类型；  
2) 训练难度与稳定性；  
3) 下游迁移性能。  
因此它不是普通增强细节，而是目标函数的结构性组成。  
Evidence: `2023_assran_self_supervised_learning_from_images_with_a_joint_embedding_predictive_architecture_cvpr_2023_paper`, `2025_v_jepa_2_self_supervised_video_models_enable_understanding_prediction_and_planning`, `arxiv_2508.02829`, `arxiv_2509.12249`

## RQ07
若目标是线性评估，JEPA 训练里最敏感的通常是：  
1) masking/context 比例与策略；  
2) predictor/head 结构与维度匹配；  
3) 优化超参（学习率、权重衰减、warmup）；  
4) 数据增强强度与时间采样（视频）；  
5) 表征正则（如方差/熵约束）是否合适。  
实践上优先固定评测协议，再单因素扫 masking 与优化器配置。  
Evidence: `2023_assran_self_supervised_learning_from_images_with_a_joint_embedding_predictive_architecture_cvpr_2023_paper`, `2025_v_jepa_2_self_supervised_video_models_enable_understanding_prediction_and_planning`, `arxiv_2602.01456`, `arxiv_2509.12249`

## RQ08
JEPA 与 BYOL/SimCLR 的方法哲学差异：  
- SimCLR：通过显式正负对比学习判别性表示。  
- BYOL：不使用负样本，依赖 teacher-student/动量目标避免塌陷。  
- JEPA：把重点放在“从上下文预测目标表征”，更强调可预测语义结构而非实例判别对齐本身。  
JEPA 的延展优势在于自然衔接 world model 与规划。  
Evidence: `2020_neurips_2020_bootstrap_your_own_latent_a_new_approach_to_self_supervised_learning_paper_pdf`, `2022_a_path_towards_autonomous_machine_intelligence`, `2023_assran_self_supervised_learning_from_images_with_a_joint_embedding_predictive_architecture_cvpr_2023_paper`

## RQ09
JEPA 研究现状（5 分钟组会版）可概括为四点：  
1) 主线确立：从 AMI 到 I-JEPA/V-JEPA，预测式表征学习路线清晰。  
2) 应用扩展：从视觉扩展到音频、视觉语言、医疗与时序场景。  
3) 方法深化：出现 variational/causal/subspace/entropy 等变体，提升稳定性与可规划性。  
4) 现实挑战：复现协议、训练稳定性、跨任务一致评测仍是短板。  
Evidence: `2022_a_path_towards_autonomous_machine_intelligence`, `2023_assran_self_supervised_learning_from_images_with_a_joint_embedding_predictive_architecture_cvpr_2023_paper`, `2025_v_jepa_2_self_supervised_video_models_enable_understanding_prediction_and_planning`, `2025_audio_jepa_joint_embedding_predictive_architecture_for_audio_representation_learning`, `arxiv_2512.10942`, `arxiv_2603.20111`

## RQ10
快速扩展领域：  
1) 视频理解与视频 world model；  
2) 音频与语音表征；  
3) 多模态（V-L、跨传感器）；  
4) 医疗与时序等行业数据。  
证据相对薄弱的方向：  
1) 跨数据集、跨硬件复现一致性报告；  
2) 统一基准下与强生成式方法的公平比较；  
3) 长时规划闭环（不仅离线指标）。  
Evidence: `2025_v_jepa_2_self_supervised_video_models_enable_understanding_prediction_and_planning`, `2025_audio_jepa_joint_embedding_predictive_architecture_for_audio_representation_learning`, `arxiv_2512.10942`, `arxiv_2601.00844`, `arxiv_2605.25313`
