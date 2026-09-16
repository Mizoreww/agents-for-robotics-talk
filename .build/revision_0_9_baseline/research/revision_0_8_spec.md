# v0.8 — implementation and acceptance scope

2026-09-14. Implements the user's approval (“可以 开始吧”) of the Control,
Data / Improvement and Astra demo proposals from the same date. These latest
approved proposals supersede v0.7's brief Control background restriction.

## Fixed baseline

Compare against `.build/revision_0_8_baseline/`, whose `manifest.json` freezes
22 pre-edit files. The verified v0.7 HTML hash is
`cccec9692b6470391539624e016cce0ee7860c3b0f4ebb8c3b0b8ac315cbd602`.
Git HEAD is older than this baseline and must not stand in for it during review.
No commit, push or release is authorized by this revision.

## Delivery and design

- One portable HTML with all figures, videos, fonts, player and script embedded;
  no external runtime requests. Edit `.build/` sources, not generated HTML.
- English slides; natural Chinese narration with English technical names.
- Preserve Noto Serif / Noto Sans / Noto Sans CJK SC, white/teal identity,
  original logos and accessible, attractive controls.
- Chapter overview diagrams come first. Original figures retain their evidence,
  aspect ratio and click-to-enlarge behavior. Keep titles at most 40 characters.
- Sparse slides: a main figure or video group, with necessary protocol caveats;
  detailed explanation belongs in the narration.
- 28 slides, 18 clips; 60 minutes is suggested pacing, not measured rehearsal.

## Approved order

| Slides | Content and purpose |
|---|---|
| 1–3 | Opening, painting demonstration, three distinct Agent roles |
| 4 | Original Agent → direct q / EEF or Agent Tools → robot overview, feedback retained |
| 5 | Hi Robot, Helix and Helix 02 original figures together; language / latent / joint / low-level interfaces |
| 6–7 | Claude Plays Robotics interfaces, concrete LIBERO-40 protocol and original result panels |
| 8 | One original RPent framework figure; tool organization, not another benchmark survey |
| 9–10 | Astra Direct real-robot evidence, then plug / keyboard community demos |
| 11 | Same-Astra ΔEEF / waypoint / code comparison, unequal budgets visible |
| 12 | Anonymous Direct/Hybrid report's original execution architecture, evidence and clips |
| 13 | Control summary: reassess the division of action generation; no permanent interface winner |
| 14–17 | Simulation overview, real/sim pair, Agentic Real2Sim method and DROID-100 results |
| 18–19 | Astra scene-building demos, then replay versus predictive validity summary |
| 20–24 | Improvement overview, ENPIRE setup / loop, reset / verifier, original idea tree, learning curve |
| 25–26 | Astra RL / physical ICL demonstrations, then ENPIRE cost and chapter summary |
| 27–28 | Structural-design application outside the three roles; final discussion |

Data and Improvement each have exactly one detailed representative: Agentic
Real2Sim and ENPIRE. Control follows the user's explicitly expanded sequence;
do not add unapproved extra studies. Community demos illustrate new work scope,
not extra deep dives or measurements for the papers.

## Evidence contracts

- Hi Robot has two inference levels: VLM → subtask language → π0 → action.
  Helix uses semantic latent; Helix 02 explicitly separates S2/S1/S0. S1 200 Hz
  and S0 internal 1 kHz must not be conflated.
- Claude LIBERO-40: 40 tasks × 5 seeds = 200 trials per condition. Opus 4.6
  Direct 3.5%, supervised 76%, MolmoAct alone 86%. Preserve axes, model labels,
  uncertainty and the baseline; the two plotted y-axis ranges differ.
- RPent is tool organization; inspected `move_to` uses OSC, not assumed IK.
- Astra's stronger demonstrated capability reopens old division-of-work
  questions. Its internal network, robot-pretraining recipe and causal data
  explanation remain undisclosed; do not assert them as established facts.
- Robocurve Direct: absolute EEF + IK, no independent VLA. Bowl 19/20;
  insertion 2/20. Selected clips omit waiting; do not infer latency.
- Asim Square: ΔEEF 1/20, waypoint 18/20, code 16/20, medium reasoning.
  ΔEEF ≤200 steps / 10 queries; waypoint ≤500 / 16; code ≤500 / 3 revisions.
  Waypoint mean 256.6 exceeds the delta step cap. “Proprio” includes visual
  geometry aids. Not a q comparison or controlled representation-only effect.
- Anonymous report: three views, 14D proprio; π0.5 50×14 joint proposal;
  accept 1–15 OR correct EEF 1–5; Direct EEF 1–5. Native control 25 Hz is
  not LLM rate. RoboDojo 13/50 vs 24/50 selected paired cases; prior, interface
  and horizon vary together. Do not pool selected RoboLab final slots.
- Real2Sim: all 100 episodes; 48 accepted / 8 partial / 44 failures. At most
  five eligible candidates; three judges; any judge's best ≥8/10 passes,
  not majority vote. Replay acceptance does not establish predictive validity;
  model-call bill is not total pipeline cost.
- ENPIRE: human-assisted setup, then fixed APIs and success definition.
  Up to eight conditional retries, not one-shot or independent best-of-eight.
  1→8 pairs: >1.5 h→~40 min research time; token costs remain visible.
  Figure 12 includes no-gain nodes: I37 +10.8 pp, I66 +0.9 pp, I76 +1.3 pp
  are one run's best-score trajectory, not independent causal ablations.
- No demonstrated recursive enhancement of the foundation-model improver.
  Training, controller-code revision and in-context adaptation are distinct.

## Community media contracts

Keep attribution, Real robot / Simulation / CAD distinctions, known speedups
and qualitative-evidence status. Keyboard 20×; plug 12×; physical ICL 8× with
existing motion tools and no trial denominator. Office shows the final simulated
scene, not verified construction history or a newly trained locomotion policy.
Quadruped is a 14-second development preview with four separate experts and
visible FULL EVAL NOT MET / partial CUT labels, not nine validated skills.
Hand is an unvalidated CAD/animation design, not a tested physical hand.

## Acceptance

1. Build, refresh Chinese font subset, rebuild and copy exactly one HTML into isolation.
2. Static checks: page order, scripts, sources, byte-identical embedded assets,
   font coverage, CSP, no external runtime dependencies.
3. Browser: all clips play/pause/restart; figures enlarge; keyboard, chapter
   navigation, script controls and desktop/mobile buttons work without overflow.
4. Inspect all final slides, critical original figures full-size, toolbar at
   desktop/390 px and meaningful new video excerpts continuously.
5. Matt Pocock Standards / Spec reviews through Codex-native reviewers only;
   record and close actionable findings. No Claude / Anthropic service calls.
6. Synchronize current docs, source registry and Chinese script; bind final
   browser and visual audits to the delivered HTML hash.

Historical PPTX/PDF/ZIP are not regenerated or represented as current. Public
source reading and record verification are not experiment reproduction.
