# v1.3.0 Targeted Fix Responses (RP09, DBG10, WRT04)

## RP09

Conclusion: 从当前 metadata 中选出的 5 篇最适合复现的 JEPA 论文，选择标准基于：(a) 本地有确认的代码存档，(b) 论文方法描述清晰，(c) 有已知的社区实现或可参考的类似实现。

Selection (ordered by reproducibility readiness):

**1. I-JEPA (CVPR 2023)** — 复现就绪度最高
- 代码: `ijepa_main` (exact_local_match, confidence=high)
- 入口: `ijepa-main/src/train.py`
- 理由: 作为 JEPA 范式的奠基性实现，代码量适中，单 GPU 可跑。适合作为理解 JEPA 训练循环的第一站。
- 复现注意: 需要 ImageNet-1K，但可用较小数据集（如 CIFAR-100）验证流程。

**2. MC-JEPA (2023)** — 复现就绪度高
- 代码: `eb_jepa_main` (family_match_only, confidence=medium)
- 入口: `eb_jepa-main/examples/ac_video_jepa/main.py`
- 理由: 同时处理运动和内容特征，比纯 I-JEPA 多一个维度，适合作为扩展练习。代码存档包含示例入口。
- 复现注意: 确认数据格式与代码的 motion/content split 预期一致。

**3. LeJEPA (2025)** — 复现就绪度高
- 代码: `lejepa_main` (family_match_only, confidence=medium)
- 入口: `lejepa-main/README.md` 提供项目级文档
- 理由: 强调可扩展/可证明的训练范式，代码包含完整项目文档。适合理解 JEPA 训练稳定性改进。
- 复现注意: 先按 README 的 quick start 验证环境，再扩展到完整训练。

**4. V-JEPA (via jepa_main)** — 需额外确认
- 代码: `jepa_main` (multiple_local_candidates, confidence=medium)
- 入口: `jepa-main/app/vjepa/train.py`
- 理由: 视频 JEPA 的核心实现候选。代码存档中有 V-JEPA 训练入口，但需确认是否与论文使用的版本完全对应。选它为第四位是因为视频复现的计算成本高于图像，但如果有 GPU 资源，它是视频方向最有价值的复现目标。
- 复现注意: 需要视频数据集（如 Kinetics-400 子集），计算需求明显高于图像方法。

**5. Rectified LpJEPA (2026)** — 无本地代码，但社区资源丰富
- 代码: 无本地存档 (no_known_local_code)
- 理由: 虽然本地没有代码，但该论文的方法描述详细（稀疏+最大熵约束），且基于已知的 JEPA 训练框架构建。选它为第五位是作为"从论文描述自行实现"的进阶挑战，适合已经复现过前 4 篇的实践者。
- 复现注意: 需要先复现基础 JEPA 训练循环，再添加稀疏约束和熵正则。预期难度较高，属于进阶复现目标。

Actions:
- A1: 从 ijepa_main 开始，验证环境/数据/训练流程
- A2: 扩展到 MC-JEPA，对比 motion/content 分解
- A3: 尝试 LeJEPA，验证稳定性改进
- A4: 有 GPU 资源时尝试 V-JEPA 视频管线
- A5: 进阶：基于论文描述实现 Rectified LpJEPA 的稀疏约束

Evidence:
- E1 (paper): E0004 2023_assran_self_supervised_learning_from_images_with_a_joint_embedding_predictive_architecture_cvpr_2023_paper
- E2 (code): E0015 ijepa_main corpus/code/archives/ijepa-main.zip
- E3 (paper): E0005 2023_mc_jepa_a_joint_embedding_predictive_architecture_for_self_supervised_learning_of_motion_and_content_features
- E4 (code): E0013 eb_jepa_main corpus/code/archives/eb_jepa-main.zip
- E5 (code): E0018 lejepa_main corpus/code/archives/lejepa-main.zip
- E6 (code): E0016 jepa_main corpus/code/archives/jepa-main.zip
- E7 (paper): E0009 2026_rectified_lpjepa_joint_embedding_predictive_architectures_with_sparse_and_maximum_entropy_representations

Mapping:
- A1 -> E1,E2
- A2 -> E3,E4
- A3 -> E5
- A4 -> E6
- A5 -> E7

