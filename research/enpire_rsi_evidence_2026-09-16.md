# ENPIRE / RSI evidence ledger

Format: revisions to the existing self-contained HTML talk and Chinese script, not a separate report template.
Paper type: Systems; secondary module: empirical evaluation. Primary paper, materially relevant appendices A–D, official site, and pinned public code read read-only. No code import, installation, training or robot execution.

## Claim / evidence / limits

| Claim | Primary evidence | Boundary |
|---|---|---|
| ENPIRE makes repeated physical experiments accessible to coding agents | Paper §2, original Figure 2 | Human-feedback environment construction precedes autonomous improvement |
| EN fixes reset, verifier and safety while PI edits policy/training | §2, Appendix A; `autoresearch_instruction.md` lines 3–6, 10–15 | Public contract corroborates the intended interface; it is not an independent reproduction |
| PI can edit a function or train a policy | §3.1–3.2; `interface.py` Policy.act / FunctionPolicy; PLD README, Appendix B.5 | Updating robot policy θ does not imply updating coding LLM weights |
| Rollout and learner communicate through recorded episodes | Appendix B.5; `rl/runner.py`, `rl/auto_eval.py`, `autoresearch.py` | Disk buffers separate action sources; user/teleop data cannot be counted as pure RL |
| E selects and shares useful hypotheses | §2, Figure 12, Appendix B.6 | Figure 12 traces one team's search, not independent causal ablations |
| More pairs reduce pin research time | §3.3 / Figure 3 | >1.5 h to ~40 min under conditional retries; not action latency; separate from Figure 7 |
| ENPIRE improves RoboCasa programs | §3.5 / Figure 6 / Appendix D | One script per fixed episode, no reset/retry/oracle; no estimated bar percentages |
| Pin experience is reusable in GPU autoresearch | §3.4 and Appendix B.1 | Explicit Markdown summary only; prior raw trajectories/checkpoints/hidden logs removed. Video illustrates GPU task, not a transfer ablation |
| RSI can include external memory/code rather than only model weights | DGM official article; September 2026 RoboRSI report | Conceptual background. No robot RSI benchmark inferred from DGM, no new result comparison |
| Stronger recursive improvement needs a better improver | This talk's synthesis | Held-out tasks, matched compute, retention and repeated gains remain open tests |

## Engineering anatomy retained in narration

- EN inputs: task, RGB-D/proprioception and human feedback. It builds safety/reset/reward tools using SAM3, tracking and cuRobo. Outputs fixed Gym-style interfaces and verification signals. Reward-design stage uses human-labelled success/failure snapshots; thresholds and latency requirements are task-specific. Code: saved Push-T reset and reward/evaluation modules.
- PI inputs: observations, demonstrations/online transitions, selected training recipe. Transformation: heuristic code edits or BC/RL training, with separate robot/learner/actor processes. Output: callable policy/program or checkpoint. No single policy network architecture is imposed by the harness; numerical settings from a particular idea are not universal defaults. Code: Policy protocol, PLD runtime, autoresearch contract.
- R inputs: candidate policy plus fixed reset and trial budget. Outputs synchronized state/action-source/video/result artifacts. Runtime consumes these for scoring and buffer ingestion. The paper reports 30 Hz policy and 100 Hz low-level joint tracking, not LLM inference rates.
- E inputs: results, logs, literature and other branches. Outputs next hypothesis, code diff, training recipe and retained experience. Learning is code/recipe search; coding-model fine-tuning is not reported. Git sharing and gated retention form the update path. Code: `autoresearch.py` and contract. Core scalar success and source validity remain fixed.

## Media authority

`research/enpire_v0_18_sources.json` pins the 2026-09-16 official website, JS, paper, code and downloads. Code commit: `99ee90acf65b5b18957c8382ad580db999528be3`. Seven selected official videos are used. Each is preserved in full, transcoded to H.264/yuv420p with source audio omitted. Success/reset/fleet recordings encode 8× source-time playback; two-view verification remains 1×. Manifest duration arithmetic checks no temporal cuts. Official JS `W` sets a default playbackRate of 8: this is a player setting, not proof the file itself was sped up. Website statement of an “uncut 5-minute” video is not adopted as an exact duration: downloaded files range from 219.5 to 479.2 seconds.

Eight official site images were archived; two task photographs enter the talk. Original Figure 2, Figure 3, Figure 6, Figure 7 and Figure 12 remain source-grounded. No new numbers extracted from bar heights.

## Added Control puzzles

`research/puzzle_v0_18_sources.json` pins the original X public syndication/video and the supplied Claw site/methods/app/manifest. The cube project returns HTTP 403, so no access bypass was attempted and no unverified API is asserted. The original X video is available independently. Its action interface and true timing are undisclosed; Awesome's zero-shot label is attributed, not promoted to a controlled experiment.

Claw's supplied website links a two-demo MP4. The entire Claw segment is [0, 20.566667) seconds, ending at the hard title/scene cut to Three-ring Threading after release/withdrawal. The visible source overlay says 8×; no further speedup is added. Methods state pregrasped rigid transforms, an attributed object-space reference solution, local path corrections and full-robot IK. It is kinematic joint replay, not contact dynamics or a fresh solution found from scratch. No claim that this site discloses the implementation model as Astra.

Sources: [ENPIRE](https://research.nvidia.com/labs/gear/enpire/), [paper](https://arxiv.org/html/2606.19980v1), [pinned code](https://github.com/NVlabs/ENPIRE/tree/99ee90acf65b5b18957c8382ad580db999528be3), [RoboRSI](https://lab.noematrix.ai/blog/2-roborsi/), [DGM](https://sakana.ai/dgm/), [Cube post](https://x.com/ZeYanjie/status/2098118164626501669), [Claw methods](https://qinengwang-aiden.github.io/demos/constraint_demos/methods.html).
