# Robotics Agents Talk — Current Delivery State

## Active scope
- Workspace is not a Git repository. Reference project unchanged.
- 26 English slides; Chinese speaker script with English proper nouns and technical terms.
- Three deep cases only: Claude Plays Robotics, Agentic Real2Sim, ENPIRE.
- Self-contained HTML is authoritative. Preserve older 22-slide outputs as history.

## Current revision: direct actions to RPent — content/static checks complete; browser retest unavailable
1. Preserve the chapter-opening diagram and add a direct q / EEF Pose action branch, separate from Agent Tools and still connected to the execution/servo stack.
2. Keep 26 slides and all media; reorder Chapter 1 to direct actions → interface comparison → VLA → real demos/limitations → RPent synthesis.
3. Ground semantic/task-decomposition strengths, physical-control limitations, and model/interface trends in the retained sources; distinguish long-horizon planning potential from proven long-horizon reliability.
4. Synchronized Chinese narration, media mapping, 60-minute timing, evidence notes and order assertions. Static checks pass for 26 slides, all 15 video hashes, offline closure and script equality. The final Chinese font covers all 733 required glyphs, including generated source headings.
5. Rendered 26 pages with a static print engine and inspected the changed layouts. The application Browser webview could not attach; current playback, responsive and interaction retests remain unavailable, not passed. Previous browser audits retain their old HTML hash and are not evidence for this revision.

## Previous revision: tool ecosystem and broader applications — completed
1. Replace the first chapter's single-controller diagram with Agent → multiple Agent Tools, including IK, VLA, WAM, controller code, and perception/state tools.
2. Ground interface advantages and limits in Claude Plays Robotics; identify IK and WAM as extended examples, not additional arms of that report.
3. Add a fourth chapter opening for Other Applications, reclassify the hand as structural design, retain ASPIRE as a debugging demonstration, and update opening/conclusion narration.
4. Added one brief RPent ecosystem slide with its original framework figure and a concrete tool sequence; ROSA / ROS-MCP are short adjacent examples. This is not a fourth deep case study or a new robot trial.
5. Kept all 15 embedded clips, original imagery and typography. Synchronized 26-slide navigation/script/timing; all four chapters begin with diagrams at 5, 12, 17 and 23, with spoken summaries at 11, 16, 22 and 25.
6. Rechecked every rendered slide, all 15 clips (play, stable pause, restart), current/full script, figure enlargement, focus view, Home/End and chapter transitions against the current HTML hash. The 390 px mobile layout has no horizontal button overflow; all 736 Chinese script characters are covered by the embedded font.

## Previous revision: chapter openings — completed
1. Moved the three synthesis diagrams to slides 5, 11 and 16; retained 24 slides and all 15 clips.
2. Rewrote Chinese chapter previews and retained concise closing takeaways on slides 10, 15 and 21.
3. Rebuilt the embedded Chinese font and standalone HTML, synchronized the script and page references, and reran order/media/layout/control validation against the current HTML hash.
4. Rechecked all 24 slide layouts and all 15 clips, including play/pause/restart. The 390 px viewport has no horizontal button overflow. Current script and full script follow the new order; focus view and figure enlargement still work.

## Completed before this revision
1. Recovered source snapshots, media and reference typography without repeating acquisition.
2. Audited the full question–method–evidence–limitation argument and all chapter transitions.
3. Added four chapter-opening diagrams on slides 5, 12, 17 and 23; the first explicitly branches to multiple Agent Tools.
4. Rewrote a speakable Chinese script with media cues, figure walkthroughs and transitions; embedded the same text in HTML.
5. Built native HTML text/diagrams with original paper images, 15 embedded video clips, Noto Serif / Noto Sans and a subsetted Chinese font.
6. Unified every control, including active/disabled/focus states, figure close and script mode controls. Fixed narrow-screen native-select overflow.
7. Inspected all 26 rendered slides and checked text/image layout. Tested all 15 video clips for time advancement, stable pause and restart.
8. Verified isolated-file completeness, all media hashes, script equality, embedded Chinese glyph coverage and responsive button bounds.

## Primary outputs
- output/Agents_for_Robotics_Self_Contained.html
- output/Speaker_Script_Revised.md
- output/README.md

## Important boundaries
- No Claude or Anthropic service/agent invocation. Public reports/media only.
- No cross-paper percentage leaderboard. Social demos remain qualitative.
- Agentic Real2Sim measures replay acceptance; exact any-judge candidate rule retained.
- ENPIRE performance includes its reset and conditional-retry protocol.
- Microphone footage is a kinematic replay after dynamics failure. Hand footage is an unvalidated design artifact.
- Native OS fullscreen did not activate in the embedded preview; the compatible focus-view toggle is implemented and tested. No claim of PowerPoint-native playback.
- Browser file:// navigation is blocked by app policy. The previous delivery was tested on loopback from a folder containing only the HTML; CSP prohibits external runtime requests.
- RPent is a separate RLinf organization repository, not a VLA backbone or a renamed training algorithm. Architecture artwork is broader than confirmed integrations; DreamZero is not marked supported in the pinned README. `move_to` uses OSC, not IK.

## Private production and audits
- .build/build_selfcontained.py, standalone_shell.html, standalone_player.css, standalone_player.js
- .build/script_revised.md (Chinese authority); script_revised_english_prior.md (superseded draft)
- .build/standalone_*_audit.json and standalone_rendered/
- research/talk_narrative_review.md records the editorial/evidence review.

## Historical material
Older 22-slide PPTX/PDF/ZIP/English notes remain unchanged in output. The 36-slide survey remains private and is not an active deliverable.
