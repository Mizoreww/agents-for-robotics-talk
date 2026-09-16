# Changelog

## [0.12] - 2026-09-15
### Features
- 第6页Hi Robot结果替换为职责迁移示意图；保留第5页原架构。
- Control讲稿围绕generalist能力的承载位置展开：从VLA/WAM到更强Agent配合较窄action primitives。
### Design Rationale
- 保持38页与现有章节页码，用同一页完成原假设、新模式与研究问题的对照。
- 末端标System 0 / Controller，保留低层tracking；角色迁移是部分、功能性的，不混同网络架构与工具实现。
### Notes & Caveats
- 未新增实验数据或训练因果声明；Astra robot-data配方未披露，generalist任意输入能力只是目标。
- 18段视频与其他结果不变；无新Release或legacy导出。

## [0.11] - 2026-09-15
### Features
- 第二章统一为 Data，覆盖 Assets / scenes、Real-to-sim Replay、Data Rollout；手部CAD案例移入该章。
- 新增一页 Astra实际动作接口与公开query time，明确Go1 joint chunks、EEF/IK、Asim OSC/waypoints/code、Hybrid prior review的区别。
- Control总结明确语义/有限空间能力与高频反馈/物理泛化缺口；Data总结加入DexGPT原图和未通过物理验收的事实。
- 38页英文slides，中文讲稿同步；18段视频与既有结果表不变，仍为单文件内嵌HTML。
### Design Rationale
- 用产物分类Data，避免将CAD或replay误当作通过物理验证的训练数据。
- 秒/次用于展示具体harness的查询成本，Controller Hz与simulator-time feedback不作为LLM推理频率。
### Notes & Caveats
- Asim为prompt-v3/medium/proprio、180回合731次查询的公开日志重算，不是独立性能测试或匹配预算的速度排名。
- 新来源单独冻结，原v0.9结果来源保持不变。未调用模型服务、未复现实验、未读取安全阻止的WeChat文章。
- 尚未彩排计时；不更新历史PPTX/PDF/ZIP，不推送或发布Release。

## [0.10] - 2026-09-14
### Features
- Merge the Control overview's learned-tool nodes and align the Claude interface branches around one LLM.
- Add a capability-diagnostic Control summary, replace slide 36 with diagram-led Takeaways and append Thank You as slide 37.
- Bold reported table extrema within explicit comparison groups, retaining ties and all original values.
- Synchronize Chinese narration, preserve all 18 embedded clips, original figures and the Noto/player styling.
### Design Rationale
- Separate semantic intent, spatial grounding and physical interaction as coupled diagnostic questions, not fixed System 2/1/0 modules.
- Preserve different execution/training endpoints and distinct validation needs across the three chapters.
### Notes & Caveats
- The WeChat article remains unread; the diagnostic synthesis is independent and user-approved.
- Bold describes reported extrema, not significance, equal-budget comparisons or an overall resource-efficiency winner.
- Local HTML/script revision only. No push, release or historical PPTX/PDF/ZIP update. Timing remains unmeasured.

## [0.9] - 2026-09-14
### Features
- Expanded to 36 English slides while retaining all 18 embedded clips and the existing Noto/player design.
- Added Hi Robot, Harness VLA, Asim, separate RoboDojo/RoboLab, full Real2Sim backend, and ENPIRE physical/RoboCasa results pages; enhanced Claude, Robocurve and resource pages with native tables.
- Added source-hashed result derivation and per-cell/protocol regressions; synchronized Chinese narration and documentation.
### Design Rationale
- Keep the v0.8 narrative and its original figures, but make each formal source's experimental evidence inspectable rather than relying on headlines or selected videos.
- Separate metrics, denominators, training conditions and selected-slot protocols instead of creating a cross-paper leaderboard.
### Notes & Caveats
- RoboLab is a descriptive retained-slot/retry comparison. Hi Robot IA/TP are not episode success; Harness uses exploration memory; Asim budgets differ.
- ENPIRE physical and simulation protocols differ; official trace means/std are not asserted independent replications or confidence intervals. No numeric RoboCasa bar estimates.
- All media remain embedded. Suggested 60 minutes is unmeasured. No public release, push, source experiment replication, or historical PPTX/PDF/ZIP update.

