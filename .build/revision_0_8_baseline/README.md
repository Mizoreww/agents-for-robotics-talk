# Agents for Robotics

21 页英文技术分享，中文逐页讲稿。主交付是**一个全部内嵌的 HTML**：9 段视频、论文原图、Noto Serif / Noto Sans / CJK 字体、播放器与讲稿均在文件内。

- 讲者 Zimo Huang · 2026-09-16；当前本地版 **0.7 · 2026-09-14**。
- HTML：`output/Agents_for_Robotics_Self_Contained.html`，约 99.9 MB（95.3 MiB）。
- 中文讲稿：`output/Speaker_Script_Revised.md`，与 HTML 内嵌稿完全一致。
- 章节问题—方法—结果提纲：`output/Chapter_Spine.md`。
- SHA-256：`cccec9692b6470391539624e016cce0ee7860c3b0f4ebb8c3b0b8ac315cbd602`。本次未发布 GitHub Release；已有 release 可能仍是旧版。
- 60 分钟包含视频、原图读图、停顿和讨论，是建议安排，尚未彩排计时。

## 三个问题，每章一个代表工作

| 页 | 部分 | 代表工作与问题 |
|---|---|---|
|1–3|Introduction|Painting demo 与三个研究问题|
|4–8|Agent Controls Robot|匿名 Direct/Hybrid 报告：谁生成动作，action prior 有什么作用？|
|9–13|Agent Produces Data|Agentic Real2Sim：真实记录能否变成可运行的 simulation episode？|
|14–19|Agent Improves Robot|ENPIRE：真实实验能否改进 policy？|
|20–21|Other Applications / Closing|Structural design demo 与全场总结|

章首框图位于 4 / 9 / 14 页，章末总结位于 8 / 13 / 19 页。第 5 页仅简述 Claude Plays Robotics 的控制接口与 RPent 的服务组合，不再展开另一套实验。第 4 页为匿名报告的原始控制系统架构图，可点击放大。9 段视频合计约 4 分 20 秒；历史素材保留但不全部嵌入。

## 证据边界

- 不预设 LLM 必须调用 learned tools，也不宣布 Direct 普遍胜出。机器人数据训练可改变旧结论的前提；Astra 的内部网络及具体机器人预训练配方未披露。
- RoboDojo：10 selected tasks × 5 paired cases，Direct 13/50、Hybrid 24/50。Action prior、生成接口、执行段长同时变化，不是纯 prior 消融。视频是不同任务的仿真片段，省略 LLM 等待；RoboLab selected final slots 不并入主结果。
- Agentic Real2Sim：48 accepted / 8 partial / 44 failed，分母为全部 100 episodes。Any-judge best-candidate acceptance 不等于物理参数准确率或新动作预测能力。
- ENPIRE：human-assisted setup 后固定 APIs；conditional retries、reset/verifier 和资源成本都属于实验条件。它不等于 one-shot precision 或已证明的 recursive enhancement。
- Painting / hand 是定性应用展示；hand 是未经物理验证的 CAD design。无跨论文成功率排行榜。

## 构建、来源与验证

完整入口见 `AGENTS.md`。只编辑 `.build/` 的源文件，不手改生成 HTML。构建 → CJK subset → 重建 → 复制到隔离目录 → 静态检查 → Chrome layout/playback/UI/mobile audits → 最终 hash-bound validator。

- `WORKPLAN.md`：交付状态；`talk_outline.md`：页序与建议时长。
- `.build/standalone_delivery_audit.json`：最终静态及浏览器验证；`.build/standalone_visual_audit.json`：逐页视觉验收。
- `research/revision_0_7_spec.md`：当前范围；`research/revision_0_7_review.md`：Standards / Spec 复核。
- `.build/assets/v0_7/provenance.json`：原架构图来源；`research/sources.json`：当前引用与历史来源分开标记。

旧 22 页 PPTX/PDF/ZIP 保留历史，不对应当前页序。生成 HTML、依赖、下载暂存、截图和 v0.7 基线备份不提交；已归档 clips 不删改。这里只读取公开论文和源码，不调用 Claude / Anthropic 服务。
