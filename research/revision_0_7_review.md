# v0.7 delivery review

2026-09-14 · final HTML SHA-256 `cccec9692b6470391539624e016cce0ee7860c3b0f4ebb8c3b0b8ac315cbd602`.

## Scope and fixed comparison point

`revision_0_7_spec.md` records the user-directed simplification. Compare editable sources to the verified v0.6 snapshot in `.build/revision_0_7_baseline/`, not only to the older Git HEAD. The saved HTML remains local and ignored. Review used the Matt Pocock two-axis workflow with Codex-native reviewers; no Claude/Anthropic service was invoked.

## Standards

Original finding [P3]: the image audit contained hashes for images removed from the actual delivery. Fixed by filtering records to used assets; the validator now asserts exact equality between image-audit hashes and embedded asset keys. All 17 delivered assets are covered and no removed asset is reported as embedded. The follow-up review closed this issue.

The follow-up also noted that delivery status still said pending after browser completion. The full validator was subsequently rerun successfully and now records passed for the final hash.

## Spec

Original finding [P2]: the RPent background carried an unverified IK label, whereas the inspected motion example uses OSC. Changed the generic service label to Motion; added a regression rejecting the old label. The follow-up review closed this issue.

The reviewer verified the chapter spine, one-study-per-chapter scope, Direct/Hybrid inputs and OR branches, segment-length confounding, Real2Sim judge rule and ENPIRE conditional retries. Chinese external/embedded scripts agree. No remaining content finding.

Summary: Standards 1 original finding (P3), closed; Spec 1 original finding (P2), closed. Both follow-ups identified the same pending-status housekeeping item, now resolved by the full validator.

## Narrative and visual review

- 21 English slides, 9 embedded clips, 17 image/poster assets and 4 embedded font faces.
- Introduction 1–3; Control 4–8; Data 9–13; Improvement 14–19; other application / closing 20–21.
- Control background 5 names Claude Plays Robotics and RPent only. Robot-data training is a premise-changing possibility, not proof of Astra's undisclosed pretraining recipe.
- Every chapter opens with its diagram and ends with a bounded summary. The original anonymous control architecture is legible in the enlargement view; the source image is unchanged.
- All 21 final slide renders, desktop/390px controls and architecture enlargement were visually inspected. Original result axes and legends remain visible. Screenshots and hashes are in `.build/standalone_visual_audit.json`.
- Opened content remains a presentation rather than a cross-paper leaderboard. The two RoboDojo videos are different-task illustrations; hand remains an unvalidated CAD application.

## Verification

Static validation and final browser-bound validation passed. All 9 clips passed play/pause/restart checks. UI checks cover chapter jumps, keyboard navigation, presentation view, figure dialogs, 21 Chinese-script headings and mobile controls. No text overflow, missing image or mobile-button overflow was detected. The HTML in the one-file isolation directory is byte-identical to the deliverable.

Python compile checks for the changed build/validator/render sources and Node syntax checks passed. `git diff --check` passed. During final QA the loopback server had stopped after a turn interruption; it was restarted, and fresh browser audits were run to completion. The failed connection attempt is not counted as a pass.

## Boundaries

60 minutes is suggested pacing including discussion, not a measured rehearsal. No original research experiments were reproduced. Historical PPTX/PDF/ZIP were not regenerated and no release was published. Retained clips are byte-identical to the v0.6 authorities; removed clips and research sources remain archived. Current user-facing outputs are the HTML, Chinese script and `output/Chapter_Spine.md`.
