# Agents for Robotics

35 页英文技术分享，中文逐页讲稿。主交付是**一个全部内嵌的 HTML**：19 段视频、论文原图、Noto Serif / Noto Sans / CJK 字体、播放器与讲稿均在文件内。

- Zimo Huang · 2026-09-16；当前本地版 **0.14 · 2026-09-15**。
- HTML：`output/Agents_for_Robotics_Self_Contained.html`，约 134.7 MB。
- 职责迁移图预览：`output/Control_Responsibility_Shift.png`。
- 中文讲稿：`output/Speaker_Script_Revised.md`，与 HTML 内嵌稿一致。
- 章节问题—方法—结果提纲：`output/Chapter_Spine.md`。
- SHA-256：`dca813ac76e82ccf8e504fefe007df3c970afdbc2795e151a3a4f8f640dabe90`。本次未发布 GitHub Release。
- 55 分钟为包含视频、读图与讨论的建议安排，尚未彩排计时。

## 主线

| 页 | 部分 | 讲解顺序 |
|---|---|---|
|1–3|Introduction|Painting demo 与三个不同角色|
|4–16|Agent Controls Robot|总框图 → 分层架构与职责迁移 → Astra 直接能力、interface 与 Direct/Hybrid → 总结|
|17–24|Agent Creates Data|Real2Sim → replay / scene demos → hand CAD asset → physics 与 training value|
|25–33|Agent Improves Policy|ENPIRE 的环境、实验、idea tree、效果 → Astra training / ICL demos → 成本与总结|
|34–35|Closing|Takeaways 与感谢|

章首框图在 4 / 17 / 25；总结在 16 / 24 / 33。第 5 页合并上一场 Hi Robot、Helix、Helix 02 三张原图。第 11 页保留匿名 Direct/Hybrid 原执行架构；第 28 页保留 ENPIRE 原始 idea tree。论文图可点击放大。

按用户新确认的提纲展开 Control；Data / Improvement 各细讲一个代表工作。Community demos 分布在章节内，不扩成更多论文介绍。19 段视频合计约 6 分 53 秒，不是全部视频都需要完整播放。

## 本版调整

- P9用三段同模型Square replay探索control interfaces，补入真实code/proprio ep00视频（6.4秒，省略模型等待）。
- P10突出Waypoint proprio整列。它是Square的非privileged最佳，不是所有任务的统一赢家；原生表格保留其他行最大值。
- P11标题明确引入Hybrid架构；P9–13按要求移除大段页面说明，协议和限制仍保留在讲稿/来源。
- P15只讲latency，以30.75 / 26.08 / 41.98秒平均query time突出快速反馈问题。
- P16四项能力/短板配原生矢量图，箭头指向两个open problems：降低foundation-model latency，以及让动作更流畅、contact-rich执行更稳定的interfaces/primitives。
- 35页、19段内嵌视频，中文讲稿同步。原字体、按钮与单文件离线方式不变。

## 证据边界

- 不预设 LLM 必须调用 learned tools，也不宣布 Direct 普遍胜出。Astra 的内部网络及机器人预训练配方未披露，能力变化与训练因果须分开。
- Robocurve：bowl 19/20、insertion 2/20；Asim Square：ΔEEF 1/20、waypoint 18/20、code 16/20，但 control/query budgets 不齐，不能归因于纯 interface 效应。
- RoboDojo：10 selected tasks × 5 aligned cases，Direct 13/50、Hybrid 24/50。Score有效分母48/50；公开baseline为重加权历史结果，不是配对重跑。Prior、interface 和执行段长同时变化。RoboLab 原图保留5方法，保留历史与 retries、180→500预算变化、未配对与设置未验证等限制，不混池。
- Go1 的12-joint residual chunks 经 interpolation / PD执行，推理时仿真暂停。Asim平均query time为30.75 / 26.08 / 41.98秒，来自180回合731次查询；不是全链路decision rate，也不是Controller Hz。
- Real2Sim：48 accepted / 8 partial / 44 failed，全 100 episodes。Any-judge best-candidate acceptance 不等于新动作预测。
- ENPIRE：human-assisted setup 后固定 APIs；conditional retries 和资源成本属于实验条件。Idea tree 不是独立因果消融，不等于已证明 recursive enhancement。
- 社区视频为定性展示，有加速/等待剪除及未完成验证的情况；Office 不证明新训练 locomotion，四足不等于九种验证技能，hand 是未经物理验证的 CAD。

## 构建、来源与验证

完整入口见 `AGENTS.md`。只编辑 `.build/` 源文件，不手改生成 HTML。结果数据推导 → 构建 → CJK subset → 重建 → 隔离复制 → 静态检查 → Chrome layout/playback/UI/mobile → 最终 hash-bound validator。

- `WORKPLAN.md`：状态；`talk_outline.md`：页序与建议时间。
- `.build/standalone_delivery_audit.json`：实际静态/浏览器状态；`.build/standalone_visual_audit.json`：实际视觉验收，须与当前 hash 一致。
- `research/revision_0_14_spec.md`：当前范围；`research/revision_0_14_review.md`：Standards / Spec 复核。
- `research/sources.json`：当前引用和历史来源；`.build/assets/v0_8/` 与研究快照保留新增媒体 provenance。

旧 PPTX/PDF/ZIP 保留历史，不对应当前页序；本次不更新。最新v0.13基线保存在 `.build/revision_0_14_baseline/`，不与更早 Git HEAD 混同。保留既有 dirty work，不调用 Claude / Anthropic 服务。
