# Changelog

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
