# Agents for Robotics

36 页英文 slides，中文逐页讲稿。**一个全部内嵌的 HTML**：25段视频、论文原图、Noto字体、播放器和讲稿均在文件内，可离线移动。

- Zimo Huang · 2026-09-16 · 本地版 **0.18**。
- 主文件：`output/Agents_for_Robotics_Self_Contained.html`，约 136.7 MB。
- 中文稿：`output/Speaker_Script_Revised.md`，与HTML一致。
- 章节主线：`output/Chapter_Spine.md`；逐页时间：`talk_outline.md`。
- SHA-256：`95d1da40f3a068bbce20289945c105f3646b272e68fb3da51b9d9780e95e5b5a`。
- 建议59分钟含读图、视频与讨论，尚未彩排计时。

| 页 | 部分 | 主线 |
|---|---|---|
|1–3|Introduction|Painting 与三个角色|
|4–17|Control|职责迁移、Astra能力与接口、Direct/Hybrid、latency|
|18–22|Data|三组双案例视频与downstream training问题|
|23–34|Improvement|ENPIRE方法、原图/结果、官方demo、经验迁移与RSI|
|35–36|Closing|Takeaways与感谢|

## v0.18

- P8后新增Cube / Claw双视频，区分仿真展示与理想grasp下的kinematic replay。
- 第三章集中讲ENPIRE。官网下载的reset、verification、fleet、pin/tie/cut/GPU共七段视频均内嵌。完整保留所选视频时间段，清楚标注8×或1×。
- 删除active CAD + RL / physical ICL视频，历史文件保留。新增两张官网任务照片，保留原Figure 2/3/6/7/12。
- 用Pin→written recipes→GPU解释经验迁移，最后引出RSI的held-out、matched-budget验证问题。
- 原Control/Data内容与媒体字节、Takeaways/Thank You内容保持不变，仅插页后顺延编号。

## 证据边界

Astra训练配方未披露；不把模型能力变化写成机器人数据训练的因果结论。Asim预算不同，RoboDojo/RoboLab历史基线和retained slots不混池。社区demo不构成成功率评测。Cube的action接口未披露，Claw不证明真实接触控制。

ENPIRE的environment setup有人参与。物理pass@8含conditional retries，RoboCasa则每episode只执行一次script。Figure 3与Figure 7的时间不拼接。经验总结迁移不等于coding模型权重更新，也不证明持续递归增强。

## 构建与核验

按`AGENTS.md`执行：结果来源检查→构建→CJK subset→重建→隔离复制→静态→Chrome layout/playback/UI/mobile→完整播放新增视频→视觉检查。不要手改生成HTML。

当前范围：`research/revision_0_18_spec.md`。固定基线：`.build/revision_0_18_baseline/`，包含v0.17和P21文字修改，不使用dirty Git HEAD。新来源冻结：`research/enpire_v0_18_sources.json`、`research/puzzle_v0_18_sources.json`。

P3/P23 仅竖直位置微调已完成，当前状态见 `.build/v0_18_centering_manifest.json`。当前 hash 的离线、全页布局、播放、按钮、移动端检查通过；22 项回归测试通过。其他页、讲稿与媒体未变，沿用 v0.18 的内容审查与完整视频播放证据，不把旧 hash 的记录当成新执行。

旧PPTX/PDF/ZIP保持历史，不对应本版。没有push/release，也没有执行ENPIRE或调用Claude/Anthropic服务。

本次保留范围例外：P8过渡句指向新增puzzle页，P3第三章提示同步为ENPIRE与可复用研究经验；其他原Control/Data正文不改。
