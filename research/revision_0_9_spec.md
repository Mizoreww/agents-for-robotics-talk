# v0.9 — inspectable experimental results

Date: 2026-09-14. User request: add results tables to Control, explicitly including RoboDojo and RoboLab, and supplement the later chapters too. This supersedes v0.8 only where results coverage expands.

## Preserved baseline and deliverable

- Fixed comparison: `.build/revision_0_9_baseline/manifest.json`, the verified v0.8 snapshot, not older Git HEAD.
- Single fully embedded HTML, English slides and synchronized Chinese script with English technical names.
- Preserve Noto typography, white/teal style, player controls, all 18 clip payloads and all existing original figures.
- Chapter overview diagrams remain first. Chapter summaries remain. No new unrelated paper or community demo.
- 36 pages: 8 additional evidence pages; existing Claude, Robocurve and ENPIRE cost pages gain native tables. Suggested total remains 60 minutes, not rehearsed.
- No public release, push, new PPTX/PDF/ZIP, source experiment replication, or Claude/Anthropic service invocation.

## Page order

| Pages | Role |
|---|---|
| 1–3 | Existing introduction |
| 4–6 | Original Control diagram; combined Hi Robot/Helix/Helix 02 architectures; Hi Robot original results + average table |
| 7–10 | Claude interfaces and results; RPent framework and its Harness VLA same-checkpoint comparison |
| 11–14 | Robocurve two-task model results with existing clips; community demos; Asim interface clips + complete three-task matrix |
| 15–18 | Anonymous original Direct/Hybrid architecture; separate RoboDojo and RoboLab tables; Control summary |
| 19–25 | Simulation overview, paired clips, Real2Sim method, original result figure, all-backend table, Astra demos, summary |
| 26–34 | Improvement overview, ENPIRE method, reset/verifier, idea tree, pin curves, two-physical-task table, RoboCasa baseline figure/table, Astra demos, resource table + summary |
| 35–36 | Structural design and closing |

## Evidence requirements

1. **Hi Robot**: original complete Figure 5 plus four author-displayed cross-task averages. IA/TP measure commands/objects, not binary episodes. Three domains × 20 trials per method. Training-data differences remain visible. Helix sources have no disclosed repeat-trial success table; do not invent one.
2. **Claude**: retain both original plots and their different axes. Table shows Opus 4.6 Direct 3.5%, supervised 76%, MolmoAct alone 86%; 40 tasks × 5 seeds per condition.
3. **RPent/Harness VLA**: v4 Table 3, same frozen π0.5-SFT checkpoint. Aggregate by instruction redirection (400), position swap (400), total (800). Counts derived from cells, not raw logs. Seed-0 exploration memory, held-out seeds 1–10, extra planning/analytic compute. No unrelated leaderboard or renamed Astra planner.
4. **Robocurve**: all 2 tasks × 3 models, 20 attempts per cell; direct EEF/IK, no VLA. Different bowl rigs, later Astra trials, unblinded grading, 20-call cap; no pretraining-cause claim.
5. **Asim**: all 3 tasks × 7 conditions, including script/random and observation variants. ΔEEF is OSC_POSE, not q. Unequal control/query budgets and enriched proprio visible.
6. **RoboDojo**: all 10 selected tasks, Direct and Hybrid separately; five aligned cases each. Totals 13/50 and 24/50 mechanically recounted. Direct Score N=48 vs Hybrid N=50, success N remains 50 each. Prior/interface/horizon co-vary.
7. **RoboLab**: all 10 tasks and 5 methods, selected final slots. Retained history + authorized retries; states unpaired, two Direct BlocksInBin retries 180→500 decisions. Historical baselines take first five June episodes including failures. Task versions/settings not verified identical. Never pool with RoboDojo or call this fresh uniform-budget comparison.
8. **Real2Sim**: all four backends, accepted/partial/failure counts summing to 100, model-call bill for the run. Any-judge best-candidate threshold, up to five candidates. Partial=7, failed≤6 or no valid record. Model bill excludes perception/simulation/preparation; replay is not predictive validity.
9. **ENPIRE physical**: official plot means for Push-T @8h (normalized score) and Pin @4h (SR), three coding agents, original complete Figure 3. Four displayed traces, not four asserted independent replications; no pooled binary count. Up to eight conditional retries; metrics and policy families differ.
10. **ENPIRE RoboCasa**: original Figure 6, GR00T N1.5 / CaP-X* / ENPIRE comparison. No estimated percentages from bars. Forty fixed episodes per reported evaluation, one script execution, no reset/retry/oracle APIs. Eight task images do not establish 320 pooled trials.
11. **ENPIRE resources**: retain original Figure 7; 1/4/8 pair mean ± official std for per-robot active time, GPU active time and fleet tokens/min. Do not label std as CI. Figure 7 time-to-success must not be mixed with Figure 3's pin near-perfect time.

## Authority and verification

- Research: `control_background_results_2026-09-14.md`, `data_improvement_results_2026-09-14.md`, and existing anonymous/Asim source audits.
- Machine-readable table values: `research/results_v0_9.json`, built by `.build/derive_results_v09.py` from frozen source files and checked transcriptions. Independently frozen identities live in `research/results_v0_9_sources.json`; normal derivation must reject drift, never refresh this manifest. All source SHA-256 values are verified during build.
- `.build/test_results_v09.py` must reproduce the result authority and reject drift in every source, including a valid-JSON 76→77 Hi Robot mutation, before any output publication.
- Table layouts: `.build/results_slides_v09.py`; source builder remains `.build/build_selfcontained.py`.
- Static validator checks every table cell, required caveats, page/clip mapping, font glyphs, Chinese script identity, single-file isolation and all payload hashes.
- Full Chrome layout/playback/UI/mobile audits, screenshots of every page, enlarged original figures; independent review of all new table pages at presentation resolution.
- Matt Pocock Standards and Spec reviews against preserved v0.8. Findings must be resolved before delivery. Latest hash-bound audit files, not prose alone, determine completion.
