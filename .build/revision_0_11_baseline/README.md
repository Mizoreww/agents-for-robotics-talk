# Agents for Robotics

37 页英文技术分享，中文逐页讲稿。主交付是**一个全部内嵌的 HTML**：18 段视频、论文原图、Noto Serif / Noto Sans / CJK 字体、播放器与讲稿均在文件内。

- Zimo Huang · 2026-09-16；当前本地版 **0.10 · 2026-09-14**。
- HTML：`output/Agents_for_Robotics_Self_Contained.html`，约 135.0 MB。
- 中文讲稿：`output/Speaker_Script_Revised.md`，与 HTML 内嵌稿一致。
- 章节问题—方法—结果提纲：`output/Chapter_Spine.md`。
- SHA-256：`c8ce5975116882cb36f40e827d53d9a64c18fb91e8767410d6ca7501de787a28`。本次未发布 GitHub Release。
- 60 分钟为包含视频、读图与讨论的建议安排，尚未彩排计时。

## 主线

| 页 | 部分 | 讲解顺序 |
|---|---|---|
|1–3|Introduction|Painting demo 与三个不同角色|
|4–18|Agent Controls Robot|总框图 → Hi Robot / Figure → Claude 实验 → RPent → Astra 直接能力、interface 与 Direct/Hybrid → 总结|
|19–25|Agent Builds Simulation|Agentic Real2Sim 的问题、方法、DROID-100 → Astra 工作流 demos → replay / prediction|
|26–34|Agent Improves Policy|ENPIRE 的环境、实验、idea tree、效果 → Astra training / ICL demos → 成本与总结|
|35–37|Beyond / Closing|Structural design、Takeaways 与感谢|

章首框图在 4 / 19 / 26；总结在 18 / 25 / 34。第 5 页合并上一场 Hi Robot、Helix、Helix 02 三张原图。第 15 页保留匿名 Direct/Hybrid 原执行架构；第 29 页保留 ENPIRE 原始 idea tree。论文图可点击放大。

按用户新确认的提纲展开 Control；Simulation / Improvement 各细讲一个代表工作。Community demos 分布在章节内，不扩成更多论文介绍。18 段视频合计约 6 分 47 秒，不是全部视频都需要完整播放。

## 本版调整

- 第 4 页合并 VLA / WAM / Learned policy；第 7 页使用一个 LLM 和对齐的接口分支。
- 第 18 页用 Semantic intent / Spatial grounding / Physical interaction 诊断框图收束。这是独立综合，不是未读取微信文章的分类。
- 11 张原生表格突出声明比较组内的最佳显示值，保留并列、原数值与实验限制；资源表仅标描述性极值。
- 第 36 页为少字 Takeaways 框图，第 37 页为感谢页。保留18段视频和所有原图，中文讲稿同步。
- 原结果 authority `research/results_v0_9.json` 与13个固定来源保持不变。

## 证据边界

- 不预设 LLM 必须调用 learned tools，也不宣布 Direct 普遍胜出。Astra 的内部网络及机器人预训练配方未披露，能力变化与训练因果须分开。
- Claude LIBERO-40：40 tasks × 5 seeds；Opus 4.6 Direct 3.5%、supervised 76%，MolmoAct alone 86%。两幅原图 y-axis 不同。
- Robocurve：bowl 19/20、insertion 2/20；Asim Square：ΔEEF 1/20、waypoint 18/20、code 16/20，但 control/query budgets 不齐，不能归因于纯 interface 效应。
- RoboDojo：10 selected tasks × 5 paired cases，Direct 13/50、Hybrid 24/50。Prior、interface 和执行段长同时变化。RoboLab 单列10任务/5方法，保留历史与 retries、180→500预算变化、未配对与设置未验证等限制，不混池。
- Real2Sim：48 accepted / 8 partial / 44 failed，全 100 episodes。Any-judge best-candidate acceptance 不等于新动作预测。
- ENPIRE：human-assisted setup 后固定 APIs；conditional retries 和资源成本属于实验条件。Idea tree 不是独立因果消融，不等于已证明 recursive enhancement。
- 社区视频为定性展示，有加速/等待剪除及未完成验证的情况；Office 不证明新训练 locomotion，四足不等于九种验证技能，hand 是未经物理验证的 CAD。

## 构建、来源与验证

完整入口见 `AGENTS.md`。只编辑 `.build/` 源文件，不手改生成 HTML。结果数据推导 → 构建 → CJK subset → 重建 → 隔离复制 → 静态检查 → Chrome layout/playback/UI/mobile → 最终 hash-bound validator。

- `WORKPLAN.md`：状态；`talk_outline.md`：页序与建议时间。
- `.build/standalone_delivery_audit.json`：实际静态/浏览器状态；`.build/standalone_visual_audit.json`：实际视觉验收，须与当前 hash 一致。
- `research/revision_0_10_spec.md`：当前范围；`research/revision_0_10_review.md`：Standards / Spec 复核。
- `research/sources.json`：当前引用和历史来源；`.build/assets/v0_8/` 与研究快照保留新增媒体 provenance。

旧 PPTX/PDF/ZIP 保留历史，不对应当前页序；本次不更新。v0.9 基线保存在 `.build/revision_0_10_baseline/`，不与更早 Git HEAD 混同。保留既有 dirty work，不调用 Claude / Anthropic 服务。
