# v0.9：Simulation / Improvement 实验结果补充

核查日期：2026-09-14。格式：Markdown；两篇均按 empirical / systems evidence 核查。此文件只给当前 talk 的结果表与原图候选，不扩成新的论文综述。

## 推荐落地

1. **Agentic Real2Sim：把现有 DROID-100 结果页补成完整四 backend 表**，原 Figure 3 保留为可放大的原始证据；不用再只讲 Gemma 一行。
2. **ENPIRE：增加一页模型 × 两个物理任务的结果表**。使用官网实际绘图数据，不从柱高估值；保留原 Figure 3 的曲线，或将其放到紧接的一页。
3. **ENPIRE：若再加一页，优先原 Figure 6 的 RoboCasa 多任务/基线图**，旁边放“方法/结果性质”短表，不填未公开的精确百分比。
4. 现有 ENPIRE 成本总结页可以补充 MRU / GPU / MTU 三行数表，**不再新增一张成本页**。不要为了“所有 demo 都有数字”替社区 demo 发明实验分母。

## 1. Agentic Real2Sim — 完整 backend 表

### 可直接上 slide 的英文表

建议标题：**DROID-100: Outcomes and Model Cost**。

| VLM backend | Accepted | Partial | Failed | Model bill / 100 episodes |
|---|---:|---:|---:|---:|
| Gemma 4 31B | 48 | 8 | 44 | $2.62 |
| Qwen 3.6 35B | 45 | 11 | 44 | $12.97 |
| Claude Haiku 4.5 | 37 | 12 | 51 | $9.16 |
| GPT-5.4 | 43 | 12 | 45 | $82.30 |

