# Data / Improvement：章节逻辑梳理提案

2026-09-14。讨论稿，未修改 HTML、中文讲稿或当前交付版本。与同日 Control 的 9 页提纲配套；Data / Improvement 仍各细讲一个代表工作，不新增论文轮播。

后续用户要求增加 Awesome-Astra community demos，见 [demo 增补方案](astra_demo_integration_proposal_2026-09-14.md)。下面的 5 + 6 页为核心讲解；每章各插入 1 页双视频展示后，暂计 6 + 7 页，不新增深讲论文。

## 整场演讲的连接

| 章节 | 核心问题 | Agent 留下的产物 |
|---|---|---|
| Control | 当前这一步，谁来决定机器人怎么动？ | action / 被调用的 controller 或 policy 输出 |
| Simulation（原 Data） | 已记录的真实交互，能否变成可运行的模拟场景？ | simulator scene、参数、replay artifacts |
| Improvement | 一次实验的反馈，能否让后续使用的策略变得更好？ | 新版本 policy、code 或 training recipe |

三章讨论 Agent 介入机器人工作的三个位置，不是一套系统已经连通的三级流水线。第一章可把某个 VLA 当作已有工具，第三章则把 policy / training code 当作改进对象。第二章展示另一个角色：构建实验场景。ENPIRE 直接做真实实验，不依赖先运行 Agentic Real2Sim。

建议标题：第二章 **Agent Builds Simulation**，第三章 **Agent Improves Policy**。前者比 Agent Produces Data 更贴近本章实际证据；后者说明留下的是可复用策略变化，而非仅在当前 rollout 临时纠错。

## 当前叙事需改进的地方

- Data 章目前在导图、demo、方法、结果、总结中多次重复 replay 与 prediction 的区别，挤占了“为什么难、Agent 究竟决策什么”的讲解。保留结果页的关键限定，完整讨论集中到章末。
- Improvement 章在导图、通用任务视频、方法页重复解释 setup / loop；reset 和 verifier 很具体，但 policy 具体被如何修改仍较抽象。用论文原始 idea tree 替代单独的通用任务介绍页，不增加章节页数。
- 先明确问题和贡献，再说明支持它的实验范围；既不把结果拔高，也不让每页都成为局限清单。

## 第二章：Agent Builds Simulation（建议保留 5 页）

