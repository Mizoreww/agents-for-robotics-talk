# Robotics Agents Talk — Current Delivery State

## Active scope
- Workspace is not a Git repository. Reference project unchanged.
- 28 English slides; Chinese speaker script with English proper nouns and technical terms.
- Three deep cases only: Claude Plays Robotics, Agentic Real2Sim, ENPIRE. Show-Harness, RPent and ASPIRE are supporting examples; community demos are application evidence.
- Self-contained HTML is authoritative. Preserve older 22-slide outputs as history.

## Current revision (0.5, 2026-09-11): three parts, short titles, community clips
1. Three parts named after the Agent's role: Agent Controls Robot (5–14), Agent Produces Data (15–19), Agent Post-trains Robot (20–26); each opens with its synthesis diagram. ASPIRE moved into Part 3; the hand design is one closing slide (27) outside the three roles; conclusion on 28.
2. Every title ≤ 40 characters. Chinese script rewritten for all 28 slides with the three-part framing.
3. Six community clips added from X and 小红书 (Yanjie Ze Rubik's Cube in MuJoCo, Wenli Xiao human video → arm, ARX knob, Show-Harness excerpt, MuJoCo juggling, 小红书 Piper carrot pick-and-place); wiping removed. 20 clips, 60-minute target.
4. New slides: Demo: Zero-shot Real Arms (10), Demo: Dexterity in Simulation (11), Harness: Semantic Actions (12, Show-Harness Table 2 numbers), Gaps and Directions (14). Evidence notes in `research/community_demos_2026-09-11.md`; sources S25–S36 in `research/sources.json`.
5. Static checks pass (`validate_standalone.py --static`): 28 slides, 20 clip hashes, offline closure, script equality, 815 required CJK glyphs covered. WeasyPrint render of all 28 pages inspected for the changed layouts.
6. Browser audits pass for the current HTML hash: layout (no text overflow, all images loaded), playback (all 20 clips play, pause stably and reset), UI (three chapter transitions, Home/End, focus view, figure dialog, both script views) and the 390 px mobile layout. They are produced by `.build/browser_audit.mjs` (Playwright driving Google Chrome) and bound to the hash in `.build/standalone_delivery_audit.json` (`browser_audits`).

## Previous revision (0.4.1): direct actions to RPent — completed
1. Chapter diagram kept with a direct q / EEF Pose branch; Chapter 1 reordered to direct actions → interface comparison → VLA → real demos/limitations → RPent.
2. Grounded strengths/limitations in retained sources; distinguished long-horizon planning potential from proven long-horizon reliability.

## Earlier revisions — completed
- 0.4: Agent → multiple Agent Tools diagram; RPent ecosystem slide; Other Applications chapter; 26 slides.
- 0.3.x: single self-contained HTML; chapter-opening diagrams; unified controls; 24 slides.
- 0.2: 22-slide focused talk with three deep cases and 15 clips.

## Primary outputs
- output/Agents_for_Robotics_Self_Contained.html
- output/Speaker_Script_Revised.md
- output/README.md

## Important boundaries
- No Claude or Anthropic service/agent invocation for content. Public reports/media only.
- No cross-paper percentage leaderboard. Social demos remain qualitative; the numbers on slide 14 come only from cited evaluations (Robocurve, Claude Plays Robotics, HumanCLAW single run, one RoboDojo run). The Show-Harness Table 2 cross-task averages sit on slide 12.
- Agentic Real2Sim measures replay acceptance; exact any-judge candidate rule retained.
- ENPIRE performance includes its reset and conditional-retry protocol.
- Microphone footage is a kinematic replay after dynamics failure. Hand footage is an unvalidated design artifact. Yanjie Ze's cube solve is a MuJoCo physics replay; learned-vs-scripted motion is not stated.
- Native OS fullscreen did not activate in the embedded preview; the compatible focus-view toggle is implemented.
- Browser file:// navigation is blocked by app policy; test on loopback from `.build/standalone_isolation`. CSP prohibits external runtime requests.
- RPent is a separate RLinf organization repository, not a VLA backbone. Architecture artwork is broader than confirmed integrations; DreamZero is not marked supported. `move_to` uses OSC, not IK.

## Private production and audits
- .build/build_selfcontained.py, standalone_shell.html, standalone_player.css, standalone_player.js
- .build/script_revised.md (Chinese authority)
- .build/prepare_clips_v2.py, clip_manifest_v2.json, community_downloads.json (2026-09-11 clips)
- .build/build_cjk_font.py (CJK subset from the generated script, slide text and player UI)
- .build/validate_standalone.py (`--static` for static-only checks)
- .build/render_static_revision.py → three_parts_static_preview.pdf, three_parts_static_rendered/
- .build/standalone_*_audit.json (browser audits bound to the HTML hash)
- .build/prior_four_chapters/ holds the 0.4.1 build inputs and docs.

## Historical material
Older 22-slide PPTX/PDF/ZIP/English notes remain unchanged in output. The 36-slide survey remains private and is not an active deliverable.
