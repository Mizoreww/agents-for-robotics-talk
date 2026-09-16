# Control background: experiment tables (2026-09-14)

Scope: Hi Robot, Figure Helix / Helix 02, and RPent. Primary-source inspection only; no author code, model, planner, training, or evaluation was executed. This note does not change the talk. Paper coordinates below use the latest checked PDFs: **Hi Robot v2** (2025-07-15), **Harness VLA v4** (2026-09-02).

## Recommended use

- **Hi Robot:** one compact 4-row table with Instruction Accuracy and Task Progress, beside its original Figure 5. These are not episode success rates.
- **Figure:** keep the three-architecture background visual. State that the checked Helix / Helix 02 launch articles do not publish system success rates with trial counts; do not manufacture a result table from demo duration or control frequency.
- **RPent:** one 3-row, same-checkpoint **LIBERO-Pro** comparison. Label it **“RPent / Harness VLA — LIBERO-Pro (few-shot)”**. Do not expand into its other benchmarks.

## 1. Hi Robot — exact displayed values, not plot estimates

Primary sources:

- [Official Hi Robot article](https://www.pi.website/research/hirobot), quantitative interactive chart after “Training high-level policy with synthetic data.” The chart exposes the following integer values as text in the official HTML; they were not estimated from bar height.
- [Paper v2](https://arxiv.org/pdf/2502.19417v2), **Figure 5, p.7**; comparisons in §5.1, pp.6–7; metric definitions in **§5.2, pp.7–8**. [HTML Figure 5](https://arxiv.org/html/2502.19417v2#S5.F5).

### Compact slide table: author-displayed cross-task average

| Method | Instruction Accuracy (%) ↑ | Task Progress (%) ↑ |
|---|---:|---:|
| Flat VLA | 36 | 44 |
| GPT-4o high-level + same low-level VLA | 30 | 64 |
| **Hi Robot** | **76** | **81** |
| Expert human high-level (oracle) | 100 | 89 |

**Required table footnote:** `Three real-world task domains; 20 trials per task and method. IA / TP, not episode success.`

Exact field meanings:

- **Instruction Accuracy (IA):** for each trial, the fraction of predicted high-level commands consistent with both the human instruction and current observation. Flat VLA has no readable high-level commands; a method-blind human evaluator infers intent from behavior. Individual command counts are not disclosed, so **do not convert 76% into 46/60 or any other successful-episode numerator**.
- **Task Progress (TP):** fraction of objects successfully placed in their intended locations or configurations. Object-level denominators are not disclosed. This measures partial completion, not whole-task success.
- **Trials:** 20 per task domain per method, across Table Bussing, Sandwich Making, Grocery Shopping (60 trials per method across the three domains). The official website displays an “Average”; retain its rounded values rather than adding spurious precision.
- **Training/comparison condition:** Hi Robot uses a trained high-level VLM plus π0 low-level policy and human-labelled + synthetic interaction data. GPT-4o is not fine-tuned on that dataset but uses the same low-level policy. The main Flat VLA baseline lacks both the high-level model and synthetic data. Thus Figure 5 is **not by itself a data-matched hierarchy ablation**; the paper separately compares a flat policy trained with synthetic data in Figure 8 (§5.4, p.9).
- **Scope:** modified instructions, constraints, and live corrections on three real-world task domains. It supports the value of this trained hierarchy in this setup, not a theorem that every future LLM must invoke a separate VLA.
- **Uncertainty:** the displayed chart does not provide per-method confidence intervals or raw individual trials. Keep integer precision.

### Full source values for verification (do not put all rows on the slide)

| Task | Metric | Flat VLA | GPT-4o high-level | Hi Robot | Human oracle |
|---|---|---:|---:|---:|---:|
| Table Bussing | IA | 36 | 35 | 74 | 100 |
| Table Bussing | TP | 61 | 63 | 77 | 82 |
| Sandwich Making | IA | 34 | 13 | 83 | 100 |
| Sandwich Making | TP | 42 | 56 | 80 | 92 |
| Grocery Shopping | IA | 39 | 41 | 72 | 100 |
| Grocery Shopping | TP | 28 | 72 | 85 | 93 |

Original visual and provenance:

- `research/sources/control_results_20260914/background/hirobot_figure5_original.svg`: **unaltered author SVG**, retrieved from [arXiv](https://arxiv.org/html/2502.19417v2/baselines_v2.svg); 1265 × 344 pt viewBox.
- `research/sources/control_results_20260914/background/hirobot_figure5_pdf_crop.png`: Figure 5 from the original PDF, rendered at 200 dpi and cropped only around the chart. **All four task/average panels, full axes, all baselines, and complete legend are retained**. The caption remains available in the full-page source `hirobot_page7.png`.
- `research/sources/control_results_20260914/background/hirobot_chart_values.json`: extracted official displayed values plus source anchor and metric caveat.
- No authoritative Hi Robot implementation is linked by the checked paper or official article. Do not present a public π0 implementation as the complete Hi Robot code release.

## 2. Figure Helix / Helix 02 — do not invent success-rate rows

| Official source checked | Published demonstration / descriptor | Missing for a quantitative success table |
|---|---|---|
| [Helix launch article](https://www.figure.ai/news/helix), 2025-02-20, “Results” | Collaborative grocery storage; novel-object grasping; author says thousands of novel objects handled | Exact tested set, attempt count, failures, numerator/denominator, comparative success rates |
| [Helix 02 launch article](https://www.figure.ai/news/helix-02), 2026-01-27, “Results” | A 4-minute autonomous dishwasher sequence with 61 loco-manipulation actions; four dexterity demos | Number of complete task attempts, repeat success rate, uncertainty, controlled baseline/ablation table |

This is an absence statement **for these checked official surfaces**, not a claim that Figure has never collected quantitative data. The articles' 200 Hz / 1 kHz, training hours, parameter counts, and 61 actions are not success rates. Helix's schematic “scaling curves” are not a numeric experimental benchmark. The “push exactly 5 ml” example is a task target in a demo, not an error distribution or repeated precision evaluation.

Fresh snapshots: `background/helix.{html,txt}` and `background/helix02.{html,txt}`. Keep these sources as architecture / qualitative evidence and add the one-line disclosure rather than an empty or misleading metric leaderboard.

## 3. RPent and Harness VLA — official identity and one matched setting

### Official relationship (verified in both directions)

1. The [RPent README at commit `328645ee9eeeb24c4cbbff030045e7efcddc4dab`](https://github.com/RLinf/RPent/blob/328645ee9eeeb24c4cbbff030045e7efcddc4dab/README.md#whats-new), **line 46**, calls Harness VLA **“Our first RPent publication”** and links arXiv 2607.08448. Lines 193–202 ask users of **RPent or Harness VLA** to cite that paper.
2. [Harness VLA v4 PDF](https://arxiv.org/pdf/2607.08448v4), **p.1 “Code” and p.2**, links directly to `https://github.com/RLinf/RPent`.

Therefore these are legitimately **the Harness VLA method results published with RPent**, not another unrelated toolkit's results. Do not imply every currently listed RPent backend has been evaluated, or that the entire general framework has one universal success rate.

### Recommended slide table: LIBERO-Pro, same frozen π0.5 checkpoint

Source: **Harness VLA v4 Table 3, p.8**, [HTML Table 3](https://arxiv.org/html/2607.08448v4#S3.T3); §3.1–3.2 and Appendix C.2.

| Method | Success / episodes* | Success rate (%) ↑ |
|---|---:|---:|
| Direct frozen π_RLinf (π0.5-SFT) | 400 / 800 | 50.0 |
| Harness VLA (Codex) | 577 / 800 | 72.1 |
| Harness VLA (CC = Claude Code) | 659 / 800 | 82.4 |

*The integer numerators are **mechanically derived from the eight reported cells, each with exactly 100 trials**; they are not independently recounted from released episode logs. The published overall percentages are retained.

**Required footnote:** `LIBERO-Pro; 8 cells × 10 tasks × 10 held-out seeds. Same frozen π0.5-SFT; Harness VLA uses seed-0 exploration memory (few-shot).`

Protocol and interpretation:

- **Cells:** Spatial, Object, Goal, LIBERO-10; each under **T = instruction redirection** and **S = position swap**. Each cell has 100 evaluations, 800 total per method. T changes the task/target binding; S changes the object layout.
- **Same low-level checkpoint:** the RLinf-released `pi05_libero130_fullshot` π0.5-SFT is frozen in both direct evaluation and the `VLA_ACT` primitive. The harness adds planner reasoning, analytic primitives, and memory; it is not a new VLA trained for each evaluation episode.
- **Few-shot construction:** for each task, **seed 0 is reference exploration only**, excluded from reported evaluation. Successful primitive traces populate Task Specific Memory, alongside reusable Global Memory; **seeds 1–10** evaluate re-grounding under new initial states.
- **Evaluation:** no environment resets. Success is the benchmark's final binary completion predicate before budget exhaustion, not a primitive's early-return condition. Re-staging and repeated VLA calls within an episode are allowed. This is not an equal-compute “change only interface” ablation and not zero-shot task performance.
- **Planner label:** retain the paper's `Codex` and `CC` labels. Do **not** rename either row `GPT-6 Astra`; the table does not identify that model. The current repo's separate RoboCasa reproduction profile (`gpt-5.5`, xhigh) does not retroactively identify the paper's LIBERO-Pro planner checkpoint.
- **Why no RATS row:** its reported overall averages only six non-LIBERO-10 cells, whereas these rows average eight. The same-checkpoint direct baseline is the cleanest compact comparison. Do not repeat the paper's cross-coverage headline delta as though it had a matched denominator.
- **No claim about direct Astra:** this establishes gains from a memory-guided harness around this frozen π0.5 checkpoint, not that a future robot-pretrained LLM needs the same decomposition.

Cell arithmetic retained for audit:

| Method | Spat-T | Spat-S | Obj-T | Obj-S | Goal-T | Goal-S | L10-T | L10-S | Sum / 800 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| π_RLinf | 42 | 59 | 71 | 78 | 45 | 42 | 49 | 14 | 400 |
| Harness VLA (Codex) | 81 | 69 | 94 | 91 | 75 | 66 | 52 | 49 | 577 |
| Harness VLA (CC) | 94 | 80 | 88 | 90 | 87 | 87 | 71 | 62 | 659 |

Read-only implementation check at the same repository commit:

- [`robots/libero/prompts/local_eval.py`](https://github.com/RLinf/RPent/blob/328645ee9eeeb24c4cbbff030045e7efcddc4dab/robots/libero/prompts/local_eval.py#L34-L57) explicitly consumes global / suite / task layers, including the matched successful seed-0 audit and recipe; geometry must be re-grounded rather than blindly replayed.
- [`docs/source-en/rst_source/usage/libero.rst`](https://github.com/RLinf/RPent/blob/328645ee9eeeb24c4cbbff030045e7efcddc4dab/docs/source-en/rst_source/usage/libero.rst#L105-L117) distinguishes resettable exploration from default single-attempt evaluation, which does not reset or update memory. This confirms the current interface contract; it is **not** independent reproduction of the published table.

Original table source: `background/rpent_table3_page8.png` retains the full original PDF page containing Tables 2 and 3. The compact 3-row table above is a clearly labelled extraction, not an altered original figure.

### Version pitfall: do not mix other RPent numbers

The latest **v4 Table 4 (p.9)** reports RoboCasa Codex **57.1% overall** (92.0 / 61.0 / 13.8 by split). An older paper version and the current repo's separate `target50_codex_results.md` still refer to a **55.4%** paper reference. That repo page also reports its own reproduction (57.0%) and lacks per-seed raw traces. These are different versions / records; **none belong in the proposed LIBERO-Pro table**. Their snapshots are retained solely to document this boundary.

## Evidence / asset ledger

| ID | Claim | Primary evidence | Boundary |
|---|---|---|---|
| C1 | Hi Robot improves displayed IA / TP in these domains | Official interactive chart + v2 Fig.5 / §5.2 | Per-command / per-object partial metrics; main rows also change training data |
| C2 | Figure examples demonstrate hierarchical control qualitatively | Helix / Helix 02 official launch results sections | No disclosed system success denominator in checked articles |
| C3 | RPent's Harness VLA improves LIBERO-Pro over the same frozen backend | README relation; v4 Table 3; Appendix C.2 | Few-shot memory and additional planning/analytic compute; no raw-log recount |

All fresh sources and derived visual provenance are under `research/sources/control_results_20260914/background/`:

- `retrieval_manifest.json`: URLs, accessed UTC time, bytes and SHA-256; paper originals retained unchanged.
- `visual_provenance.json`: source-page / SVG anchors, crop coordinates and visual-completeness check.
- `hirobot_chart_values.json`, `rpent_libero_pro_values.json`: values and explicit metric / denominator semantics.

No slide, builder, script, shared specification, or other agent-owned file was changed.
