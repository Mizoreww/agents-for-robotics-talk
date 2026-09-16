# Talk outline · v0.7 · 2026-09-14

每章围绕一个代表工作，按问题 → 方法与架构 → 实验设置与结果 → 局限与总结展开。三章不是一条必须串联的 pipeline。

1. **Control（4–8）**：匿名报告原架构 → 一页 Claude Plays Robotics / RPent 背景 → Direct/Hybrid 输入输出与控制步数 → RoboDojo 结果与视频 → 有条件的结论。
2. **Data（9–13）**：Agentic Real2Sim 框图 → real/twin → 原始 pipeline → DROID-100 的完整分母与 judge 规则 → replay 与预测的区别。
3. **Improvement（14–19）**：ENPIRE 框图 → 真实任务 → human-assisted setup / fixed API → reset / verifier → learning curve → 资源成本与本章总结。

第 2 页 painting、第 20 页 hand 是独立应用展示，不支撑三项工作的定量结论。第 21 页总结三个不同的研究问题。其他 supporting works 保留在研究档案，不恢复为正文案例轮播。

## 页序与建议时间

| 页 | 标题 | 分钟 |
|---:|---|---:|
|1|Agents for Robotics|0.5|
|2|Demo: Painting with Feedback|2|
|3|Three Questions, Three Studies|1.5|
|4|Agent Controls Robot|4|
|5|Context: Models and Interfaces|2|
|6|What Enters and Leaves Each Model?|3|
|7|RoboDojo: Results and Examples|5|
|8|Control: What Did We Learn?|2|
|9|Agent Produces Data|2|
|10|Real Episode and Its Twin|2|
|11|Agentic Real2Sim: Method|4|
|12|DROID-100: Protocol and Results|6|
|13|Data: Replay Is Not Prediction|2|
|14|Agent Improves Robot|2|
|15|ENPIRE: The Real Task|2|
|16|ENPIRE: Environment and Improvement|5|
|17|ENPIRE: Reset and Verification|4|
|18|ENPIRE: Pin Insertion Curve|5|
|19|ENPIRE: Cost and Chapter Summary|3|
|20|Beyond: Structural Design|1.5|
|21|Three Studies, Three Conclusions|1.5|

总计 60 分钟，含读图、视频、停顿和讨论；不是实测时长。9 段 clips 合计约 4 分 20 秒。章首图在 4 / 9 / 14，章末总结在 8 / 13 / 19。

## 讲稿与原始媒体

- `output/Speaker_Script_Revised.md`：中文逐页讲稿，与内嵌稿同步。
- `output/Chapter_Spine.md`：问题—方法—结果—局限提纲，含来源链接。
- 第 4 页：用户所指报告的原始架构，可点击放大；不是 Astra 内部网络图。
- 第 7 页：RoboDojo Direct sorting / Hybrid packing，两段不同任务视频，不用于端到端速度比较。
- 第 11 / 12 页：Agentic Real2Sim 原始方法图与结果图。
- 第 16 / 18 / 19 页：ENPIRE 原始方法、pin-insertion 结果和资源图。

## 验收

静态与浏览器结果由 `.build/standalone_delivery_audit.json` 绑定到 HTML hash；逐页视觉记录见 `.build/standalone_visual_audit.json`。旧 PPTX/PDF/ZIP 不随本次重排，未发布 release。