Confidence: high

---

## DBG10

Diagnosis:
- Primary hypothesis (highest probability): NCCL/communication library configuration mismatch across machines — different NCCL versions, NCCL_DEBUG settings, or network interface selection cause non-deterministic all-reduce ordering and gradient divergence.
- Secondary hypothesis: CUDA/cuDNN version differences leading to different floating-point reduction orders in convolution and attention kernels.
- Tertiary hypothesis: Dataset loading differences (different file system caching,不同节点的数据加载顺序差异).

Fix order (ranked by probability × impact):

**Step 1 — Isolate the variance source (smoke test)**
- A1.1: 在单台机器上，固定 seed 跑两次 training（相同 GPU），确认单机 variance 基线。预期 loss curve 几乎完全重合。
- A1.2: 在单台机器上，用两个不同 GPU 各跑一次（相同 seed），确认同机多 GPU variance 基线。

**Step 2 — Check NCCL/distributed configuration**
- A2.1: 在所有机器上运行 `python -c "import torch; print(torch.__version__, torch.cuda.nccl.version())"` 并比较输出。任何版本差异都是高优先级修复项。
- A2.2: 检查关键环境变量一致性：
  - `NCCL_DEBUG=INFO`（启用 NCCL 详细日志）
  - `NCCL_SOCKET_IFNAME`（网络接口选择，多网卡时必须一致）
  - `NCCL_IB_DISABLE`（InfiniBand 环境关键）
  - `CUDA_VISIBLE_DEVICES`（确保每台机器使用相同数量/型号的 GPU）
- A2.3: 确认所有机器使用相同的 PyTorch distributed 后端（`nccl` vs `gloo`）和相同的 `torch.distributed.init_method`。

**Step 3 — Check CUDA/cuDNN determinism**
- A3.1: 在所有机器上设置 `torch.backends.cudnn.deterministic = True` 和 `torch.backends.cudnn.benchmark = False`，重新运行 smoke test。
- A3.2: 如果 variance 消失，说明根因是 cuDNN 自动算法选择在不同 GPU 架构/驱动版本上的差异。逐项放开 benchmark 并监控。

**Step 4 — Check data pipeline**
- A4.1: 验证所有节点上数据集的 checksum (`sha256sum dataset/**/*`)。
- A4.2: 确认 `DistributedSampler` 的 seed 传递正确，每个 epoch 的 partition 一致。
- A4.3: 比较各节点的 data loading 时间分布（`torch.utils.bottleneck` 或简单计时），确认 IO 不是 variance 来源。

Verify:
- 每步修复后，跑 same-seed smoke test（2 台机器 × 2 GPU），确认 loss curve 重合度
- 最终验证：same-seed 3 机 24 GPU full run，loss curve 标准差应 < 1e-3
- 如果仍有 variance，检查硬件层面（GPU 温度降频、电源差异、NVLink 拓扑差异）

Actions:
- A1: Smoke test — isolate single-machine vs cross-machine variance
- A2: NCCL/distributed configuration audit
- A3: CUDA/cuDNN determinism enforcement
- A4: Data pipeline consistency check

Evidence:
- E1 (protocol): E0012 metadata/eval_protocol_template.md
- E2 (code): E0017 jepa_main2 corpus/code/archives/jepa-main2.zip (contains CLI train entrypoint for distributed launch reference)

Mapping:
- A1 -> E1
- A2 -> E1,E2
- A3 -> E1,E2
- A4 -> E1

Confidence: medium (cross-machine determinism is inherently complex; if hardware differences exist, software fixes may not fully resolve)

---

## WRT04

8 篇 JEPA 核心论文按影响力排序，附每篇的具体贡献和用途：

**#1 I-JEPA (Assran et al., CVPR 2023)**
- 贡献: 首次在图像域大规模验证了 JEPA 范式——从上下文预测被遮挡 patch 的潜表征，而非重建像素。奠定了 predict in latent space 的实践路线。
- 用途: 作为 JEPA 入门引用；任何讨论"为什么 JEPA 有效"的场景首选此论文。

**#2 AMI (LeCun, 2022)**
- 贡献: 提出自主机器智能的架构蓝图，明确将 JEPA 定位为世界模型的核心学习范式。概念影响力远超单篇实验论文。
- 用途: 在引言/愿景部分引用，建立 JEPA 工作的哲学动机和长期目标。