代表工作：[Agentic Real2Sim](https://arxiv.org/html/2607.19190v3)。

### 主线

已有大量真实交互记录 → 手工转成 simulator 很复杂 → Agent 协调工具与修正步骤 → 得到可执行 episode twin → 检验 replay conversion 的覆盖率 → 再区分重放与新干预下的预测。

### 逐页

| 页 | 标题 | 主要画面 | 讲解任务 |
|---|---|---|---|
| 1 | Agent Builds Simulation | 保留本章综合框图：recording → tools / scene → simulation → comparison → repair | 从人工建场景、对齐坐标和调参数的负担提出问题；说明输入是真实交互记录，不只是单个 RGB 视频。 |
| 2 | From Recording to Simulation | 同一 episode 的 real / sim 并排视频 | 先让观众看到输入与产物：不仅生成外观，还要让机器人、物体、相机和轨迹在 simulator 中运行。 |
| 3 | What Does the Agent Decide? | 论文原始方法图，用标签区分 Agent decisions 与 specialist tools | 解释发现对象、选择 keyframe/mask、检查 tracking、选择 repair；mesh / depth / tracking / calibration / sweep 由专门组件承担。 |
| 4 | How Often Does Conversion Work? | DROID-100 原始结果图，突出 48 accepted / 8 partial / 44 failure | 说明所有 100 episodes 在分母；结果是指定规则下找到 accepted replay 的比例，不是只统计成功 demo。 |
| 5 | From Replay to Prediction | 简洁对照图：recorded action → matching replay；new action → prediction（待验证） | 总结已经得到可运行、可检查的 scene artifact；若要用来规划或训练，还要检验新的 action / initial state。 |

### 方法讲解必须具体，但不念工具名单

1. **输入**：synchronized camera streams、calibration、robot trajectory、depth / stereo geometry、task context。不要简化成“给一段任意视频就自动变成物理世界”。
2. **Agent 的决策**：object discovery、keyframe selection、mask acceptance / retry、tracking reinitialization、选择操纵物体与 ground reference，以及 replay-based refinement choices。
3. **工具的工作**：segmentation、mesh recovery、depth、pose tracking、deterministic calibration，以及 contact / grasp candidate sweep。不是 Agent 自己替代所有几何计算和物理引擎。
4. **可检查的中间产物**：meshes、scale、pose tracks、robot trajectory、camera metadata → MuJoCo scene → rendered replay / structured metrics。
5. **修正分支**：scene preparation 可选择 deterministic sweep 或 LLM-assisted replay-refinement loop，不应画成每个 candidate 都必然由 LLM 自由调参。

### 实验口径

- 论文 §4.1–4.3 / Figure 3：最佳 backend Gemma 4 31B，48 accepted、8 partial、44 failure，全 100 episodes 留在分母。
- 每 episode 最多 5 个 eligible candidates；3 位 VLM judges 分别选最佳 candidate，任意一个 judge 的最佳分数 ≥8/10 即通过。不是 majority vote。
- 这套口径要在结果图注中可见；详细 rubric 放中文讲稿，不用大段文字挤满幻灯片。
- 不扩展为 backend 能力排行榜；model-call cost 不是完整 pipeline 成本。若成本不是主问题，可不在正文逐项读成本图。

**章末一句话：**Agent 把记录转成可运行的 simulation artifact；这为后续实验提供了起点，预测新干预的可靠性仍要单独验证。

**过渡：**有了可运行的场景，仍需要通过实验判断策略是否真的变好；而下一项工作选择直接在真实机器人上建立这种实验循环。

## 第三章：Agent Improves Policy（建议保留 6 页）

代表工作：[ENPIRE](https://arxiv.org/html/2606.19980v1)。RSI / robot self-improvement 作为方向性背景，不添加 ASPIRE / RoboRSI 对比页。

### 主线

一次动作做对不等于以后更会做 → 需要保留下来的 policy 改进 → 真实实验缺少可重复 reset / verification → ENPIRE 构建固定实验接口 → Agent 实际修改训练代码并试验 → policy 改善与并行加速 → 资源和评价边界。

### 逐页

| 页 | 标题 | 主要画面 | 讲解任务 |
|---|---|---|---|
| 1 | Agent Improves Policy | 保留章首综合框图：hypothesis / code → rollout → feedback → revision | 与 Control 区分：修改的是下次 trial 仍会用到的 policy / training code，不只是下一条 action。 |
| 2 | Make Experiments Repeatable | 论文原始 ENPIRE framework；标出 human-assisted setup / autonomous improvement 两阶段 | 固定 action、safety、reset、verification APIs；再让 Agent 改策略。不可在策略失败时偷偷改成功标准。 |
| 3 | Reset, Run, Verify | pin reset 与 zip-tie verifier 两个原视频 | 让抽象实验接口可见：怎样启动下一轮、怎样知道做对；注明两视频来自不同任务。 |
| 4 | What Did the Agent Change? | 原 Figure 12 idea tree + 同轴 hill-climbing curve | 用真实记录讲 BC regularization、batch-size tuning、controller compensation 等尝试；图中保留无收益分支。 |
| 5 | Does the Policy Improve? | pin insertion 原始 learning / fleet-scaling 曲线 | 分别回答策略随研究推进是否提高、更多 agent–robot pairs 是否缩短 time-to-target。 |
| 6 | Faster Research, More Resources | 只保留与 time / tokens-to-success 有关的原图，附简短章节总结 | 更快不等于更省；把固定环境内的 policy improvement 与更强意义的 recursive improvement 分开。 |

### 新加入的实质内容：policy 到底怎么变好

原论文 §3.2 说明 pin insertion 的 Agent 尝试 BC、带 online rollout data aggregation 的 iterative BC，以及含 BC regularization 的 online / offline / offline-to-online RL，并修改相关训练参数。

附录 B.6 / Figure 12 给出一个 agent-team run 的 idea tree 与 team-average best success curve：

- **I37 / BC regularization**：论文标注 +10.8 percentage points。
- **I66 / batch-size tuning**：+0.9 pp。
- **I76 / controller compensation**：+1.3 pp。
- 实心节点表示 best-score 改善，空心节点是已评估但没有改善；粗线追踪最高分 idea 的 lineage。

这比通用“改代码—跑实验”的文字更直接。主画面不必列完所有数字，可只重点指 BC regularization 及一个无收益分支。必须称为该 run 的探索记录，**不是每项修改独立随机消融得到的平均因果增益**；team-average best curve 也不能说成每个当前 policy 都单调变好。

待实施时从同版本论文取 Figure 12 原图，保留树、曲线、标签及无收益节点，不凭文字重画一个“只成功、不失败”的线性故事。此次仅核查原文，未新增生产素材。

### 实验口径与 RSI 的位置

- pin insertion：1 → 8 个 agent–robot pairs，将达到 near-perfect success 的 research time 从 >1.5 h 缩短到约 40 min（§3.3）。这是研究开发时间，不是单次动作的 inference latency。
- fixed rollout protocol 包含最多 8 次 conditional retries；success rate 不能叫 one-shot precision，也不是 independent best-of-eight。
- 增加并行资源可提高 time-to-result，但 token 使用增加；讲清实际 tradeoff，不把“scaling”当成统一效率收益。
- reset 常从任务关键 subphase 开始；human-assisted environment setup 是前提，不声称任意环境即插即用。
- 跨 trial 留下的变化可以是 policy weights / code / recipe，不要求 foundation LLM 更新权重。不要把所有这些更新都叫同一种 gradient-based post-training。
- 可放在 robot self-improvement 方向下讨论，但不能仅因存在反馈环就声称改进者自身获得了递归增强能力。

**章末一句话：**在可重复、可验证的真实实验接口内，Agent 已能把试验反馈转成后续策略改进；扩大实验并行度还能缩短研究周期，但其前提和资源代价同样重要。

## 压缩与媒体安排

- 两章页数暂保持 5 + 6，重点是去掉重复解释，不增篇目。
- ENPIRE 原通用 task-video 独立页由 idea-tree 原图页替代；需要保留的任务片段可纳入章内已有视频区域，但不为它再加页。
- 每页只回答一个问题；方法图、real/sim 视频、reset/verifier 视频、idea tree 和 learning curves 承担主要讲解。
- 关键 protocol 限定跟着数字出现，完整局限集中章末；不在每页重复一整段 disclaimer。
- 不改当前 v0.7 的 Chapter_Spine、讲稿、页面顺序或审计记录；这些只在新提纲获确认并实施后同步。

## 本次核对来源

- 当前讲稿 `.build/script_revised.md` 第 9–19 页及 `output/Chapter_Spine.md`。
- Agentic Real2Sim 本地全文快照 `research/sources/agentic_real2sim_paper.txt`，重点 §3.2、§4.1–4.3、Figure 3；对应 [论文](https://arxiv.org/html/2607.19190v3)。
- ENPIRE 本地全文快照 `research/sources/enpire_paper.txt`，重点 §2.1–2.2、§3.2–3.3、Appendix B.6 / Figure 12；对应 [论文](https://arxiv.org/html/2606.19980v1)。
- 仅做材料阅读与提纲梳理，没有运行作者代码、调用模型服务或复现实验。
