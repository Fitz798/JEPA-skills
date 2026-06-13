# Research QA Targeted Rerun Responses

## RQ05

JEPA 在多模态迁移上的共性，不只是“都能做联合表征”，而是更具体地体现在三点：

1. 都把目标放在预测语义一致的潜表征，而不是逐模态重建细节。在视觉-语言方向，`VL-JEPA` 直接把 vision-language 对齐写进 JEPA 框架；在音频方向，`Audio-JEPA` 和 `JEPA as a Neural Tokenizer` 也都强调鲁棒语义表征，而不是波形级复原。
2. 都依赖“上下文到目标”的结构化预测，把可迁移信息压进共享表示。这意味着跨模态迁移时，模型更容易保留与下游任务相关的语义，而不是只记住单模态纹理或局部统计。
3. 下游迁移通常围绕共享 backbone 展开，再按任务加轻量适配头。视觉-语言、音频、临床多模态这几条线虽然数据形态不同，但都沿着“共享表示先成型，再做任务适配”的路线走。

更需要保守地说的是：现有证据更能说明 JEPA 已经扩展到 vision-language、audio、clinical multimodal 等方向，但对“哪一种跨模态迁移最稳定、最省标注、最抗域偏移”的统一对照证据还不够强。

Evidence: `arxiv_2512.10942`, `2025_audio_jepa_joint_embedding_predictive_architecture_for_audio_representation_learning`, `arxiv_2512.07168`, `arxiv_2509.15470`

## RQ07

如果目标是下游线性评估，JEPA 训练阶段最敏感的因素通常不是单一超参，而是下面四类会直接改表示几何的设计：

1. `masking/context` 设计。目标块有多难、上下文给多少、是否保留足够全局语义，会直接决定模型学到的是稳定语义还是局部捷径。这个点在 I-JEPA 系方法和后续 masking 相关工作里都很核心。
2. 表征稳定化机制。例如 feature normalization、方差约束或类似稳定化手段，往往会直接影响线性可分性；`Elucidating the Role of Feature Normalization in IJEPA` 就属于这类直接证据。
3. 辅助目标是否引入，以及怎么引入。`Why and How Auxiliary Tasks Improve JEPA Representations` 和视频 JEPA 的 auxiliary-objective 研究都说明，辅助目标可能明显改变表征质量，但如果加法不对，也可能把优化目标带偏。
4. 优化设置和评测协议是否绑死。当学习率、weight decay、warmup、数据增强和线性评估协议一起变化时，很容易把“训练更好”误判成“表示更好”。所以实践上应先固定评测，再单因素扫描 masking、normalization、auxiliary objective。

结论上，若你只想优先抓最敏感项，通常先看 `masking/context`，再看 `normalization/stability`，最后看 `auxiliary objectives`。

Evidence: `arxiv_2508.02829`, `arxiv_2509.12249`, `arxiv_2605.17165`, `arxiv_2605.15466`
