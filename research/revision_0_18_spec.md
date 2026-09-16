# v0.18 — ENPIRE and the RSI question

## Authority and scope
- Fixed baseline: `.build/revision_0_18_baseline`, verified against v0.17 final manifest, including P21 wording follow-up.
- Preserve the content/scripts/media of baseline slides 1–21. User follow-up adds one Control demo page immediately after baseline P8; subsequent pages renumber. Preserve closing content, renumber only.
- Third chapter remains a single representative study: ENPIRE (the official spelling of the user's EMPIRE).
- Remove the active CAD + RL preview and unrelated physical ICL clip. Retain historical source files.
- Use official original figures, official task/reset/verification/fleet videos, English slides and Chinese script with English technical terms. All media and fonts stay embedded.

## Narrative and layout
9 simulation puzzle demos (Rubik cube + claw).
23 chapter flowchart; 24 original two-stage architecture; 25 reset and verification;
26 policy/code versus gradient-based improvement; 27 idea tree; 28 physical results;
29 fleet scaling; 30 RoboCasa results; 31 official task demos;
32 experience transfer and RSI bridge; 33 resource cost; 34 chapter summary / RSI question;
35 Takeaways; 36 Thank You.
Claw is a kinematic replay with ideal grasps, not validated contact dynamics. Cube interfaces and conditions must follow its original project, not the Awesome summary alone.

Keep Noto fonts, white canvas, teal `#2ba39b` / dark teal `#1d7d76`, pale `#eaf5f3`,
gray `#646464` and quiet red `#aa514a`. Diagrams encode actual interfaces and feedback.
Few words, large original media. No decorative scientific graphics.

## Evidence contract
- ENPIRE §2 / Figure 2: human-assisted environment construction precedes autonomous PIRE.
- Fixed safety, reset, verifier and evaluation contract during policy improvement.
- PI changes heuristic code or training recipe/weights; it does not update the coding foundation model.
- Preserve exact pinned Figure 3 / Figure 6 / Figure 7 results and uncertainty.
- Physical pass@8 uses conditional retries, not iid sampling or pass@1 precision.
- RoboCasa: once-per-episode script, matched fixed settings, no reset/retry/oracle APIs.
- §3.4 + Appendix B.1: pin autoresearch is distilled into a written recipe for GPU insertion;
  no raw prior trajectories/checkpoints/hidden logs are carried over. The GPU demo illustrates
  the target task, not an ablation proving transfer gains.
- RSI means Recursive Self-Improvement in this talk's discussion. Policy improvement is established;
  recipe/memory reuse is a partial bridge. Improved ability to improve future tasks under fixed
  compute and held-out evaluation remains unproven here. No claim of self-improving LLM weights,
  open-ended acceleration or solved autonomous lifelong learning.
- RoboRSI September 2026 report and DGM provide brief conceptual context in notes/citations only,
  not new paper deep-dives or mixed result tables.
- Official video playback speed is a player setting. Encode explicitly documented presentation
  speedups, preserve each complete chosen file without cutting failed attempts, and record source
  duration, derived duration and hashes. No independent experiment reproduction.

## Verification
Source/hash and semantic regressions, full build/font cycle, isolated-copy static audit,
all-slide layout/media/UI/mobile checks, complete playback of all seven new clips,
visual inspection of third chapter and controls, Standards/Spec review against this fixed baseline.
No push, release, PPTX/PDF/ZIP regeneration or ENPIRE execution.

## Review corrections
- P8 transition explicitly points to the new puzzle page, not the former interface page.
- P3 roadmap uses “ENPIRE + reusable research experience” instead of the removed training/ICL demo description. Only these two exact text replacements are permitted by baseline preservation tests.
