# Agents for Robotics

一场 60 分钟技术分享的源码、素材处理脚本与研究笔记。交付物是单个完全内嵌的 HTML：28 页英文幻灯片加中文逐页讲稿，图片、视频、字体、样式、播放脚本与讲稿全部内嵌，约 132 MB，移动 HTML 本身即可演讲，运行不需要网络。

- 讲者 Zimo Huang，讲期 2026-09-16，资料截点 2026-09-11。
- 当前版本 0.5（2026-09-11），sha256 `1f42a44b6f8875fab7fa800096a9bd94a9a999f539ccdef1c9c8b7ca986b5b5b`。
- 版本演进见 `CHANGELOG.md`，当前状态与边界见 `WORKPLAN.md`，页序与叙事见 `talk_outline.md`，构建与约定见 `AGENTS.md`，面向听讲者的操作说明见 `output/README.md`。

## 三个部分

全场按 Agent 在 robotics 里的三种角色组织，每部分以一张 synthesis 流程图开场（第 5、15、20 页）。

| 页 | 部分 | 内容 |
|---|---|---|
| 1–4 | Introduction | 开场 painting demo、目标、三角色总览 |
| 5–14 | Agent Controls Robot | 直接 action 与 controller code、model/interface 比较、VLA as a tool、Robocurve 放置与插入、社区真机与仿真 demo、Show-Harness、RPent、Gaps and Directions |
| 15–19 | Agent Produces Data | 真实 episode 与其 simulated twin、conversion pipeline、DROID-100 replay acceptance、Real2Sim 失败案例 |
| 20–26 | Agent Post-trains Robot | ENPIRE 的 environment contract、reset 与 verification、pin insertion curve、token 开销、ASPIRE |
| 27–28 | Closing | 机械手结构设计（放在三角色之外）、总结 |

三个细讲标杆：Claude Plays Robotics、Agentic Real2Sim、ENPIRE。Show-Harness、RPent、ASPIRE 为支撑例子。20 段视频，合计约 459 秒。

## 目录

- `output/` — 交付物与中文讲稿 `Speaker_Script_Revised.md`；`README.md` 是演讲使用说明。
- `.build/` — 构建与校验脚本、clip manifest、下载记录、审计 JSON，以及讲稿权威源 `script_revised.md`。
- `research/` — 调研笔记与来源快照：`survey_notes.md`、`media_storyboard.md`、`talk_narrative_review.md`、`interface_application_revision.md`、`community_demos_2026-09-11.md`、`sources.json`、`sources/`。

权威状态文件：`.build/standalone_delivery_audit.json`（校验结果，含 `browser_audits` 状态）、`.build/standalone_build_audit.json`（slides / videos / hash）、`.build/slide_records_revised.json`（逐页标题、分组、分钟）。

## 重建

完整命令序列与依赖见 `AGENTS.md`。仓库内已包含重建所需的全部输入：`.build/focus_draft.pptx`、`.build/focus_rendered/*.layout.json`、`.build/clips/*.mp4`（20 段内嵌视频，79 MB）、`.build/assets/*.jpg` 海报、`.build/script_revised.md`、`output/offline_player/media_credits.json`、`research/assets/rpent_framework.png`。

注意：沿用上一版的 14 段 clip 必须与 `output/offline_player/media_credits.json` 记录的 sha256 逐字节一致，校验脚本对此有断言；重新编码不保证得到相同字节，因此这些 clip 入库而不是靠重新下载。

## 不入库的内容

以下条目体积大、可再生或与本讲无关，通过 `.gitignore` 排除。

| 条目 | 体积 | 说明 |
|---|---|---|
| `output/Agents_for_Robotics_Self_Contained.html` 及 `.build/standalone_isolation/index.html` | 各 132 MB | 超过 GitHub 100 MB 单文件上限，用 `build_selfcontained.py` 重建 |
| `output/*.pptx`、`*.zip`、`*.pdf`、`output/offline_player/{media,posters,slides}` | 约 240 MB | 0.2 版历史交付，与当前 28 页不逐页对应。其生成链依赖仓库外的 presentation runtime，需要时从本地备份取回；`media_credits.json` 是构建输入，已保留 |
| `.build/assets/*_source.mp4` 等原始下载 | 242 MB | 项目页素材用 `fetch_media.py` 与 `continue_assets.py` 重取；2026-09-11 的社区视频按 `.build/community_downloads.json` 记录的 `post_url` 与 `sha256` 重取（fxtwitter API 元数据 + X CDN ≤1280 px，小红书取 note 页 stream URL）。X CDN 链接会过期，因此成品 clip 已入库 |
| `.build/prior_*/` 下的 HTML、`.build/previews/`、各 `*_rendered/`、`*.pdf` | 约 380 MB | 历史或可再生的构建产物。`prior_*` 里的源文件（md / json / py）保留入库 |
| `.build/font_deps`、`.build/static_render_deps`、`.build/qa_deps`、`.build/node_modules` | 107 MB | 第三方依赖，重装即可 |
| `.build/reference/`、`.build/reference_review.html` | 3.2 MB | 另一场讲座（Steerable Hierarchical-VLA）的渲染页，仅作排版参考，不属于本讲内容 |
| `research/searches/github_empire.json` | 345 KB | 检索词 "empire" 与 ENPIRE 撞名的结果，混入无关第三方内容，无研究价值 |

## 证据口径

- 只细讲三个标杆，其余工作作为背景、对照或支撑例子。
- 社区 demo（X、小红书）按定性材料使用：作者自述、带倍速、无 trial 统计，讲稿标注其性质，不进入定量结论。
- 数字只来自被引用的评测：Robocurve 放置 19/20、插入 2/20；HumanCLAW 单次 low-thinking 运行；RoboDojo 一次社区运行 11/60；Show-Harness Table 2（每任务 10 次 trial，作者自设任务集，位于第 12 页）。不做跨论文 success-rate 排行榜。
- Agentic Real2Sim 测的是 replay acceptance，采用 any-judge best-candidate 规则；ENPIRE 的成绩包含其 reset 与 conditional retry 协议。
- 若干素材有明确限定：hand 是未经物理验证的 design artifact；microphone 片段是动力学失败后的 kinematic replay；Yanjie Ze 魔方是 MuJoCo physics replay，动作为学习还是脚本，帖子未说明。
- RPent 是 RLinf 组织下的独立仓库，不是 VLA backbone；其架构图范围大于已确认的集成，DreamZero 未标记支持，`move_to` 用 OSC。
- 逐条来源见 `research/sources.json` 与 `research/sources/`，社区素材的评估见 `research/community_demos_2026-09-11.md`。

## 使用第三方材料的说明

本仓库为私有存档。`research/sources/` 是公开论文、项目页与帖子的完整快照，`.build/clips/` 是社媒与项目页视频的剪辑片段，均用于这次分享的引用与讲解，作者与出处记录在 `research/sources.json`、`.build/community_downloads.json` 与 `.build/media_downloads.json`。仓库若要公开或对外分发，应先把这些第三方媒体换成按记录重新抓取的脚本。
