# Agents for Robotics：当前演讲结构

## 当前交付

26 页英文幻灯片，中文逐页讲稿，专有名词保留英文。建议总时长 60 分钟，包含视频、读图和短互动。主交付为单个完全内嵌 HTML。

只细讲三个标杆：Claude Plays Robotics、Agentic Real2Sim、ENPIRE。RPent 是第一章的简短工具包案例，ROSA / ROS-MCP 仅作对照；第四章展示其他应用，不增加第四篇论文细讲。

## 叙事主线

Agent 调用什么工具，产生什么结果，用什么证据判断它有用？进一步看哪些结果能够保留，帮助后续工作。

1. **Execution（5–11）**：Agent 选择和组合 Agent Tools。先用 RPent 说明工具如何组织，再借 Claude Plays Robotics 解释接口优势和边界。精细控制及真机试错成本引出 simulator。
2. **World building（12–16）**：工具链把真实交互变成可运行场景。Replay acceptance 不等于 predictive validity；对新动作的预测仍需单独验证。
3. **Improvement（17–22）**：直接组织真实实验。固定 environment contract、reset 和 verifier 支持可重复试验，结论仍受 setup 与 retry protocol 限定。
4. **Other applications（23–25）**：结构设计和程序调试扩大应用视野。Hand 是设计方案，ASPIRE 展示程序检查与修复；不同产物需要不同验证。

四章分别以第 5、12、17、23 页的 synthesis 流程图开场。第 11、16、22、25 页讲稿保留简短小结与过渡；第 26 页统一收束。这些角色不是互斥分类，也不是必须按顺序执行的统一流水线。

## 页序

| 页 | 标题 | 建议分钟 |
|---:|---|---:|
| 1 | Agents for Robotics | 0.5 |
| 2 | Demo: A Robot Paints with Feedback | 2 |
| 3 | Our Ultimate Goal | 2.5 |
| 4 | Three Core Roles, Broader Applications | 1 |
| 5 | Execution: An Agent with Many Tools | 2.5 |
| 6 | RPent: Packaging Robotics as Agent Tools | 2.5 |
| 7 | Claude Plays Robotics | 3 |
| 8 | Direct Actions and Controller Code | 3 |
| 9 | VLA Tools: Grounding and Supervision | 2.5 |
| 10 | Demo: Placement and Fine Insertion | 2 |
| 11 | Demo: Wiping a Table | 1 |
| 12 | World Building: Replay and Prediction | 2 |
| 13 | Agentic Real2Sim: A Real Episode and Its Twin | 2.5 |
| 14 | Agentic Real2Sim: The Conversion Pipeline | 3.5 |
| 15 | Replay Acceptance on DROID-100 | 3 |
| 16 | Demo: Real2Sim and a Disclosed Failure | 2 |
| 17 | Improvement: A Repeatable Real Experiment | 2 |
| 18 | ENPIRE: Real Experiments Inside the Loop | 3 |
| 19 | ENPIRE: Environment and Improvement | 4 |
| 20 | ENPIRE: Reset and Verification | 3.5 |
| 21 | ENPIRE: Improvement on Pin Insertion | 3 |
| 22 | Faster Research, Higher Token Use | 2 |
| 23 | Other Applications: Design and Engineering | 1.5 |
| 24 | Demo: Structural Design of a Robot Hand | 2 |
| 25 | Demo: Inspecting and Repairing an Execution | 2 |
| 26 | Conclusion | 1.5 |

## 演示素材与口径

- 15 段原项目或作者视频，合计 376.90 秒，其中两段源自 GIF；未额外加速。
- 原始项目/研究图位于第 6、7、9、14、15、19、21、22 页，保留坐标、legend 和必要限制。
- RPent 的原图描述架构范围，不证明所有模型或硬件已验证；DreamZero 在固定版本 README 中未标记支持。工具调用例子是说明，不是新执行的机器人实验。
- IK / WAM 是扩展工具例子，不是 Claude Plays Robotics 新增的测试组。RPent 的 `move_to` 使用 OSC，不称为 IK。
- Robocurve 是独立评测；microphone 是 dynamics failure 后的 kinematic replay；hand 是未经物理验证的 design artifact。
- DROID-100 使用 any-judge best-candidate acceptance rule；ENPIRE 的 conditional retries 不等于 one-shot 或 independent best-of-eight。
- 不做跨论文 success-rate 排行榜。

## 文件

- 主交付：`output/Agents_for_Robotics_Self_Contained.html`。
- 独立讲稿：`output/Speaker_Script_Revised.md`。同一内容内嵌到 HTML，并支持当前页/整稿阅读。
- 旧 22 页 PPTX、PDF、ZIP 与英文笔记保留作历史版本，不与当前 26 页逐页对应。