## [0.8] - 2026-09-14
### Features
- Reorganize the talk into 28 English slides, synchronized Chinese narration and 18 embedded clips.
- Restore the Agent/action/tools overview; combine Hi Robot, Helix and Helix 02 original figures; expand Claude's concrete experiments and retain one RPent framework page.
- Add same-Astra action-interface evidence, the original Direct/Hybrid architecture, and chapter-local keyboard, Office/Newton and quadruped demos.
- Clarify Agentic Real2Sim's decisions/artifacts and ENPIRE's actual policy changes using the complete original Figure 12 idea tree.
### Design Rationale
- Follow the user-approved sequence from common division of work to new capability and open questions, rather than declaring tools mandatory or obsolete.
- Keep original figures and short videos primary; preserve Noto typography, player controls and one-file offline portability.
### Notes & Caveats
- Astra's pretraining cause is undisclosed; Asim budgets are unequal; Direct/Hybrid changes multiple factors; ENPIRE retries, setup and costs remain explicit.
- Community demos are qualitative, sometimes sped up or partially validated. No source experiments were reproduced.
- 60 minutes is suggested, not rehearsed. No PPTX/PDF/ZIP update, push or Release; final QA belongs to hash-bound audit records.

## [0.7] - 2026-09-14
### Features
- Reduced the talk to 21 English slides and 9 embedded clips, with synchronized Chinese narration and a separate problem–method–results chapter spine. Noto typography, white/teal layout and player controls are preserved.
- Each chapter now has one representative: the anonymous Direct/Hybrid report, Agentic Real2Sim, and ENPIRE. Claude Plays Robotics and RPent share one short Control background page; other supporting studies remain in the research archive.
- Embedded the anonymous report's original English control architecture at chapter opening 4. Chapters open at 4/9/14 and summarize at 8/13/19. Retained original paper figures, relevant project videos, and separate painting/structural-design demos.
### Design Rationale
- Keep each problem, mechanism, experiment and conclusion within one study rather than assembling an argument from several partially explained works.
- Robot-data training can change the premises behind earlier interface findings; the cited evidence does not establish Astra's internal training recipe. Tool necessity and universal Direct superiority both remain unproven.
### Notes & Caveats
- RoboDojo: 13/50 Direct versus 24/50 Hybrid on selected paired cases; action prior, interface and segment length vary together. RoboLab final slots are excluded from the main table. The two simulation clips depict different tasks and omit LLM waiting time.
- Real2Sim's 48/100 is any-judge best-candidate replay acceptance, not physical-parameter accuracy. ENPIRE's conditional retries, human setup and token costs remain explicit.
- Fixed an unsupported RPent IK label and filtered the image audit to delivered assets; static regressions cover both. All 9 clip payloads remain byte-identical to their sources in the previous build.
- HTML SHA-256 `cccec9692b6470391539624e016cce0ee7860c3b0f4ebb8c3b0b8ac315cbd602`; final state is recorded in hash-bound audits. 60 minutes is an unmeasured timing target. Historical PPTX/PDF/ZIP and GitHub Release are unchanged.

## [0.6] - 2026-09-14
### Features
- Reframed the28-slide talk as From Action to Reusable Capability; retained Noto fonts, white/teal style and polished offline controls. Chinese narration remains synchronized with English slides.
- Added GPT-Policy-Eval plug/goal-image clips, the user-supplied anonymous Direct/Hybrid report with two RoboDojo clips, and RoboRSI original consolidation figure/ACT comparison.21active clips, about9minutes. Four superseded clips remain archived.
- Renamed Part3 to Agent Improves Robot; chapter-opening diagram separates weights, code and skill knowledge. Corrected ASPIRE's knowledge-reuse mechanism. ENPIRE resource discussion moved into curve narration rather than adding pages.
### Design Rationale
- Do not infer that LLMs inherently must delegate control, or that Direct universally beats Hybrid. Numeric/semantic actions, code generation and complete skill delegation distribute responsibility differently.
- Report primary evidence with its denominator/budget; model robot-pretraining scale/causality remains unverified. Treat RSI as a research question, not proven recursive amplification.
### Notes & Caveats
- Anonymous RoboLab final slots include historical runs/retries/unequal budgets; different reported orderings are not a controlled causal reversal. Both displayed report videos are different RoboDojo simulation tasks, excluding LLM latency.
- RoboRSI code-on/off retains identical Base Skills; its ACT comparison is one same-task example, notRL/transfer evidence. Cumulative coverage is not frozen-policy SR.
- Build hash `e4e8c9c571b8c7304364705c7a054d705c3ab1814a5b006d6a64e131570b2cf2`; final static/browser/visual status is recorded in hash-bound audits.60minutes is a rehearsal target. HistoricalPPTX/PDF/ZIP and GitHub Release are not updated.

## [0.5.1] - 2026-09-11
### Features
- Put the project under Git and added the two entry-point documents it lacked: a root `README.md`
  (what the talk is, the three parts, how to rebuild, what the repo deliberately omits, the evidence
  conventions) and a real `AGENTS.md`. The previous `AGENTS.md` held only an auto-generated
  memory-plugin context block and carried no project rules.
