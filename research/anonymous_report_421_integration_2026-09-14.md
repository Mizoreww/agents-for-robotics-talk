# Anonymous report 421：第一章 supporting example 核查

> 版本说明：本文保留 v0.6 素材采集时的布局建议与候选讲稿，属于方案历史。v0.7 已将本报告改为 Control 唯一代表，Claude Plays Robotics / RPent 仅作背景，RoboLab 不进入主结果；当前叙事以 `revision_0_7_spec.md` 和 `../output/Chapter_Spine.md` 为准。下方原始方法、数据与来源继续作为证据记录。


核查日：2026-09-14。保持匿名，不推测或转述身份；本文只讨论公开 report/code/media。未修改讲稿或生产生成器。素材仅写入主任务授权的 `.build/assets/v0_6/anon_*`、`.build/clips/anon_*` 和 `anonymous_clip_manifest.json`。

## 标题与定位

**GPT 6 Astra as an Embodied Policy**

副标题：*A comparative study of direct end-effector control and hybrid control with π0.5*。

[用户提供的报告](https://anonymous-report-421.github.io/public-website/?lang=en&view=1)；页面 `<title>` 是 `Data app`，那不是论文标题。当前是 technical report + public code，不称已同行评审论文。

建议放第一章，作为 **“Direct or Hybrid?”** 的一页 supporting example，替换旧的 Direct Actions and Code 案例页，而不变成第四篇 deep case。保留 Claude Plays Robotics 的 model/interface 原图和研究设计作为历史标杆。

## 与 Claude Plays Robotics 的关系

两者不是同一 benchmark 上的新旧模型复测。Claude Plays Robotics 的旧结果给出特定 model/task/interface 条件下的证据；新报告直接考察 Astra 生成 EEF action 与 hybrid action prior 的结果，进一步显示**控制能力和接口选择的最佳点是条件性的**。不能用二者 success rate 拼成模型能力进步曲线，也不能说旧论文被全盘推翻。

新报告不是 post-training 或 RSI：这次比较不通过 rollout 更新 Astra weights，也不把新经验训练回 π0.5。它属于 inference-time closed-loop control，正好为第三章“能否将经验沉淀为可复用能力”留下问题。

## 实际方法：不要把它简化为高层调用 VLA skill

- **Hybrid**：RoboDojo task-finetuned π0.5 基于 RGB、14D proprio、instruction 生成 `50×14` joint-space candidate trajectory；Astra 同时看到当前 observation、history 及候选的双臂 FK trajectory，决定接受原候选或纠正。
- **Direct**：不启动/调用 π0.5 candidate service。Astra 自行生成双臂 EEF targets 与 gripper commands，每次执行 1–5 control steps，然后重新观察。
- **共有条件**：`gpt-6-astra`, `xhigh`；task descriptions、success-condition reminders、EEF execution interface 相同；native control rate 25 Hz，不等于 LLM 以 25 Hz 生成决策。
- **不完全受控变量**：Hybrid 接受候选时执行 1–15 steps；修正/Direct 为 1–5 steps。模型先验、action-generation interface 和 segment length 同时变化，不能把差异全部归因于 VLA prior。
- **源码确认**：Hybrid schema 是 `student/edit/eef/stop`；Direct schema 仅 `eef`、1–5 steps。Bounded EEF 目标的每臂保护为 5 cm / 0.35 rad；执行器以 local damped-least-squares IK 逐 control ACK 重新计算。没有 cuRobo planning / teleportation。这是底层执行解算，不是 Agent 把任务职责全部交给高层 learned skill。

## 可引用数据：两个 suite 各自独立讲

| 范围 | Direct | Hybrid | 关键分母与边界 |
|---|---:|---:|---|
| RoboDojo selected 10-task panel | **13/50 = 26%** | **24/50 = 48%** | 10 tasks × 5 aligned cases；task、scene、eval/layout/reset/initial/policy seeds paired；任务偏向 π0.5 低成功率区间 |
| RoboDojo native mean Score | **37.8125，48 条有 native score** | **62.60，50 条** | Direct 有两条缺失 native score；SR 仍用全部 50 cases，不能混用Score分母 |
| RoboLab selected final slots | **49/50 = 98%** | **46/50 = 92%** | 10 tasks × 5 final slots；包含历史记录与 authorized retries；initial states/budgets 不完全 paired，不能视为严格同预算单次 fresh benchmark |

RoboDojo 的 π0.5 **15.6666% / Score24.43** 来自官方 per-task aggregate 在这十个任务上的重新加权，**不是同 seeds 的 rerun**。不建议将其当等条件第三根柱子，更不需要复制报告的十模型排行榜。

RoboLab 的 π0.5、Cosmos3-Nano-Policy 分别 18/50，DreamZero 17/50，来自同一 June 2026 historical cohort 各任务前五 episodes，含失败；Astra arms 是 retained historical results + retries。来源明确说 baseline 与 Astra 不保证相同 initial states、task versions 或 control settings。RoboLab 两次 Direct BlocksInBin retries 的 decision budget 从 180 增至 500；这些信息应比正文笼统的“部分 retries”更显眼。

因此页上可以说：**“Hybrid helps on one selected panel; Direct is already strong on another.”** 但不能说“controlled experiment proves Direct universally beats VLA on RoboLab”，也不能把两 suite 的 48% 与 98% 对比为任务难度或能力排名。

## 最适合口头讲的条件差异

报告给出的可能解释，而非独立因果证据：

- RoboDojo task-finetuned π0.5 可提供适配的 motor prior；所选任务包含 packing、sequence memory、construction、deformable manipulation。
- RoboLab 所选任务以 semantic pick-and-place 为主，也有 ordered stacking / mug reorientation；π0.5、Cosmos3、DreamZero 用 DROID-trained weights zero-shot，没有这些 RoboLab task demos 的微调。
- 当 Direct 已能解决任务，而 student prior 没有适配，额外审核/修正 candidate 未必提高成功。**Best representation depends on model capability, task, prior fit, feedback, and budget.**

## 效率与“14.4%”的正确说法

- 50 条 Hybrid trajectories 共 42,750 executed control steps，其中6,174修正（14.4%），36,576沿用π0.5（85.6%）。**不是 Astra 只被调用14.4%，它在每个 decision point 审核 candidate**。
- Selected runs 的 token totals：Hybrid624,762,828、Direct1,132,343,772（减少44.8%）；包含 cached input，不是 billed cost，也不包括全部早期 retries。
- Action segments：3,776 vs7,729，Direct约2.05倍。
- 视频/physical duration 按 control steps ×0.04s，不含 model-response latency。Direct更短的physical duration可能受early failure影响，不能称端到端更快。

## 已准备的两个原视频

**共同注意：两段都来自 RoboDojo，不能一段贴 RoboLab 标签。** 当前公开网站树托管100条RoboDojo rollouts和gallery clips；未找到可核验的RoboLab视频文件。网页RoboLab“150-video gallery”文字与公开树不一致，不补猜URL。

### A. Direct semantic sorting（24.64s，完整原始 evaluation rollout）

- Source case: `gpt__classify_objects__standard__g0__l3`；instruction “Sort the objects by category into the three baskets.”；native success=true、Score=1。
- [原视频](https://anonymous-report-421.github.io/public-website/media/rollouts/gpt__classify_objects__standard__g0__l3.mp4)
- Source SHA-256: `d0a09bd92d73f864c668029fd15a2761327bcf00c5a4e07aabe3949acce22c22`（与公开metadata一致）。
- 编制：完整0–24.64s，不额外倍速；建议标签 `Direct EEF · RoboDojo · successful rollout`。
- 最终：`.build/clips/anon_direct_sort.mp4`；poster `.build/assets/v0_6/anon_direct_sort.jpg`。

### B. Hybrid packing（15.44s，作者原始切片）

- Source case: `mix__pack_objects_into_box__random__g0__l1`；instruction “Place all the objects into the box with their front sides facing left.”；该case最终native success=true、Score=1。
- [原切片](https://anonymous-report-421.github.io/public-website/media/clips/clip__615a6ef1b93ea9da852f24c9__0.mp4)
- Source SHA-256: `d17fd03a8e2926f5c1474eb6fb5ebd368bfbcdd17649b497093e351d405cbf10`（与公开metadata一致）。
- 原作者从完整rollout25.48–40.92s切出（frame637–1023 exclusive，25fps）；这里保留整个15.44s片段，不再加速。
- 建议标签 `π0.5 + Astra · RoboDojo · excerpt from successful rollout`；切片不证明完整任务在15.44s完成。
- 最终：`.build/clips/anon_hybrid_pack.mp4`；poster `.build/assets/v0_6/anon_hybrid_pack.jpg`。

两段原作者视频按25Hz simulator control-time播放、删去model等待，**不是实际wall-clock录屏**。源文件与最终文件分开保存；最终编码和hash见 `.build/assets/v0_6/anonymous_clip_manifest.json`。

## 原图建议

报告 Fig.3 是RoboDojo整体Score/SR图，Fig.4是RoboLab SR图；两者为HTML/SVG实时渲染，公开树未提供独立PNG/SVG asset URL。推荐直接引用[报告结果区](https://anonymous-report-421.github.io/public-website/?lang=en&view=1#results)与[RoboLab结果区](https://anonymous-report-421.github.io/public-website/?lang=en&view=1#robolab-results)。不把本地重绘称为原图。

如果该页采用两段视频，顶部用两行简洁、带分母和条件的结果文字即可，不必再塞两张五/十模型排行榜；原有章节framework继续承担全局解释，避免内容过载。

## 可直接改写为讲稿的段落

这个新报告更适合回答“什么时候让 Agent 自己控制，什么时候借助动作先验”，而不是证明工具必不可少。在 RoboDojo 的十任务、五十个配对实例上，π0.5 加 Astra 的组合完成了二十四次，Direct 完成了十三次。但到了另一组以语义 pick-and-place 为主的 RoboLab 任务，Direct 已经达到四十九个成功的最终槽位，Hybrid 是四十六个。后一组包含重试，预算和初态没有完全对齐，所以我不会把它当成严格胜负，而把它看作值得解释的现象：当 Agent 的直接控制已经够强、已有 policy 又不太适配任务时，增加一层动作先验未必继续有益。我们真正要问的是，给定任务和预算，什么分工最合适。

## Provenance / 校验

- Code repo pinned：`anonymous-report-421/eval-of-gpt-6-astra-as-policy@79f8be5905102d6b16000c0f02a9c2195b51bb61`。
- Website repo pinned：`anonymous-report-421/public-website@9ac494dce8fcd7333eb2ea685fee5b4cddf19eb1`。
- 从 `data.json` 的 `queries.cases.rows` 独立重算：Hybrid50/24/meanScore62.6；Direct50/13/48scores/meanScore37.8125，匹配报告。
- `reportData.robolab.notes` 是retry/budget/历史baseline边界的关键来源；不要只读摘要。
- `skill/schema.py` 与 `skill/context/eef_control.md` 已只读核查；没有安装模拟器、调用模型或复现GPU实验。
- 公共源码含作者字段，但本任务按匿名处理，没有进一步关联或推测身份。