**#3 V-JEPA-2 (2025)**
- 贡献: 将 JEPA 从静态图像扩展到视频时空域，证明预测式学习对视频理解/预测/规划都有效。是 JEPA 从 vision 走向 world model 的关键桥梁。
- 用途: 讨论视频自监督学习、world model 预训练、或 JEPA 扩展性时引用。

**#4 Rectified LpJEPA (2026)**
- 贡献: 引入稀疏约束和最大熵正则控制表示几何，系统性地解决了 JEPA 训练中的表示坍塌风险。是 JEPA 稳定性研究的分水岭。
- 用途: 讨论 JEPA 训练稳定性、表示坍塌问题、或正则化设计时引用。

**#5 Var-JEPA (arxiv_2603.20111, 2026)**
- 贡献: 将确定性 JEPA 扩展为变分概率模型，在潜空间中建模不确定性，使 JEPA 能处理随机动态和部分可观测场景。打通了预测式学习与概率建模的边界。
- 用途: 讨论 JEPA 的不确定性量化、概率世界模型、或规划中的随机性时引用。

**#6 BYOL (Grill et al., NeurIPS 2020)**
- 贡献: 虽然不是 JEPA 论文，但其 teacher-student 双网络 + 动量更新 + 无负样本的设计直接启发了 JEPA 的 target encoder 架构。JEPA 可视为 BYOL 在"从上下文预测目标"方向上的推广。
- 用途: 在 related work 中将 JEPA 定位为 BYOL 的继承和扩展，解释方法谱系。

**#7 Audio-JEPA (2025)**
- 贡献: 首次将 JEPA 范式从视觉扩展到音频域，证明预测式潜表征学习在非视觉模态同样有效。开启了 JEPA 的多模态扩展路线。
- 用途: 讨论 JEPA 的跨模态泛化性或音频自监督学习时引用。

**#8 VL-JEPA (arxiv_2512.10942, 2025)**
- 贡献: 将 JEPA 范式直接应用于视觉-语言对齐任务，证明预测式目标可以替代或补充对比式目标进行多模态融合。
- 用途: 讨论多模态 JEPA 或视觉-语言预训练时引用。

Claims (per-paper):
- C1: I-JEPA 是 JEPA 范式在图像域的首次大规模验证
- C2: AMI 为 JEPA 提供了长期概念框架和哲学动机
- C3: V-JEPA-2 是 JEPA 从图像扩展到视频/世界模型的关键桥梁
- C4: Rectified LpJEPA 在表示几何控制上做出了决定性贡献
- C5: Var-JEPA 打通了 JEPA 与概率建模的边界
- C6: BYOL 的 teacher-student 设计是 JEPA 架构的直接前驱
- C7: Audio-JEPA 首次证明了 JEPA 跨模态的有效性
- C8: VL-JEPA 将 JEPA 范式应用于视觉-语言对齐

Evidence:
- E1 (paper): E0004 2023_assran_self_supervised_learning_from_images_with_a_joint_embedding_predictive_architecture_cvpr_2023_paper
- E2 (paper): E0003 2022_a_path_towards_autonomous_machine_intelligence
- E3 (paper): E0007 2025_v_jepa_2_self_supervised_video_models_enable_understanding_prediction_and_planning
- E4 (paper): E0009 2026_rectified_lpjepa_joint_embedding_predictive_architectures_with_sparse_and_maximum_entropy_representations
- E5 (paper): arxiv_2603.20111 Var-JEPA A Variational Formulation of the Joint-Embedding Predictive Architecture
- E6 (paper): E0002 2020_neurips_2020_bootstrap_your_own_latent_a_new_approach_to_self_supervised_learning_paper_pdf
- E7 (paper): E0006 2025_audio_jepa_joint_embedding_predictive_architecture_for_audio_representation_learning
- E8 (paper): arxiv_2512.10942 VL-JEPA Joint Embedding Predictive Architecture for Vision-language

Mapping:
- C1 -> E1
- C2 -> E2
- C3 -> E3
- C4 -> E4
- C5 -> E5
- C6 -> E6
- C7 -> E7
- C8 -> E8

Confidence: high