- Added `.gitignore`: the rendered deliverables, raw download staging, vendored Python/Node
  dependencies and regenerable renders stay out; the build inputs, including the 20 embedded clips,
  are committed so the deck can be rebuilt from a clone.
### Design Rationale
- The 14 clips carried over from earlier revisions are asserted byte-identical against the SHA-256 in
  `output/offline_player/media_credits.json`, and the X CDN URLs they came from expire, so re-encoding
  cannot reproduce them. They are committed rather than re-fetched.
### Notes & Caveats
- Corrected six documentation statements that no longer matched the build: the Show-Harness numbers are
  on slide 12 and not slide 14 (WORKPLAN), the six new community clips were listed as four
  (output/README), a speaker-script sentence still pointed at "slide 10" under the old 26-slide
  numbering, and `survey_notes.md` still described an appendix and a wiping clip that 0.5 removed and
  cited a stale source count. The deck was rebuilt and re-verified; sha256 is now
  `1f42a44b6f8875fab7fa800096a9bd94a9a999f539ccdef1c9c8b7ca986b5b5b`.
- Redacted six Xiaohongshu `xsec_token` access tokens from the saved note snapshot, made
  `prepare_clips*.py` find ffmpeg/ffprobe on PATH instead of a hard-coded conda path, and made the
  preview-server path in `.claude/launch.json` relative.
- Excluded from the repository: renders of a different presentation kept as a typography reference, and
  a GitHub search result whose query collided with the ENPIRE paper name and returned unrelated
  third-party content.

## [0.5] - 2026-09-11
### Features
- Reorganized the talk into three parts named after the Agent's role: Agent Controls Robot (5–14), Agent Produces Data (15–19), Agent Post-trains Robot (20–26), plus a two-slide closing. Each part opens with its synthesis diagram; ASPIRE moved into Part 3; the hand design remains as one closing slide outside the three roles.
- Shortened every slide title to at most 40 characters (for example "Model and Interface", "VLA as a Tool", "Gaps and Directions").
- Added six community clips gathered on 2026-09-11 from X and 小红书: Yanjie Ze's MuJoCo Rubik's Cube with two dexterous hands, Wenli Xiao's human-video-to-arm demo, ARX's washing-machine knob demo, a Show-Harness project-video excerpt, two MuJoCo humanoids juggling, and a 小红书 Piper carrot pick-and-place at 70×. Removed the wiping clip. 28 slides, 20 clips, 60-minute target.
- Added "Harness: Semantic Actions" (Show-Harness, arXiv 2609.10522; cross-task averages from Table 2 on the slide, the full table in the script) and "Gaps and Directions", which lists current shortcomings (contact and precision, latency, dynamics, embodied memory) and directions (harness and tool libraries, scaled action models, simulation and data, repeatable real experiments). The added slides keep the deck's sparse demo style: large short labels, details and citations (Jitendra Malik, Max Fu, Yu Xiang, HumanCLAW, a RoboDojo run) in the Chinese script and source lists.
- Rewrote the Chinese script for all 28 slides with the three-part framing and new transitions; the 小红书 Real2Sim note is cited on slide 19.
- Title slide: speaker "Zimo Huang", talk date 16 September 2026, subtitle line removed; the footer keeps the sources cut-off (11 September 2026).
### Design Rationale
- The three roles match what the Agent produces: actions, data, or a retained policy/skill. Community demos are shown as application evidence next to each role, and the gaps slide keeps demo footage separate from cited evaluation numbers.
- Show-Harness and RPent are two implementations of the same interface idea (an evaluable action space versus a composable tool library); neither claims to solve contact or long-horizon execution.
### Notes & Caveats
- All community clips are author-reported demonstrations with playback speed-ups and no trial counts. Show-Harness numbers come from the authors' own task set (10 trials per task). HumanCLAW is a single low-thinking run; RoboDojo is one community run.
- Yanjie Ze's demo is a MuJoCo physics replay of one fixed scramble; whether the motion is learned or scripted, and whether it transfers to real hands, is not stated in the post.
- Community clips were fetched through the fxtwitter metadata API and X's CDN (≤1280 px formats); the 小红书 clip came from the note page's stream URL. Post metadata snapshots are in `research/sources/x_*_fxtwitter.json`; downloads are recorded in `.build/community_downloads.json`.
- Historical PPTX/PDF/ZIP deliverables remain unchanged.

