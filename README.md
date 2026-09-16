# Agents for Robotics

37 页英文 slides，中文逐页讲稿。**一个全部内嵌的 HTML**：28段视频、论文原图、Noto字体、播放器和讲稿均在文件内，可离线移动。

- Zimo Huang · 2026-09-16 · 本地版 **0.23**。
- [下载完整 HTML（v0.23 Release 附件）](https://github.com/Mizoreww/agents-for-robotics-talk/releases/download/v0.23/Agents_for_Robotics_Self_Contained.html) · 仓库保持 Private。
- 主文件：`output/Agents_for_Robotics_Self_Contained.html`，约 138.0 MB。
- 中文稿：`output/Speaker_Script_Revised.md`，与HTML一致。
- 章节主线：`output/Chapter_Spine.md`；逐页时间：`talk_outline.md`。
- SHA-256：`1ad493bd19bb81264f4b7543600ed1124451586af34b424c56ec00d230014507`。
- 建议60分钟含读图、视频与讨论，尚未彩排计时。

| 页 | 部分 | 主线 |
|---|---|---|
|1–3|Introduction|Painting 与三个角色|
|4–17|Control|职责迁移、Astra能力与接口、Direct/Hybrid、latency|
|18–22|Data|三组双案例视频与downstream training问题|
|23–35|Improvement|ENPIRE方法、原图/结果、官方demo、经验迁移与RSI|
|36–37|Closing|Takeaways与感谢|

## v0.23 — 统一 SVG 总结图

- P36 最左侧新增 Agent，分出 Control / Data / Improvement 三条路径。
- 移除截图缩略，用原生 SVG 重绘 System 2 → Primitives 与 semantic/spatial、fast/contact-rich 提示；图中文字统一 24px Noto Sans。
- 保留四个具体问题，更新中文读图提示；P35 和其他页面不变。
- 范围与验证：`research/revision_0_23_spec.md`、`research/revision_0_23.md`。

## v0.22 历史调整 — 用具体问题收束

- P36 重画为三条路径：Control → P6/P17 原页缩略 → Latency? / Better interface?；Data → Sim2Real?；Improvement → Efficiency?。
- 两张缩略图可点击放大，文字、字体和框图忠实对应 P6/P17；删除旧的抽象标语，更新中文讲稿。
- P35 仅删除指定 Open test 行，其余框图与位置不动。右侧 Script 行为和 28 段媒体均保留。
- 范围与记录：`research/revision_0_22_spec.md`、`research/revision_0_22.md`。

## v0.21 — 右侧讲稿栏

- 打开 Speaker script 时，右侧展开独立滚动讲稿，左侧 slides 和控件等比例适配剩余空间，不重叠。
- 保留全文/当前页切换，支持 N、Escape 和 Close；收起后恢复演示区域，不重建视频。
- Fullscreen 保留双栏；窄屏上下排列，短横屏也保留可读的讲稿高度。字体和全部 slides、讲稿、媒体字节保持不变。
- 范围与核验：`research/revision_0_21_spec.md`、`research/revision_0_21.md`；侧栏审计：`.build/v0_21_sidebar_audit.json`。

## v0.20 历史调整

- P31 原始图表只做竖直居中，保留原水平位置、大小、标题和学术引用。
- 原 P34 拆为 P34 **ENPIRE: Limitations** 与 P35 **Toward Recursive Self-Improvement**；后者保留研究闭环和经验复用的 open question。
- Takeaways 顺延至 P36，感谢页至 P37，中央文字为 **Thanks for listening!**。
- 当前变更与核验：`research/revision_0_20.md`；固定基线：`.build/v0_20_baseline/`。34项回归及最终浏览器、视觉核验通过。

## v0.19 历史调整

- 最新 P31 清理：删除表格和底部总结条，保留原始三联图、标题及学术引用；讲稿不再指向已删表格。核验记录：`research/revision_0_19_p31.md`。

- 最新微调：ENPIRE 灰色页脚统一为学术引用；原 P24 Learned Policy 四视频移至 P33，放在定量结果之后、Limitations/RSI 之前。

- P8后新增Cube / Claw双视频，区分仿真展示与理想grasp下的kinematic replay。
- 第三章集中讲ENPIRE。官网下载的四类reset、verification、fleet、pin/tie/cut/GPU共十段视频均内嵌。完整保留所选视频时间段，清楚标注8×或1×。
- 删除active CAD + RL / physical ICL视频，历史文件保留。新增两张官网任务照片，保留原Figure 2/3/6/7/12。
- 用Pin→written recipes→GPU解释经验迁移，最后引出RSI的held-out、matched-budget验证问题。
- 原Control/Data内容与媒体字节、Takeaways/Thank You内容保持不变，仅插页后顺延编号。

## 证据边界

Astra训练配方未披露；不把模型能力变化写成机器人数据训练的因果结论。Asim预算不同，RoboDojo/RoboLab历史基线和retained slots不混池。社区demo不构成成功率评测。Cube的action接口未披露，Claw不证明真实接触控制。

ENPIRE的environment setup有人参与。物理pass@8含conditional retries，RoboCasa则每episode只执行一次script。Figure 3与Figure 7的时间不拼接。经验总结迁移不等于coding模型权重更新，也不证明持续递归增强。

## 构建与核验

按`AGENTS.md`执行：结果来源检查→构建→CJK subset→重建→隔离复制→静态→Chrome layout/playback/UI/mobile→完整播放新增视频→视觉检查。不要手改生成HTML。

此前范围：`research/revision_0_19_spec.md`。此前固定基线：`.build/revision_0_19_baseline/`，包含v0.18交付及全部P3/P23竖直调整、文字删除，不使用dirty Git HEAD。来源冻结：`research/enpire_v0_18_sources.json`、新增reset的`research/enpire_v0_19_sources.json`及`research/puzzle_v0_18_sources.json`。新增reset由`.build/enpire_order_v019.py`检查，回归为`.build/test_enpire_order_v019.py`；extended QA完整播放十段ENPIRE与两段puzzle。

此前引用/页序核验记录：`.build/standalone_delivery_audit.json`、`.build/v0_19_polish_extended_audit.json`、`research/revision_0_19_polish.md`。官网顺序重排的独立 Standards/Spec 复核已通过；后续引用与页序微调单独记录于 `research/revision_0_19_polish.md`。本次微调的30项回归、完整播放、引用排版及最终视觉核验均已通过。

旧PPTX/PDF/ZIP保持历史，不对应本版。用户已授权将 v0.23 源码与 HTML 上传到现有 Private GitHub 仓库；HTML 因超过 100 MB，使用 Release 附件。未执行 ENPIRE 或调用 Claude/Anthropic 服务。

引用/页序微调保留了所有页面主体和媒体字节。后续 P31 仅删除表格及总结条，并修正讲稿中的“下表”指代；其他页面与所有媒体完全不变。

## GitHub 发布约定

源码、精简后的播放媒体、构建实际核验的 hash-pinned 原始来源及研究记录进入 Git。未使用的原始下载、截图渲染、重复 HTML、第三方依赖和本地缓存不进入 Git。部分已固定的原始视频超过 50 MB，但均低于 GitHub 的 100 MiB 硬限制。不能删除它们后绕过来源验证。

主 HTML 使用 Releases，随附 `.sha256` 校验文件。检出后构建仍需使用文档列出的依赖及工作路径；历史逐版审计属于历史证据，当前状态看 v0.23 的 hash-bound 审计。
