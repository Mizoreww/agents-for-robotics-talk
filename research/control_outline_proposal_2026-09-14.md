# Control 章节新提纲：分层架构、接口实验与 Astra 新能力

2026-09-14。**讨论提纲，尚未修改 HTML 或中文讲稿。** 本次用户方向替代 v0.7 中“Claude Plays Robotics / RPent 只共享一页”的安排。

后续用户要求增加 Awesome-Astra community demos，见 [demo 增补方案](astra_demo_integration_proposal_2026-09-14.md)。下面 9 页是核心讲解顺序；额外插入 1 页双视频展示后，Control 暂计 10 页。原文不扩展其他工作的要求指“不再新增深讲案例”，不排斥这次明确要求的轻量 demo 展示。

## 主线

常见分层设计 → 通用 LLM 放在哪一层，接口有多重要？ → Claude Plays Robotics 的实验 → RPent 的工程组织 → Astra 的直接动作能力促使我们重新检验分工 → 同一 Astra 换 action interface 的证据 → 开放结论。

不将“工具有用”误写成“LLM 永远只能在高层”；也不将新的直接控制案例误写成“所有低层控制或专用 policy 都已不需要”。本章暂不以 model latency 判胜负，但仍说明 action horizon、信息输入、低层 controller 和执行预算。

## 1. 原 Control 总框图保留

原图没有丢失，可从当前 Git HEAD 的 `.build/build_selfcontained.py::execution_tools` 恢复。

- Agent 既可以输出 **q / EEF Pose**，也可使用 **IK / motion planner、controller code、VLA / learned policy、WAM**。
- 所有路径仍接下游 servo / controller；perception / state tools 在 observation feedback 路径上。
- 这是全章的综合框图，不再由匿名报告的局部 Direct/Hybrid 架构替代。
- q / EEF 是一般接口选项，不表示后面每一个实验都测试了 joint-q 输出。

## 2. 一页架构背景，沿用上一场 talk 的三张原图

2026-09-14 用户确认：Hi Robot 与 Figure 合并为一页。左侧 Hi Robot，右侧上下放 Helix / Helix 02；三张原图都保留，不另增架构背景页。用简短标签区分 language、latent 和 joint target 接口，底部只留一句关于分层分工的总结。Hi Robot 原图中的两级 inference 与 Helix 02 明确命名的三级结构仍须区分。

已在 `/home/limx/Desktop/steerableVLA/steerable-vla-talk/assets/figs/` 找到 `hirobot.png`、`helix01.png`、`helix02.png`。文件身份见 `sources/control_outline_20260914/local_reference_manifest.json`；不修改原 talk。

### Hi Robot：通过语言分解任务

合并页左侧原图。High-level VLM 读复杂指令、图像与用户 interjection，输出 low-level language command；low-level π0 VLA 结合图像和机器人状态生成 action。