## [0.4.1] - 2026-09-11
### Features
- Reordered Execution as chapter diagram → direct actions/controller code → model/interface comparison → VLA → real demos and limitations → RPent synthesis. Retained 26 slides, all 15 clips and a 60-minute target.
- Added a direct q / EEF Pose branch to the chapter diagram, explicitly retaining the downstream servo/controller.
- Reused the wiping page for semantic/task-decomposition strengths and continuity/contact/fine-manipulation limitations. Updated Chinese transitions and the conclusion to emphasize both model capability and interface design.
### Design Rationale
- Begin with the physical-control problem, establish what different interfaces contribute, then use RPent to organize the resulting division of work instead of opening with toolkit architecture.
- Keep long-horizon planning potential distinct from proven long-horizon execution, and familiar-task VLA advantages distinct from universal model rankings.
### Notes & Caveats
- Model-generation improvements are uneven in direct control; more tools, abstraction or input do not guarantee improvement. Contact-state estimation is a reasoned bottleneck interpretation, not a separately proven cognitive mechanism.
- Static resource/order/script checks and a 26-page print-engine render were completed. The app Browser webview could not attach, so no fresh video/interaction/mobile pass is claimed for this revision. Existing video bytes and player controls are unchanged.
- Rebuilt the embedded Chinese font from the complete generated script, including generated source-heading characters; 733 required Chinese glyphs are covered.
- The historical PPTX/PDF/ZIP deliverables remain unchanged.

## [0.4] - 2026-09-10
### Features
- Reframed the opening around Agent + robotics tools; the Execution diagram now branches to IK / motion planning, controller code, VLA / learned policy and WAM, with perception/state feedback.
- Added a brief RPent example using its original framework figure and verified tool names; ROSA / ROS-MCP remain short adjacent examples.
- Added Other Applications as Chapter 4, beginning with an artifact/validation diagram and covering hand structural design and ASPIRE program debugging.
- Published 26 English slides with synchronized Chinese narration, four chapter-opening diagrams and concise chapter summaries; retained all 15 embedded videos and the 60-minute target.
### Design Rationale
- Separate how tools are packaged from evidence about what different interfaces enable. Retain only three deep studies rather than expand into a toolkit survey.
- Explain interface advantages before limitations; distinguish synthesis and architecture scope from tested integrations and measured outcomes.
- Preserve Noto Serif / Noto Sans, the white/teal visual language, original imagery and unified controls.
### Notes & Caveats
- RPent code was inspected read-only at `3fcf4b3645d2210c629974232c6182b5b7f98cc5`. Its illustrated tool sequence is not a newly executed robot experiment; `move_to` uses OSC, not IK. The pinned README does not mark DreamZero supported.
- The hand remains an unvalidated design artifact. Other Applications is not a mutually exclusive taxonomy or a fourth benchmark.
- The single HTML embeds all media, four fonts and narration. All 26 layouts and 15 video controls were checked, along with script navigation, figure enlargement, focus view and 390 px control layout. Native fullscreen was unavailable in the embedded preview; the focus-view fallback worked.
- Historical 22-slide PPTX/PDF/ZIP outputs are unchanged and do not match this page order.

## [0.3.1] - 2026-09-10
### Features
- 三章流程图移到章节开头（第 5、11、16 页），保持 24 页和全部 15 段内嵌视频。
- 中文讲稿同步改为章首导读、案例展开、章末简短总结；更新页码、时间表和素材清单。
### Design Rationale
- 先建立章节结构再读案例，避免观众看完实验才得到整体流程。
### Notes & Caveats
- 保留现有字体和按钮样式；HTML 与讲稿同步验证，历史 22 页文件不变。

## [0.3] - 2026-09-10
### Features
- 单文件、全内嵌 HTML；24 页英文幻灯片与同步中文讲稿。
- 三章分别加入 synthesis 框图与 Evidence / Still open 小结。
- 统一按钮与窄屏布局，增加整篇讲稿阅读和原图放大，保留 15 段视频。
### Design Rationale
- 用章节内收束和明确过渡替代末尾集中总结，仍只细讲三个标杆。
- Native HTML 文本与图形保留可编辑性；视频按页解码，避免一次初始化全部影片。
### Notes & Caveats
- 大 HTML 约 115 MB，建议桌面浏览器；引用链接联网，但演讲运行不需要网络。
- 旧 22 页 PPTX/PDF/ZIP 保留，不与新版逐页对应。
- 不支持原生全屏的内嵌预览器使用专注视图。

## [0.2] - 2026-09-10
### Features
- 22-slide English focused talk with three deep case studies, 15 embedded videos/GIF conversions, original research figures and editable synthesis diagrams.
- Detailed speaker notes, static PDF preview and portable offline player.
### Design Rationale
- Replace broad paper-by-paper coverage with fewer case studies and media-led explanation after user feedback.
- Preserve the previous Steerable VLA talk’s actual local typography and visual identity.
### Notes & Caveats
- Demonstration footage and measured research evidence remain explicitly distinct.
- PDF is static; browser playback passed for every clip, while PowerPoint-native playback still needs a pre-talk check on the presentation computer.
