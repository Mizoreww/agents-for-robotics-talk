# Talk outline · v0.8 · 2026-09-14

主线：先讨论谁生成 action，再讨论谁构建 simulator，最后讨论谁改进 policy。三章是不同介入位置，不是已打通的 pipeline。每章以总框图开场，并有独立总结。

Control 按用户确认顺序展开；Simulation / Improvement 各保留一个详细代表。Community demos 展示新的工作范围，不替代正式实验。

## 页序与建议时间

| 页 | 标题 | 分钟 |
|---:|---|---:|
|1|Agents for Robotics|0.5|
|2|Demo: Painting with Feedback|1.5|
|3|Three Roles for Robotics Agents|1|
|4|Agent Controls Robot|2|
|5|Hierarchical Robot Control|2.5|
|6|Claude Plays Robotics: Interfaces|3|
|7|Claude: The Value of a Motor Prior|3|
|8|RPent: Organizing Robot Tools|1.5|
|9|Astra: Direct Actions in Practice|2|
|10|Astra: Visual Feedback in Action|1.5|
|11|Same Astra, Different Action Outputs|3|
|12|Astra: Direct or Hybrid?|3.5|
|13|Where Should the Boundary Sit?|1.5|
|14|Agent Builds Simulation|1.5|
|15|Real Episode and Its Twin|1.5|
|16|Agentic Real2Sim: Method|3.5|
|17|DROID-100: Protocol and Results|3|
|18|Astra Builds Simulation Workflows|1.5|
|19|From Replay to Prediction|1.5|
|20|Agent Improves Policy|1.5|
|21|ENPIRE: Environment and Improvement|3|
|22|ENPIRE: Reset and Verification|2.5|
|23|ENPIRE: What Did the Agent Change?|3.5|
|24|ENPIRE: Pin Insertion Curve|3|
|25|Astra: Training and Context|1.5|
|26|ENPIRE: Cost and Chapter Summary|2.5|
|27|Beyond: Structural Design|1.5|
|28|Changing the Division of Work|2|

总计 60 分钟，含读图、视频、停顿与讨论，未彩排计时。18 段 clips 合计约 6 分 47 秒。章节开场 4/14/20；章节总结 13/19/26。

## 过渡

- Control：常见分层 → 旧模型的接口实验 → 工具组织 → Astra 直接能力与同模型比较 → 分工需要重新检验。
- Simulation：已有真实交互 → 转成可运行 scene → 观察 Agent 决策与工具产物 → 衡量 conversion → 新干预预测仍须验证。
- Improvement：一次反馈不等于持久改进 → 建立可重复实验 → 修改训练/执行程序 → 学习曲线与并行实验 → 成本及成立条件。
- 最后：结构设计属于更广应用。Model 能力变化带来新的分工问题，不等于旧实验作废。

中文逐页稿见 `output/Speaker_Script_Revised.md`；章节论证见 `output/Chapter_Spine.md`；范围与审核见 `research/revision_0_8_spec.md` 和 `research/revision_0_8_review.md`。最终验证以匹配 HTML hash 的 audits 为准。旧 PPTX/PDF/ZIP 未重排，无新 release。
