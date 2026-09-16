# Agents for Robotics — current work

## Revision 0.7 · 2026-09-14

The user simplified v0.6: one representative study per chapter, with problem → method → experiment → conclusion. This supersedes the old 28-slide / 21-clip plan.

- [x] Reduce to 21 English slides and 9 active clips; retain fonts, controls and Chinese narration.
- [x] Control 4–8: anonymous Direct/Hybrid report, original architecture, exact protocol, RoboDojo results and summary.
- [x] Background 5: Claude Plays Robotics interfaces and RPent services only; no second benchmark story.
- [x] Data 9–13: Agentic Real2Sim only, with full DROID-100 denominator and judge rule.
- [x] Improvement 14–19: ENPIRE only, with setup, immutable APIs, retries and resource cost.
- [x] Chapter diagrams 4/9/14; summaries 8/13/19; qualitative demos 2/20; conclusion 21.
- [x] Chinese chapter spine and synchronized complete speaker script.
- [x] Static rebuild, refreshed CJK font and asset-audit regression checks.
- [x] Final hash-bound browser and visual gates; all 21 slides and 9 clips passed.
- [ ] Rehearse timing before the 2026-09-16 talk.

## Authoritative outputs

- `output/Agents_for_Robotics_Self_Contained.html`
- `output/Speaker_Script_Revised.md`
- `output/Chapter_Spine.md`
- `.build/standalone_delivery_audit.json`: actual verification state, not stale prose.

Current HTML SHA-256: `cccec9692b6470391539624e016cce0ee7860c3b0f4ebb8c3b0b8ac315cbd602`.

## Review and provenance

`research/revision_0_7_spec.md` defines the requested scope. The fixed comparison snapshot is `.build/revision_0_7_baseline/` (previous verified v0.6); it is ignored by Git and retained locally. Standards found stale image-audit records; Spec found an unsupported RPent IK label. Both were repaired and regression assertions added. Final review and visual status belong in `research/revision_0_7_review.md`.

Primary boundaries: no claim about undisclosed Astra robot-pretraining scale; no pure-prior causal attribution; no RoboLab pooling; replay acceptance is not novel-action prediction; ENPIRE retries are conditional, not one-shot or independent best-of-N. No Claude/Anthropic service invocation.

Build → font subset → rebuild → copy to isolation → static check → browser audit → final validator. See `AGENTS.md` for the current runtime. The optional PDF is not regenerated; older PPTX/PDF/ZIP and previous research plans remain historical. This revision is local; no release publication requested.

Final verification: static, browser layout/playback/UI/mobile and manual visual audits all match the current hash. The final full validator has refreshed delivery status from pending to passed. Python compile checks, Node syntax checks and `git diff --check` passed.