**E1：所有数字直接印在原 Figure 3 上**，并与 §4.2–4.3 文本中的 success counts 和 cost ratios 交叉一致。[paper §4.3 / Fig. 3](https://arxiv.org/html/2607.19190v3#S4.F3)。本表的 48 等是计数；由于每行 N=100，其数值恰好等于百分比，slide 仍建议使用计数以保持分母醒目。

原图：[`agentic_replay_results_original.png`](sources/control_results_20260914/later/agentic_replay_results_original.png)。[官方原始 PNG](https://arxiv.org/html/2607.19190v3/figures/figs/compressed/replay_outcomes_model_cost.png)。原图右轴是 logarithmic cost，不能截去轴或改成线性柱高进行比较。

建议页脚：**All 100 attempts retained. Replay acceptance ≠ predictive validity. Model bills only.**

### 必须保留的 protocol / cost scope

- DROID-100 是抽样的 100 个 manipulation episodes，覆盖 objects / views / occlusion / pick-place-push-insert；提前失败和无合法 judge record 的 episode 也保留在分母中。[§4.2](https://arxiv.org/html/2607.19190v3#S4.SS2)
- 每 episode 从最新 grasp sweep 中筛出 eligible candidates，至多 5 个；按 peak object displacement 排序，sample id 打破平局。3 个不同 VLM judges 独立看 real / simulated keyframes。[§4.1](https://arxiv.org/html/2607.19190v3#S4.SS1)
- **任何一个 judge 的 best candidate ≥8/10 即 accepted**，不是 majority vote，不是所有 judges 一致通过。最大 score=7 为 partial；≤6 或无合法记录为 failed。[§4.1 / Fig. 3](https://arxiv.org/html/2607.19190v3#S4.SS1)
- 同一 pipeline configuration，仅换 VLM backend，selected agentic steps 开启 reasoning；论文说 model bills 包含该 configuration 下的全部 model usage。**GPU-hours、perception/simulator compute、人工和 wall-clock 全成本未报告，不能叫 total reconstruction cost**。[§4.3](https://arxiv.org/html/2607.19190v3#S4.SS3)
- GPT-5.4 / Gemma 的 model bill 比值为论文报告的 31.4×；这不是 reconstruction speedup，更不是 physics fidelity 提升。[§4.3](https://arxiv.org/html/2607.19190v3#S4.SS3)

### 不应额外捏造的表

**L1：没有正式 quantitative critic ablation 或 failure-stage histogram。** Fig. 2 的 segmentation / pose-tracking failures 是说明性例子，不是各失败原因占比。不能把 44 failures 分摊到 segmentation、pose、physics 等类别。[§4.2](https://arxiv.org/html/2607.19190v3#S4.SS2)

**L2：Deformable / humanoid 是 qualitative stress tests，不存在可引用的同分母 success rate。** [§4.4](https://arxiv.org/html/2607.19190v3#S4.SS4)。如需一句补充：**Rigid DROID: 100-episode evaluation; deformable/humanoid: qualitative only.**

**C1（有限结论）：**在这个把 VLM 限定为 bounded decisions、让专业 perception / simulation tools 承担底层计算的 pipeline 中，换昂贵 VLM 没有对应更高的 observed replay acceptance；不能由此证明 foundation-model capability 对所有 world building 都不重要，也没有统计等效性检验。

## 2. ENPIRE — 两个物理任务的模型对照表

建议标题：**ENPIRE: Results Across Two Tasks**。

| Coding agent | Physical Push-T @ 8 h | Pin insertion @ 4 h |
|---|---:|---:|
| Codex / GPT-5.5 xhigh | 0.9375 | 95.5% |
| Claude Code / Opus 4.7 High | 0.7500 | 97.5% |
| Kimi Code / Kimi K2.6 thinking | 0.6250 | 79.0% |
| **Metric / policy family** | **Normalized score / heuristic** | **Success rate / gradient-based** |

可视排版时，Push-T 保留 0.938 / 0.750 / 0.625 即可；明确是 normalized score，**不要把 0.9375 改叫 93.75% binary task success**。

**E2：本表并非像素估读。** 官方 ENPIRE 网页随 JS 发布了与 Figure 3 对应的 `pushtModel` / `pinModel` arrays；每 configuration 有 4 条 `runs`，并显式给出上述终点 `highlight_mean`。已静态解析、保存原 JS、原文 byte range 与 SHA；没有执行任何网页/作者代码。

- [官方网页](https://research.nvidia.com/labs/gear/enpire/)
- [官方 JS 原始数据](https://research.nvidia.com/labs/gear/enpire/_next/static/chunks/11dgx9quo0zhy.js)
- [`enpire_site_model_scaling_data.json`](sources/control_results_20260914/later/enpire_site_model_scaling_data.json)
- [`enpire_site_model_scaling_data.provenance.json`](sources/control_results_20260914/later/enpire_site_model_scaling_data.provenance.json)
- [论文原 Figure 3](https://arxiv.org/html/2606.19980v1#S1.F3)；本地完整原图 [`enpire_scaling_original.png`](sources/control_results_20260914/later/enpire_scaling_original.png)

### 对这张表的 protocol 限定

- 表中是 **官网给出的 plotted means at the stated research times**，不是另一次独立 held-out benchmark，不是 pooled binary count。每 configuration 可检查到 4 条显示轨迹，但独立随机 seed 数、采样规则、最终专门 test set 的大小没有充分披露；不能写“4 independent replications”。
- 原图带 individual traces 和 uncertainty bands；最终讲稿/放大原图保留它们。网页没有给这些 bands 一个足够明确的统计定义，不称其为 confidence interval。
- 论文 physical task success 包含 **up to 8 conditional retries inside a rollout**，失败观察可以影响后续恢复；不是 pass@1，也不是 independent best-of-8。[§3](https://arxiv.org/html/2606.19980v1#S3)
- Pin insertion 的目标为 **50 consecutive successes**；允许 agents 搜索 BC、iterative BC、online/offline/offline-to-online RL、BC regularization、batch size 和 update rate 等。[§3.2](https://arxiv.org/html/2606.19980v1#S3.SS2)
- 必须先完成人工参与的 Environment setup；此后 reset / verifier / safety / Gym APIs 固定。这里研究的是 policy/training code 改善，不是 agent 可以任意改 reward 来“提高成功率”。[§2.1–2.2](https://arxiv.org/html/2606.19980v1#S2.SS1)
- **E2 与 Idea Tree 的 E6 不是同一个统计对象**：不要把 Figure 12 的 team-average best trajectory 当作这里某个固定 current policy 的 held-out score。

建议页脚：**Official plot means; 4 displayed traces/config. Different task metrics. Physical rollouts allow ≤8 conditional retries.**

## 3. ENPIRE — 多任务 baseline 原图（第二优先）

建议标题：**ENPIRE: Tools, VLA and Autoresearch**。原图 [Figure 6](https://arxiv.org/html/2606.19980v1#S3.F6)：[`enpire_robocasa_original.png`](sources/control_results_20260914/later/enpire_robocasa_original.png)。

| Setting / comparison | What is actually reported |
|---|---|
| RoboCasa365; GR00T N1.5 | End-to-end VLA baseline |
| RoboCasa365; CaP-X* | Zero-shot agentic tool use, without autoresearch |
| RoboCasa365; ENPIRE | Highest aggregate plotted result among these three; exact bar values not numerically reported |
| Discovered execution strategy | Detection + motion planning to hover above target, then grasp; tools and VLA can be composed |

**E3：保留原始 aggregate bar chart，不向表里填 52%、77%、27% 一类像素推测值。** 图上没有 numeric labels，paper HTML 和所查官网 JS 均未找到对应精确 bar data。原图包含 8 个 task panels：OpenCabinet、TurnOnSinkFaucet、OpenDrawer、OpenStandMixerHead、PnPSinkToCounter、TurnOffStove、PnPCounterToCabinet、CoffeeMugSetup。不要把 8 个 exemplar panels 冒称 paper 逐任务数表。

Canonical RoboCasa evaluation：每 generated script 每 episode 运行一次，native success predicate；已报告的 40-episode evaluations 使用预先冻结的 `(seed, layout_id, style_id)` list，generator seed=42，同一 task 的 methods 使用相同 list / initial states / cameras / task instruction；禁 oracle poses/state、reset/repeated-retry APIs。[Appendix D.1–D.2](https://arxiv.org/html/2606.19980v1#A4.SS2)。**这个仿真 protocol 不要沿用 physical pass-with-8-retries。**

可再配一条量化机制证据，而不新增整页：SAM3 diagnostic 的每点 N=20 queries；原 prompt 在 256×256 为 10/20 correct，higher resolutions 达 14/20；agent candidate prompts 从 14/20 提升到 17/20 后 plateau。这是 **detection accuracy，不是 rollout success**。[Fig. 16](https://arxiv.org/html/2606.19980v1#A4.F16)，原图 [`enpire_detection_original.svg`](sources/control_results_20260914/later/enpire_detection_original.svg)。

## 4. ENPIRE — fleet / resource 表（补充已有成本页）

| Agent–robot pairs | Mean robot utilization | Mean GPU utilization | Mean tokens / minute |
|---:|---:|---:|---:|
| 1 | 49.14% | 29.41% | 9,269.21 |
| 4 | 30.87% | 32.52% | 40,028.72 |
| 8 | 29.78% | 48.96% | 140,310.43 |

**E4：数字来自同一官方网页 JS 的 `utilization` / `tokenRate` fields，非柱高估读。** Slide 可四舍五入为 49.1/30.9/29.8%、29.4/32.5/49.0%、9.3k/40.0k/140.3k。原图要保留 error bars；不把这些均值暗示为无变异或精确硬件常数。

若需要均值±离散度表，以下 `std` 字段是官网源数据的字面值，不是自己从误差棒估计：

| Pairs | MRU, mean ± source `std` (%) | GPU active, mean ± source `std` (%) | MTU, mean ± source `std` (tokens/min) |
|---:|---:|---:|---:|
| 1 | 49.14 ± 24.93 | 29.41 ± 11.43 | 9,269.21 ± 2,648.62 |
| 4 | 30.87 ± 10.86 | 32.52 ± 12.86 | 40,028.72 ± 29,441.58 |
| 8 | 29.78 ± 9.48 | 48.96 ± 30.15 | 140,310.43 ± 14,912.40 |

任务/单位：§3.6 指定 **pin insertion**。MRU 是 robot actively executing experiment 的 research wall-clock fraction，并比较 per-robot utilization；GPU 是 GPU actively in use 的 wall-clock fraction，不能自动换成 nvidia-smi 的 SM occupancy 定义；MTU 是该 fleet 随研究时间平均的 tokens/min，不能误标成每个 agent 的 tokens/min。图中随 fleet 增长的量不是 per-agent 恒定率。页脚可写：**Pin insertion; official plot mean ± std. Aggregation details not fully specified.**

- 原 Figure 7：[paper anchor](https://arxiv.org/html/2606.19980v1#S3.F7)；本地 [`enpire_utilization_original.svg`](sources/control_results_20260914/later/enpire_utilization_original.svg)
- 原始数据：[`enpire_site_resource_data.json`](sources/control_results_20260914/later/enpire_site_resource_data.json)，配套 [provenance](sources/control_results_20260914/later/enpire_site_resource_data.provenance.json)
- 官网字段另有 robotStd/gpuStd、MTU std；统计重复数与 error-bar estimation protocol 未充分说明。不要自行赋予 confidence level。

**C2（有限结论）：**1→8 pairs 提高 GPU active utilization，却降低 per-robot utilization；MTU 从约 9.3k 增至约 140.3k，比 8×线性增幅更高。论文把原因联系到 peer-branch 阅读与汇总、等待模型、调试等，而不是所有新增机器人持续执行实验。[§3.6 / §4](https://arxiv.org/html/2606.19980v1#S3.SS6)

### 时间与 token 指标不能拼接

**E5a（Figure 3 / §3.3）：**Push-T 的 1.0 normalized score，1→8 pairs 约 5h→2h；Pin insertion near-perfect，>1.5h→约40min。[§3.3](https://arxiv.org/html/2606.19980v1#S3.SS3)。官网 `pinScaling` 名称明确是 `1-agent best` / `4-agent team best` / `8-agent team best`，不是 all robots current mean。

**E5b（Figure 7 / 官网 resource data）：**`tokensToSuccess` 的 1/4/8 pairs 行分别为 2.50M/7.69M/16.84M tokens，以及 4.5/3.2/2.0 h。**这不是 E5a 的40min曲线**。论文未充分解释两组 time-to-success 的关联或协议差别，不能自行给它们补一个不同 stopping threshold 的原因，更不能把 16.84M 与40min拼成同一实验结果。

因此推荐当前成本页用上面的 utilization / token-rate 表；如想列 tokens-to-success，必须连同同图自己的 4.5/3.2/2.0h 放在单独 block，注明不能与 Figure 3 直接对齐。

## 5. ENPIRE 其他可引用结果与不能越界的地方

- **E6：Idea tree**：I37 BC regularization +10.8 pp、I66 batch-size tuning +0.9 pp、I76 controller compensation +1.3 pp，是一条 autoresearch run 的 **team-average best-score trajectory milestones**，不是固定其他因素的 independent causal ablations。[Appendix B.6 / Fig. 12](https://arxiv.org/html/2606.19980v1#A2.SS6)
- **E7：Gym-PushT sim heuristic learning**：论文 Figure 5 caption 明确写 Codex / Claude Code 约2h达到95%，Kimi约两倍时间。[Figure 5](https://arxiv.org/html/2606.19980v1#S3.F5)。原图 [`enpire_pusht_sim_original.png`](sources/control_results_20260914/later/enpire_pusht_sim_original.png)。这不是 physical Push-T @8h 的同一种结果，不能混表成共用 success rate。
- **E8：GPU insertion transfer**：由 pin autoresearch 总结成 Markdown，传到新 task；prior raw trajectories / hidden logs / checkpoints 被移除。可讲“recipe knowledge transfer”，不要说 foundation-model 权重自我训练或跨任务模型能力递归增强。[§3.4](https://arxiv.org/html/2606.19980v1#S3.SS4)、[Appendix B.1](https://arxiv.org/html/2606.19980v1#A2.SS1)
- 官网 headline 的 **99% pass@8 across showcased tasks** 缺少足够逐任务分母说明；不建议新造 GPU insertion / zip-tie 各自99%的表。Paper 只给 high success / strategy transfer 的地方，写 **not reported numerically**。
- 引言文本把 pin convergence 与 human-in-the-loop prior work 对比，但当前已核图没有可提取的 matched baseline 数表。不要制造 ENPIRE-vs-PLD-RL 的精确快几倍结论。
- 新增 Astra quadruped / office / ICL / hand demo：不能从剪辑或作者 headline反推实验统计；现有的 qualitative / status labels 保留。尤其四个 separate experts、FULL EVAL NOT MET、ICL 非 weight training 的边界不应被“增加 results”要求覆盖。

## 6. 只读代码核查与证据边界

**Agentic Real2Sim** public repo 已按 `880389bda289d2e78154c73ae1b6d23b7a650557` pin；只读 `README.md` 与 [`ar2s/grasp_candidates.py`](https://github.com/agentic-real2sim/agentic_real2sim/blob/880389bda289d2e78154c73ae1b6d23b7a650557/ar2s/grasp_candidates.py)。`CANDIDATE_TOP_K=5`、finite metric 筛选、peak displacement 排序与 paper 描述相符。这个文件明确服务于 cleanup / handoff 且没有 evaluation-specific dependencies，故**没有把它冒称完整 three-judge 实现**；judge rubric 与 all100 denominator 仍是 paper-stated。公开主项目 tree 未找到独立 judge/evaluation 实现；不据此推断论文没有评估。

**ENPIRE** public repo 已按 `99ee90acf65b5b18957c8382ad580db999528be3` pin；只读 [`enpire/policy/autoresearch_instruction.md`](https://github.com/NVlabs/ENPIRE/blob/99ee90acf65b5b18957c8382ad580db999528be3/enpire/policy/autoresearch_instruction.md) 与 [`enpire/policy/pld/runtime/README.md`](https://github.com/NVlabs/ENPIRE/blob/99ee90acf65b5b18957c8382ad580db999528be3/enpire/policy/pld/runtime/README.md)。Contract 明确 environment/reset/verifier/safety/evaluation seeds 不可修改、frozen rolling-window 50 metric、failed trials 保留；runtime 确认 actor/learner code 的存在。**这不是重新跑实验，也不独立验证报告的成功率。**

原始论文 HTML hashes 与窄范围摘录见 `sources/control_results_20260914/later/paper_provenance.json` 和相邻 `*_relevant_excerpts.txt`；图片 manifest、JS manifest 和 code manifest 也在该目录。没有安装依赖、导入/执行作者项目、调用 Claude/Anthropic、启动机器人或训练。

## 7. 简短中文讲述方向

Real2Sim：**这里不只给成功视频。把100次尝试全部摊开，最好的这组也只有48次被接受。更贵的模型没有带来更多 replay acceptance，说明这套系统的瓶颈不能只归结为推理模型不够强。但48不是“物理世界建模准确率”，而是这套 best-candidate、best-judge protocol 下的 replay acceptance。**

ENPIRE：**我们要把“会运行研究流程”和“流程真的提高了策略”分开看。这张表显示，在相同论文里，coding agents 对 Push-T 的 heuristic discovery 和 pin insertion 的 gradient-based learning 都有可见改进，但两个任务的指标不一样。再看 RoboCasa 的原图，autoresearch 也可以改善工具和 VLA 的组合，而不是一定重新训练所有东西。最后，更多 agent–robot pairs 能缩短寻找好策略的时间，但每台机器人的利用率下降，token 成本增长更快。**
