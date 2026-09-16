# v0.8 delivery review

2026-09-14 · final HTML SHA-256 `01505a9c7b51801eb5593b8113fcd3a3b21ca05053e2c79122977d08b9b3b868`.

## Scope and fixed comparison

Implements `revision_0_8_spec.md` and the three user-approved same-day proposals.
Comparison is the 22 saved files in `.build/revision_0_8_baseline/` plus the new v0.8 assets, clip preparation, scope and supplemental QA files. All baseline hashes verified. Git HEAD predates the verified baseline and is not substituted for it. No new commits or release.

Review used Matt Pocock's two-axis workflow with parallel Codex-native Standards and Spec reviewers. No Claude / Anthropic service was invoked.

## Standards

- Original **P2**: main builder gained a Pillow dependency not stated in recovery instructions. Fixed in `AGENTS.md`: Pillow must belong to the main interpreter, with an available bundled-Python fallback. The fallback independently imports Pillow 12.3.0.
- Original **P3**: S09 `current_use` still said no quantitative result. Updated to the actual LIBERO-40 results and page roles; exact `active_slides` mappings and all cited URLs independently checked.
- Follow-up review closed both. No actionable code-smell finding or offline/media mapping regression.

## Spec

- Original **P2**: slide 12 dropped its simulation / omitted-LLM-waiting labels. Captions, footer and Chinese playback cue now state these limitations.
- Added a regression requiring the labels and the control-time/latency cue. It failed on the old candidate exactly at the new assertion, then passed after rebuilding and refreshing the font subset.
- Follow-up verified the generated final-hash slide and closed the finding. Control's expanded sequence is explicitly approved; the three hierarchy figures, RPent role, action-budget caveats, report OR branch, Real2Sim judge rule and ENPIRE protocol were confirmed.

Summary: Standards **2 original findings, both closed** (worst original P2); Spec **1 original finding, closed** (P2). No unresolved findings in either axis.

## Narrative and visual design

- 28 English slides / 18 embedded clips; Chinese embedded and external narration agree.
- Control 4–13, Simulation 14–19, Improvement 20–26, Beyond / closing 27–28. Overview diagrams open 4/14/20; summaries close 13/19/26.
- Hi Robot / Helix / Helix 02 share one page, with concise interface labels. Original report architecture remains on slide 12.
- ENPIRE idea tree is the complete original Figure 12, including no-gain nodes and the best-score curve; short right-side callouts explain actual changes. It is not depicted as a causal ablation.
- Original figures and player controls preserve the Noto / white-teal design. Figures 5 and 23 were enlarged/rebalanced after first visual inspection. Figure detail remains available in the enlargement dialog.
- Sequential 1-second samples of the entire keyboard / Office / quadruped excerpts were inspected. Keyboard shows backspace and a retry that still holds the key too long, not guaranteed mastery. Office shows the finished simulation; quadruped retains partial / failed evaluation labels.

## Verification

Static and browser-bound validation passed for the final hash: no external runtime resources, identical embedded media, 33 image/poster assets, four font faces, all 28 Chinese script headings and 696 covered glyphs. Desktop text overflow and mobile button overflow are zero. All 18 clips passed play/pause/restart, plus keyboard navigation, chapter jumps, focus/fullscreen, figure dialogs and script controls.

All 28 slide renders and desktop/390px controls were inspected. Screenshot hashes and full-size figure review are recorded in `.build/standalone_visual_audit.json`, bound to this final hash.

Supplemental audit passed for the final hash: all five new clips reached ended=true with decoded frames and no errors. Streamed HTTP bytes before/after the run match delivery; the actual loaded deck-data DOM also matches. Seven enlarged original-figure captures are complete. The repaired supplemental audit received a final Standards check with no new finding. See `.build/v0_8_extended_audit.json`.

Python compilation, Node syntax checks and `git diff --check` passed. Initial connection-refused attempts before starting loopback were not passes. Supplemental QA first encountered Chromium response-cache eviction for the 132 MB document, then a failed route-fulfillment workaround; neither altered the artifact or counted as verification. The repaired audit streams HTTP hashes outside CDP and independently hashes the actual loaded deck-data DOM.

## Boundaries

No experiments were reproduced. Media decode/playback and sampled visual inspection are distinct; no claim of inspecting every source-video frame or the full five-minute Office original. Sixty minutes is suggested pacing, not measured rehearsal. Historical PPTX/PDF/ZIP were not regenerated. Preserved unrelated dirty work and prior outputs; no push or Release.
