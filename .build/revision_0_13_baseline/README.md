# Agents for Robotics

38 页英文技术分享，中文逐页讲稿。主交付是**一个全部内嵌的 HTML**：18 段视频、论文原图、Noto Serif / Noto Sans / CJK 字体、播放器与讲稿均在文件内。

- Zimo Huang · 2026-09-16；当前本地版 **0.12 · 2026-09-15**。
- HTML：`output/Agents_for_Robotics_Self_Contained.html`，约 135.2 MB。
- 职责迁移图预览：`output/Control_Responsibility_Shift.png`。
- 中文讲稿：`output/Speaker_Script_Revised.md`，与 HTML 内嵌稿一致。
- 章节问题—方法—结果提纲：`output/Chapter_Spine.md`。
- SHA-256：`a37c40df984ba507afcf6fce78443bc9c6c208c1ca9e02218bd7fb3ae0fb202c`。本次未发布 GitHub Release。
- 60 分钟为包含视频、读图与讨论的建议安排，尚未彩排计时。

## 主线

| 页 | 部分 | 讲解顺序 |
|---|---|---|
|1–3|Introduction|Painting demo 与三个不同角色|
|4–19|Agent Controls Robot|总框图 → 分层架构与职责迁移 → Claude 实验 → RPent → Astra 直接能力、interface 与 Direct/Hybrid → 总结|
|20–27|Agent Creates Data|Real2Sim → replay / scene demos → hand CAD asset → physics 与 training value|
|28–36|Agent Improves Policy|ENPIRE 的环境、实验、idea tree、效果 → Astra training / ICL demos → 成本与总结|
|37–38|Closing|Takeaways 与感谢|

章首框图在 4 / 20 / 28；总结在 19 / 27 / 36。第 5 页合并上一场 Hi Robot、Helix、Helix 02 三张原图。第 15 页保留匿名 Direct/Hybrid 原执行架构；第 31 页保留 ENPIRE 原始 idea tree。论文图可点击放大。

按用户新确认的提纲展开 Control；Data / Improvement 各细讲一个代表工作。Community demos 分布在章节内，不扩成更多论文介绍。18 段视频合计约 6 分 47 秒，不是全部视频都需要完整播放。

## 本版调整

- 删除第6页 Hi Robot 量化结果，用“Where Does Generalization Live?”职责迁移图替换。第5页三个原架构图保留。
- 以原先的设计设想开场：System 2传递语义，generalist VLA / WAM承担广泛visuomotor generalization；然后检验部分空间/动作决策是否可以上移到更强Agent。
- 职责迁移页只保留上下两条控制链，用模块宽度、青绿色重点和一条箭头表达对比；解释留在讲稿。
- 下方System 1可提供较窄action primitives，System 0中的Controller仍负责servo/tracking。图是功能性综合，不断言所有primitive都是learned VLA，也不宣布全部控制上移。
- 同步重写Control讲稿及过渡。保留10张原生结果表、18段视频、Data / Improvement与所有其他原图。
- Astra robot-data训练配方及因果未披露；“任意(o,l)→a”是generalist目标，不是已有模型的能力保证。

## 证据边界

- 不预设 LLM 必须调用 learned tools，也不宣布 Direct 普遍胜出。Astra 的内部网络及机器人预训练配方未披露，能力变化与训练因果须分开。
- Claude LIBERO-40：40 tasks × 5 seeds；Opus 4.6 Direct 3.5%、supervised 76%，MolmoAct alone 86%。两幅原图 y-axis 不同。
- Robocurve：bowl 19/20、insertion 2/20；Asim Square：ΔEEF 1/20、waypoint 18/20、code 16/20，但 control/query budgets 不齐，不能归因于纯 interface 效应。
- RoboDojo：10 selected tasks × 5 paired cases，Direct 13/50、Hybrid 24/50。Prior、interface 和执行段长同时变化。RoboLab 单列10任务/5方法，保留历史与 retries、180→500预算变化、未配对与设置未验证等限制，不混池。
- Go1 的12-joint residual chunks 经 interpolation / PD执行，推理时仿真暂停。Asim平均query time为30.75 / 26.08 / 41.98秒，来自180回合731次查询；不是全链路decision rate，也不是Controller Hz。
- Real2Sim：48 accepted / 8 partial / 44 failed，全 100 episodes。Any-judge best-candidate acceptance 不等于新动作预测。
- ENPIRE：human-assisted setup 后固定 APIs；conditional retries 和资源成本属于实验条件。Idea tree 不是独立因果消融，不等于已证明 recursive enhancement。
- 社区视频为定性展示，有加速/等待剪除及未完成验证的情况；Office 不证明新训练 locomotion，四足不等于九种验证技能，hand 是未经物理验证的 CAD。

## 构建、来源与验证

完整入口见 `AGENTS.md`。只编辑 `.build/` 源文件，不手改生成 HTML。结果数据推导 → 构建 → CJK subset → 重建 → 隔离复制 → 静态检查 → Chrome layout/playback/UI/mobile → 最终 hash-bound validator。

- `WORKPLAN.md`：状态；`talk_outline.md`：页序与建议时间。
- `.build/standalone_delivery_audit.json`：实际静态/浏览器状态；`.build/standalone_visual_audit.json`：实际视觉验收，须与当前 hash 一致。
- `research/revision_0_12_spec.md`：当前范围；`research/revision_0_12_review.md`：Standards / Spec 复核。
- `research/sources.json`：当前引用和历史来源；`.build/assets/v0_8/` 与研究快照保留新增媒体 provenance。

旧 PPTX/PDF/ZIP 保留历史，不对应当前页序；本次不更新。v0.11 基线保存在 `.build/revision_0_12_baseline/`，不与更早 Git HEAD 混同。保留既有 dirty work，不调用 Claude / Anthropic 服务。