[官方文章](https://www.pi.website/research/hirobot)，2025-02-26；[论文](https://arxiv.org/abs/2502.19417)。官方明确称 two-level inference / System 2 + System 1；不要把图中未单列的 System 0 说成论文的第三个模型模块。底层控制器可在口头映射中说明。

### Figure：从 Helix 到 Helix 02

合并页右侧上下放两张原图，区分 interface 而不展开 performance survey。

- [Helix](https://www.figure.ai/news/helix)，2025-02-20：7B S2 → latent → 80M S1；S2 7–9 Hz，S1 200 Hz。
- [Helix 02](https://www.figure.ai/news/helix-02)，2026-01-27：S2 semantic latents → S1 full-body joint targets → S0 whole-body tracking / actuator commands。当前官网正文为 S1 200 Hz、S0 1 kHz。上一场图中的 200 Hz 标注不能误读成 S0 内部执行频率。
- 概括为一种常见、清楚的工程分工：**reasoning → visuomotor policy → low-level control**。不是所有系统必须遵守的统一定律；Helix 02 是三层命名最明确的例子。

## 3. Claude Plays Robotics：用两页讲具体实验

[官方报告](https://www.anthropic.com/research/claude-plays-robotics)，2026-07-09；2026-09-14 新鲜抓取的正文、图片地址和 hash 位于 `sources/control_outline_20260914/claude*`。公开 mirror `safety-research/embody` 的 GitHub API 在本次检查返回 404，因此依据报告与原图，不声称完成源码审计或复现。

### 做了什么

- 比较多种 model × embodiment × control interface；classic control、Go2/G1 locomotion、Franka Panda manipulation。
- 四类接口：direct action、generated Python controller、pretrained-policy supervision、RL training supervision。RL 仅交代为另一个接口，不在本章展开训练流程。
- 聚焦 manipulation 的可比较设置：LIBERO-40 = **40 tasks × 5 seeds = 200 trials / model / condition**；Direct 输出 7D EEF motion，VLA-supervised 模式接受/编辑/替换 MolmoAct proposal。
- 只用一小段 direct/code 视频示意行为，不把成功 clip 当统计。

### 有什么效果

- 同一 **Opus 4.6**：LIBERO-40 Direct **3.5%**；MolmoAct + Opus 4.6 supervision **76%**；MolmoAct alone **86%**。前两项来自报告原始 SR 图；最后一项是同图基线。
- 含义：既有 motor prior 对当时模型帮助很大；但监督器也可能干扰一个本来熟练的 policy。不能把“更多 Agent 干预”预设成正收益。
- 另有 3 个 novel goals × 12 seeds = 36 trials，VLA alone 在基线 trials 中未成功，部分监督模型带来正增益。作为讲稿的一句限定，不再增加结果表。
- 若需要更直接的 interface-design 例子：同一 Mythos Preview 在 10-task subset × 5 seeds 中，cursor 工具从 **6% → 32%**；这是 observation/tool ablation，不是 action representation ablation，也不能混用 40-task 分母。
- 原图资产已存在：`research/assets/claude_interfaces.png`、`research/assets/claude_vla.png`、`.build/assets/claude_direct.png`。重点高亮同一 model，不按模型逐个讲。

## 4. RPent：一张原图收束工具工程

[官方仓库](https://github.com/RLinf/RPent)，已有原图 `research/assets/rpent_framework.png`。只讲 Agent、memory、tool library、action primitives、统一机器人接口怎样连接。架构画出的范围不代表所有后端都已实现并评测；motion 示例不能误写为 IK（此前核查 `move_to` 使用 OSC）。

它说明怎样组织可组合能力，不单独证明大模型必须通过这些能力才能控制机器人。

## 5. 叙事转折的证据边界

Claude 报告本身描述其出发点是 general-purpose chat model without robotics training。随着 foundation-model 训练分布和能力改变，直接 action 的适用范围应重新测试。

当前可公开核实的材料尚不足以确认 Astra 机器人预训练数据的规模或因果作用。因此转折宜写为 **“模型的能力前提变了，我们需要重新测分工”**；如果提机器人数据训练，使用条件性或待验证的机制解释，不作为本章已证事实。

## 6. 新找到同一 Astra 的 action-interface 比较

[Astra control dashboard](https://asimfish.github.io/astra-control-dashboard/#sec3) 是作者公开实验面板，不是同行评审论文。使用同一 `gpt-6-astra` / medium，在 Franka / robosuite 上比较三种输出；以下只取相同 proprio 观测档位、prompt v3 的每条件 20 episodes：

| Task | ΔEEF chunks | EEF waypoints | Code → waypoints |
|---|---:|---:|---:|
| Lift | 20/20 | 20/20 | 20/20 |
| Can | 18/20 | 17/20 | 7/20 |
| Square | 1/20 | 18/20 | 16/20 |

- ΔEEF 是每次 20 个 7D OSC_POSE 动作，不是 joint-q；waypoint 为绝对 EEF targets，经 P controller 跟踪；code 返回 waypoints，也交给该 controller，不能称任意高频闭环程序。
- 公开记录的 180 个 episode badges 与九格结果一致；这只是记录一致性核查，不是实验复现。
- **必须同页注明 unequal control/query budgets**：ΔEEF ≤200 steps / 10 queries；Square waypoint ≤500 steps / 16 queries；code ≤500 steps / 3 revisions。Square waypoint 平均 256.6 steps，已超过 ΔEEF 上限，不能把差距全部归因于 action representation。
- proprio 档位还含 EEF 像素标记、相机尺度/轴向与固定地标，不是只有本体状态。
- 可用两段 Square replay：ΔEEF 失败、waypoint 成功；256×256，已实际播放核查，省略模型等待。视频只是逐回合例子，统计来自完整 20 回合条件。
- 原表是 HTML，不是论文 PNG；完整表截图仅展开网页布局，没有改数字。未来正文宜只显示三列接口示意、两段小视频与三个结果，不照搬整个密集表。

结论是 **同一模型的接口选择仍值得实验，而且效果随任务改变**，不是“waypoints 总是优于 direct action”。本轮没有找到控制模型、任务、观测、预算后覆盖 joint-q / EEF / code / VLA 的完整比较。

完整来源、视频地址、原始快照和预算边界见 [action-interface evidence note](control_action_interfaces_2026-09-14.md)。

## 7. Astra 直接能力与 Direct/Hybrid 各承担一个论证角色

### 能力转折：Robocurve 的真实机器人例子

[Robocurve 报告](https://openai.robocurve.org/gpt-6-astra/)，2026-09-04：Astra 输出绝对 EEF targets，经 IK 执行，没有独立 VLA。bowl **19/20**；round puzzle insertion **2/20**。一页以真实机器人视频为主，保留两个结果作为能力与边界，不作跨模型排行榜。精选视频删掉 thinking pauses，不能用于声称实时速度。

这页只支持“某些真实任务已能直接做好”，不支持“精细接触已全面解决”或“已证明机器人预训练是原因”。

### 保留匿名报告架构：独立 learned prior 还扮演什么角色？

保留用户先前明确要求的[匿名报告](https://anonymous-report-421.github.io/public-website/?lang=en&view=1)原始 Direct/Hybrid 图。

- Direct：Astra → EEF 1–5 steps → IK。
- Hybrid：π0.5 → 50×14 joint candidate → Astra 接受 1–15 steps 或 EEF 修正 1–5 steps。
- RoboDojo selected 10 tasks × 5 paired cases：Direct **13/50**，Hybrid **24/50**。
- 这是同一 Astra 加入 learned prior 的系统比较；prior、interface 与 segment length 同时变化，不是纯 representation 消融。joint candidate 来自 π0.5，不是 Astra 直接输出 q。
- 不使用 RoboLab 最终选留 slots 做受控胜负；不把执行框架冒称 Astra 内部网络。保留原架构，避免又退回只有 demo 没有机制的讲法。

## 8. 建议逐页提纲：9 页，按一个问题推进

这里的页码是 **Control 章内顺序**，不是当前 HTML 页码。不是九项并列工作：前两页建立全景与分层背景，三页讲旧模型的实验/工具组织，后三页检验 Astra 的新边界，最后收束。

| 页 | 建议英文标题 | 主要画面 | 这页回答什么 / 过渡 |
|---|---|---|---|
| 1 | Agent Controls Robots | 原 Agent 总框图：direct q / EEF 与多种 Agent Tools，保留反馈和底层控制 | Agent 可以在哪个层级参与控制？这张全景图贯穿全章。 |
| 2 | Hierarchical Robot Control | 左侧 Hi Robot；右侧上下放 Helix / Helix 02，三张原图同页 | 从 subtask language、semantic latent 到 joint target / low-level control；区分 Hi Robot 两级 inference 与 Helix 02 明确的三层分工。 |
| 3 | Claude: Which Control Interface? | 报告四接口原图；小型机器人/任务画面 | 固定模型后，把它放在不同接口会怎样？聚焦 LIBERO-40 的 200 trials/condition。 |
| 4 | Claude: What Changed the Outcome? | Direct 与 VLA 原始结果图，突出同一 Opus 4.6；可选一个短行为片段 | 3.5% Direct、76% supervised、86% VLA alone：motor prior 有用，Agent 干预也可能有害。 |
| 5 | RPent: Organizing Robot Tools | 一张官方 framework 图 | 工具路线怎样成为可组合的机器人系统？只讲连接，不另开 benchmark。 |
| 6 | Astra: Direct Actions in Practice | Robocurve 真实机器人视频为主，两个简短结果 | 没有独立 VLA，bowl 19/20；precision insertion 2/20。直接动作能力值得重测，边界仍在。 |
| 7 | Same Model, Different Actions | ΔEEF / waypoint / code 小接口图，Square 两段 replay 与三个数字 | 同一 Astra 换 action output 有明显差异，但执行预算不齐；Can 的排序又不同。 |
| 8 | Astra: Direct or Hybrid? | 匿名报告原 Direct/Hybrid 架构，RoboDojo 两个结果 | 新能力不等于 learned prior 没价值；13/50 vs 24/50 是系统级比较，不是单变量消融。 |
| 9 | Where Should the Boundary Sit? | 回到原总框图，高亮 S2/S1 边界和保留的 S0 | Agent 该自己生成什么、交给独立 policy 什么？答案随模型、任务与接口改变。 |

### 每页的信息预算

- 一张主图或一组短视频；不再把所有工作与所有模型结果摊成大表。
- 标题外最多一句结论。直接影响解释的限定仍可见；细节、实验分母和来源在中文讲稿/图注中保留。
- Claude 的两个原结果图必须保留轴、baseline、legend 与 uncertainty；只做重点标注，不裁掉决定结论的部分。
- Astra dashboard 可选取明确标注的 proprio 子表，但不能伪装为作者独立论文图；不得隐藏预算差异。
- 新找到的其他项目不加进正文；Hi Robot / Figure 是架构背景，RPent 是组织示意，不扩展成多篇 benchmark survey。

## 9. 章末建议结论与开放问题

**建议结论：**常见的 System 2 / 1 / 0 分工有清楚的工程依据；Claude 的实验说明旧模型如何依赖 interface 与 learned prior。Astra 的直接控制证据意味着 S2 与独立 S1 的边界应重新测量，但尚不能宣布某个接口或分层架构永远最优。

**开放问题：**更强的 foundation model 是否开始承担过去交给独立 System 1 的 action 决策？在同模型、同观测、同控制预算下，哪些任务仍需要 learned motor prior？本轮暂不以 model latency 判优，不等于忽略控制步数与反馈预算。

**本轮交付边界：**已完成公开来源研究与讨论提纲，没有调用任何模型服务，没有更改 HTML、中文讲稿或当前版本的交付审计；等待用户确认新主线后再实施。
