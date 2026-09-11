# Changelog

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
