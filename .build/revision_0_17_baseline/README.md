# Agents for Robotics

35 页英文技术分享，中文逐页讲稿。主交付是**一个全部内嵌的 HTML**：19 段视频、论文原图、Noto Serif / Noto Sans / CJK 字体、播放器与讲稿均在文件内。

- Zimo Huang · 2026-09-16；当前本地版 **0.16 · 2026-09-15**。
- HTML：`output/Agents_for_Robotics_Self_Contained.html`，约 136.3 MB。
- 职责迁移图预览：`output/Control_Responsibility_Shift.png`。
- 中文讲稿：`output/Speaker_Script_Revised.md`，与 HTML 内嵌稿一致。
- 章节问题—方法—结果提纲：`output/Chapter_Spine.md`。
- SHA-256：`4ee50b540fe42314e9e14774da37504da8790d66b1ef944c258abf4ca9987e49`。本次未发布 GitHub Release。
- 53.5 分钟为包含视频、读图与讨论的建议安排，尚未彩排计时。

## 主线

| 页 | 部分 | 讲解顺序 |
|---|---|---|
|1–3|Introduction|Painting demo 与三个不同角色|
|4–16|Agent Controls Robot|总框图 → 分层架构与职责迁移 → Astra 直接能力、interface 与 Direct/Hybrid → 总结|
|17–24|Agent Creates Data|章首框图 → Office → kitchen → hand CAD → rope-hand → Replay → Rollout → 总结|
|25–33|Agent Improves Policy|ENPIRE 的环境、实验、idea tree、效果 → Astra training / ICL demos → 成本与总结|
|34–35|Closing|Takeaways 与感谢|

章首框图在 4 / 17 / 25；总结在 16 / 24 / 33。第 5 页合并上一场 Hi Robot、Helix、Helix 02 三张原图。第 11 页保留匿名 Direct/Hybrid 原执行架构；第 28 页保留 ENPIRE 原始 idea tree。论文图可点击放大。

Control 保留已确认内容；Data 只展示 Awesome-Astra 收录的六个 demo，不再讲 Agentic Real2Sim 论文；Improvement 保留 ENPIRE。19 段视频合计约 7 分 18 秒，不是全部视频都需要完整播放。

## 本版调整

- 增加用户指定的 Case22 articulated kitchen（第19页）与 Case23 rope-driven hand reconstruction（第21页）。
- 厨房保留列表原配图，标明 Source image；Rednote 原视频要求登录，未绕过。另核实公开 kitchen-twin 输出仓库的 ViPE / Blender 工作流。
- 绳驱手使用9月10日原视频完整24.67秒，不误用9月12日后续模型；保留 simplified mechanics / illustrative cable deformation。
- 第二章现在是章首 + 六个案例 + 总结，仍无论文深讲。中文讲稿与后续页码同步。
- 全稿35页、19段内嵌视频；所有原有媒体字节不变。

## 证据边界

- 不预设 LLM 必须调用 learned tools，也不宣布 Direct 普遍胜出。Astra 的内部网络及机器人预训练配方未披露，能力变化与训练因果须分开。
- Robocurve：bowl 19/20、insertion 2/20；Asim Square：ΔEEF 1/20、waypoint 18/20、code 16/20，但 control/query budgets 不齐，不能归因于纯 interface 效应。
- RoboDojo：10 selected tasks × 5 aligned cases，Direct 13/50、Hybrid 24/50。Score有效分母48/50；公开baseline为重加权历史结果，不是配对重跑。Prior、interface 和执行段长同时变化。RoboLab 原图保留5方法，保留历史与 retries、180→500预算变化、未配对与设置未验证等限制，不混池。
- Go1 的12-joint residual chunks 经 interpolation / PD执行，推理时仿真暂停。Asim平均query time为30.75 / 26.08 / 41.98秒，来自180回合731次查询；不是全链路decision rate，也不是Controller Hz。
- DexGPT：有 states/actions/contacts 记录，但 physical validation 未通过；其203个记录状态不是203次试验。
- ENPIRE：human-assisted setup 后固定 APIs；conditional retries 和资源成本属于实验条件。Idea tree 不是独立因果消融，不等于已证明 recursive enhancement。
- 社区视频为定性展示，有加速/等待剪除及未完成验证的情况；Office 不证明新训练 locomotion，四足不等于九种验证技能，hand 是未经物理验证的 CAD。

## 构建、来源与验证

完整入口见 `AGENTS.md`。只编辑 `.build/` 源文件，不手改生成 HTML。结果数据推导 → 构建 → CJK subset → 重建 → 隔离复制 → 静态检查 → Chrome layout/playback/UI/mobile → 最终 hash-bound validator。

- `WORKPLAN.md`：状态；`talk_outline.md`：页序与建议时间。
- `.build/standalone_delivery_audit.json`：实际静态/浏览器状态；`.build/standalone_visual_audit.json`：实际视觉验收，须与当前 hash 一致。
- `research/revision_0_16_spec.md`：当前范围；`research/revision_0_16_review.md`：Standards / Spec 复核。
- `research/sources.json`：当前引用和历史来源；`.build/assets/v0_8/` 与研究快照保留新增媒体 provenance。

旧 PPTX/PDF/ZIP 保留历史，不对应当前页序；本次不更新。最新v0.15基线保存在 `.build/revision_0_16_baseline/`，不与更早 Git HEAD 混同。保留既有 dirty work，不调用 Claude / Anthropic 服务。
