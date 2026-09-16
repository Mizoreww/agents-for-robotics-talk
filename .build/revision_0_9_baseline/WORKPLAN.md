# Agents for Robotics — current work

## Revision 0.8 · 2026-09-14

Implements the three user-approved proposals: expanded Control spine, clearer Data / Improvement logic, and Astra demos within chapters. It supersedes v0.7's single background-page constraint, not its evidence standards.

- [x] Preserve verified v0.7 and 22 hash-bound baseline files.
- [x] 28 English slides / 18 embedded clips; unchanged Noto fonts and player style.
- [x] Control 4–13: original overview, combined hierarchy figures, Claude experiments, RPent, Astra capability / interfaces / Hybrid, summary.
- [x] Simulation 14–19: Agentic Real2Sim with DROID-100 protocol, Astra workflows and replay/prediction summary.
- [x] Improvement 20–26: ENPIRE with fixed environment, reset/verifier, original idea tree, curves, demos and resource summary.
- [x] Chinese narration and chapter spine; current source registry and documentation.
- [x] Final hash-bound static/browser/visual gates and two-axis review closeout.
- [ ] Rehearse timing before 2026-09-16.

## Outputs and comparison point

Current HTML SHA-256: `01505a9c7b51801eb5593b8113fcd3a3b21ca05053e2c79122977d08b9b3b868`.

- `output/Agents_for_Robotics_Self_Contained.html`
- `output/Speaker_Script_Revised.md`
- `output/Chapter_Spine.md`
- `.build/standalone_delivery_audit.json` and `.build/standalone_visual_audit.json`: actual verification state.

Fixed baseline `.build/revision_0_8_baseline/`; do not compare only to older Git HEAD. Requested scope: `research/revision_0_8_spec.md`. Review findings: `research/revision_0_8_review.md`.

Only Codex-native review; no Claude/Anthropic services. No training/benchmark replication. Preserve historical outputs and unrelated dirty work. No release publication or push.

Build → refresh font subset → rebuild → isolation copy → static checks → browser playback/layout/UI/mobile → full validator → hash-bound visual record. Use bundled Node and H.264-capable Chrome as in `AGENTS.md`.

Final result: Standards 2 original findings and Spec 1 original finding, all closed. Static / browser / visual audits and the five-new-clip complete-playback audit pass for the current hash. No experiment reproduction or measured rehearsal is claimed.
