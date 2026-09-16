# Revision0.6 — final review

Baseline: Git3e64b1f; final HTML SHA-256 `e4e8c9c571b8c7304364705c7a054d705c3ab1814a5b006d6a64e131570b2cf2`. Public sources only; no source experiments reproduced.

## Standards
Reviewer reported no actionable Standards findings. Existing source-generated workflow, fonts/style, language separation, sparse28slides/three deep cases and evidence boundaries preserved. No scoped code-smell refactor required. `git diff --check` passed.

## Spec
First pass: oneP2. Direct/Hybrid narration could imply causality from two differently configured suites. Fixed by replacing winner-reversal phrasing with reported orderings, making complementarity/prior mismatch explicit hypotheses, and adding action-segment/decision-budget/pairing limits. Replaced vertically paired stat blocks with a full-width table; both videos clearly labelled RoboDojo simulation. Reviewer recheck closedP2; no remaining findings or scope creep.

Summary: Standards0findings; Spec1resolved,0open.

## Narrative and visuals
Every chapter opens with its diagram and closes with a short takeaway. First chapter tests action responsibility rather than assuming delegation; third chapter separates weights/code/knowledge. All28slides rendered in Chrome and visually reviewed; page8table separates suite results from selected videos. Original figures remain uncropped, with enlargement; controls preserved on desktop and390px mobile.

## Functional verification
-28slides,21clips,35embedded image assets,4font faces;801required CJK glyphs covered.
-21clips play, pause stably and restart; retained bytes match source manifests.
-HTML and independent Chinese script match; no external runtime resources; isolated directory contains only byte-identical HTML.
-Chapter navigation, Home/End, focus/fullscreen, figure dialogs including the new RoboRSI figure, current/full-script modes and mobile controls pass.
-60minutes remains a target including9minutes of footage; rehearsal duration is not measured.

Authorities: `.build/standalone_delivery_audit.json`, `.build/standalone_visual_audit.json`, browser auditJSONs.
