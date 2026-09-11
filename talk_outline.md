# Agents for Robotics：当前演讲结构

## 当前交付

28 页英文幻灯片，中文逐页讲稿，专有名词保留英文。建议总时长 60 分钟，包含视频、读图和短互动。主交付为单个完全内嵌 HTML。

只细讲三个标杆：Claude Plays Robotics、Agentic Real2Sim、ENPIRE。Show-Harness 和 RPent 是第一部分的接口/工具例子，ASPIRE 是第三部分的收尾例子；GPT-6 Astra 发布后一周内 X 与小红书上的社区 demo 作为应用展示，不作为定量证据。

## 三个部分

全场按 Agent 在 robotics 里的三种角色组织，每部分以一张 synthesis 流程图开场（第 5、15、20 页）：

1. **Agent Controls Robot（5–14）**：直接 action → Claude Plays Robotics 的 model/interface 比较 → VLA 工具 → Robocurve 放置/插入 → 社区真机 demo（Wenli Xiao、ARX）→ 社区仿真 demo（Yanjie Ze 魔方、双机器人抛接）→ Show-Harness 语义动作接口 → RPent 工具库 → 缺口与方向（小红书 Piper demo + 各评测数字）。
2. **Agent Produces Data（15–19）**：Agent 把真实记录转成可运行的 simulated episode。Replay acceptance 不等于 predictive validity；第 19 页附小红书 Real2Sim 流程笔记作为社区例子。
3. **Agent Post-trains Robot（20–26）**：固定 environment contract、reset 和 verifier 支持可重复真实实验（ENPIRE）；ASPIRE 把改进落在 skill 代码上。

结尾（27–28）：机械手结构设计作为三角色之外的一页应用，再总结。

## 页序

| 页 | 标题 | 建议分钟 |
|---:|---|---:|
| 1 | Agents for Robotics | 0.5 |
| 2 | Demo: Painting with Feedback | 2 |
| 3 | Our Goal | 2.5 |
| 4 | Three Roles | 1 |
| 5 | Agent Controls Robot | 1.5 |
| 6 | Direct Actions and Code | 2 |
| 7 | Model and Interface | 3 |
| 8 | VLA as a Tool | 2 |
| 9 | Demo: Placement and Insertion | 2 |
| 10 | Demo: Zero-shot Real Arms | 2 |
| 11 | Demo: Dexterity in Simulation | 2 |
| 12 | Harness: Semantic Actions | 2 |
| 13 | RPent: Robotics as Tools | 2 |
| 14 | Gaps and Directions | 2.5 |
| 15 | Agent Produces Data | 1.5 |
| 16 | Real Episode and Its Twin | 2 |
| 17 | Conversion Pipeline | 3 |
| 18 | Replay Acceptance on DROID-100 | 3 |
| 19 | Demo: Real2Sim and a Failure | 2 |
| 20 | Agent Post-trains Robot | 1.5 |
| 21 | ENPIRE: Real Experiments in the Loop | 2.5 |
| 22 | ENPIRE: Environment and Improvement | 4 |
| 23 | ENPIRE: Reset and Verification | 3 |
| 24 | ENPIRE: Pin Insertion Curve | 3.5 |
| 25 | Faster Research, Higher Token Use | 2 |
| 26 | ASPIRE: Repairing Skills | 2 |
| 27 | Beyond: Structural Design | 1.5 |
| 28 | Conclusion | 1.5 |

## 第一部分的叙事

第 5 页总图保留直接 q / EEF Pose 分支；第 6 页直接动作与 controller code，第 7 页 model/interface，第 8 页 VLA，第 9 页 Robocurve。第 10–11 页是社区 demo：真机零样本（human video → arm；一句指令转旋钮）和仿真灵巧操作（MuJoCo 魔方、抛接）。第 12 页 Show-Harness 把接口做成可评测的离散动作空间；第 13 页 RPent 把接口做成可组合的工具库；第 14 页用小红书 Piper demo 引出缺口（接触精度、延迟、动力学、具身记忆）与方向（harness/工具库、扩展动作模型、仿真与数据、真实实验自改进），并过渡到第二、三部分。新增四页沿用原有 demo 页的版式：视频加少量大字标签，数字、出处和作者观点都放在讲稿里。

语义理解、任务拆解和工具复用是适合 Agent 的职责；可靠长程执行仍受空间记忆、动作连续性和接触控制限制。更强模型与更合适 interface 是两条改进轴，不声称每项任务严格单调提升。

## 演示素材与口径

- 20 段视频，合计约 459 秒；其中 14 段沿用上一版（去掉 wiping），6 段为 2026-09-11 新增社区视频：Yanjie Ze 魔方（MuJoCo）、Wenli Xiao human-video→arm、ARX 旋钮、Show-Harness 项目视频 39–72 s 片段、双机器人抛接（MuJoCo）、小红书 Piper 胡萝卜抓放。所有社区视频保留作者倍速，静音。
- 社区 demo 均为作者自述，无 trial 统计；讲稿明确"作者报告首次成功"的性质。
- 数字口径：Robocurve 19/20 与 2/20；HumanCLAW 单次 low-thinking 运行；RoboDojo 一次社区运行 11/60；Show-Harness Table 2（每任务 10 次 trial，作者自设任务集）。
- 原始项目/研究图位于第 7、8、13、17、18、22、24、25 页；RPent 原图口径不变（DreamZero 未标记支持；`move_to` 为 OSC）。
- DROID-100 使用 any-judge best-candidate acceptance rule；ENPIRE 的 conditional retries 不等于 one-shot 或 independent best-of-eight。
- Hand 是未经物理验证的 design artifact，放在三角色之外的结尾页。
- 不做跨论文 success-rate 排行榜。

## 文件

- 主交付：`output/Agents_for_Robotics_Self_Contained.html`。
- 独立讲稿：`output/Speaker_Script_Revised.md`。同一内容内嵌到 HTML，并支持当前页/整稿阅读。
- 旧 22 页 PPTX、PDF、ZIP 与英文笔记保留作历史版本，不与当前 28 页逐页对应。
