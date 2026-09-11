# Community demonstrations after the GPT-6 Astra release — evidence notes

2026-09-11. Searched X (logged-in Chrome: queries "astra robot" latest/top, "astra humanoid", "astra rubik", user timelines) and 小红书 (search "Astra 机器人"). Post metadata was pulled through the fxtwitter API (`research/sources/x_*_fxtwitter.json`); videos came from X's CDN at ≤1280 px, and one 小红书 clip from the note page stream URL. Nothing here is a controlled evaluation unless marked.

## Clips embedded in the deck

| Slide | Clip | Author, date, reach | What the author states | What is not established |
|---|---|---|---|---|
| 10 | `wenli_icl` (11.2 s, 8×) | Wenli Xiao, CMU Robotics PhD, ex NVIDIA GEAR; 2026-09-09; ~196K views | A recording of a human doing a novel task is dropped into the Codex app; Astra drives the arm the same way on the first pass ("physical ICL"). A roundup notes the setup uses existing motion-planning tools. | Trial counts, failure statistics, interface details, latency. |
| 10 | `arx_knob` (15.3 s, 16×) | ARX Robotics (company); 2026-09-05; ~213K views | In a new room, one instruction ("turn the knob to start the washing machine") was enough to complete the task. | Interface, repeats, failures. 15.3 s × 16 ≈ 4 min wall-clock is derived from the playback label. |
| 11 | `ze_rubik` (23.1 s) | Yanjie Ze, Stanford CS PhD, ex Figure; 2026-09-10; ~132K views | "GPT6 Astra solved Rubik's Cube with robot hands". Project page: two dexterous hands solve a cube through physical contact in MuJoCo; one fixed 10-move scramble; physics replay with contact / normal-force / layer-error / validation panels. | Whether the motion is a learned policy or scripted primitives, whether it ran in real time, and transfer to real hands. Replies asked these questions; no author answer as of 2026-09-11. |
| 11 | `juggle` (5.3 s) | @thermalpastor (anyact.ai); 2026-09-09; ~74K views | Astra orchestrates two robots juggling one ball; "actual MuJoCo physics simulation at 1× speed". | Anything beyond the demonstration. |
| 12 | `show_harness` (39–72 s excerpt of the project video) | Show Lab, NUS; arXiv 2609.10522, 2026-09-09; announcement thread ~28K views | See paper notes below. | — |
| 14 | `xhs_piper` (41.4 s, 70×) | 小红书 author 虽然不但是; 2026-09-06; 157 likes | A clean Codex + GPT-6 setup with only the Piper and RealSense SDKs; the arm picks and places a carrot; three failed grasps then a successful rollout. | Trial counts; harness details. |

Removed: the @k7agar wiping clip (its role, a sustained real-world attempt, is now covered by the 小红书 Piper clip with disclosed failures).

## Show-Harness (slide 12 shows only the cross-task averages; the rest is in the script)

Source: arXiv 2609.10522 PDF, Table 2 (10 trials per task, authors' own task set, Franka Research 3 and AgileX bimanual, ManiSkill and RoboLab in simulation).

| Split | π0.5 | GR00T | ZS (Gemini 3.1 Pro, medium thinking) | FT (Qwen3.5-2B, LoRA) |
|---|---|---|---|---|
| Cross-task average (10 object→receptacle tasks) | 39.0% | 35.0% | 89.0% | 86.0% |
| Cross-environment average (background, lighting, viewpoint, distractors) | 40.0% | 34.0% | 100.0% | 88.0% |
| Sim-to-real (simulated demos only) | 0/20 | 0/20 | – | 13/20 |
| Cross-embodiment average (Franka, AgileX) | 41.0% | 36.0% | 93.0% | 87.0% |

Action units: MV_FWD/BACK/LEFT/RIGHT/UP/DOWN, ROTATE_CW/CCW, GRASP, RELEASE, DONE. Interpreters: Franka tracks Cartesian setpoints with impedance control, AgileX uses IK with streamed joint targets, the simulator executes operational-space commands. The paper states planning is not the main bottleneck; errors concentrate on fine-grained grasping and placement. Limits: parallel-jaw manipulation only; no tactile or force feedback. Two earlier web summaries of this paper gave different numbers (96/92/94 and 96/84/82); the PDF table is authoritative.

## Evaluations and comments cited on slide 14

- Robocurve (already in the deck): placement 19/20, insertion 2/20.
- HumanCLAW-Bench (Jiawei Gu, 2026-09-10): GPT-6 Astra Find/Nav/Interact SR 75.5 / 57.1 / 46.6% versus previous best 64.9 / 42.4 / 16.8%; still bumps into objects; single run in the low-thinking setting.
- RoboDojo (community run by @XuefW82242, 2026-09-10): 20 tasks × 3 seeds → 11/60 full successes (18.3%), mean score 24.4; author notes leading published policies are around 20%.
- Jitendra Malik (2026-09-08): demos are parallel-jaw pick-and-place and mainly show planning; robotics also needs high-frequency controllers for torques and forces; challenge: prompt an LLM to output high-frequency control for a legged robot on varying terrain.
- Max Fu, Google DeepMind (2026-09-06): harness + tool calls (IK, SAM3) can match direct control cheaper, faster and more reliably; self-evolving harnesses and skill libraries will expand the frontier; VLA and WAM become library entries.
- Yu Xiang, UT Dallas (2026-09-10): Astra takes vision and language and outputs actions, so in a broad sense it is a VLA; "your VLA just isn't trained and scaled at the GPT-6 level".
- Omar Espejel (2026-09-09): asks for the same model on the same task with different tools and memory (Go2 with DimOS / Viam / ROS 2) to compare tokens, mistakes and human help.
- Jiawei Gu (2026-09-10): robotics may inherit the scaling curve of general intelligence; a robot body as another interface. Treated as a hypothesis.
- 小红书 "GPT-6 Astra开启 Robot RSI时代" (2026-09-07): frames ASPIRE / ENPIRE as "Robot RSI" and names the missing reproducible, roll-back-able, parallel test environment as the bottleneck. Used in the slide 26 script as a community framing; its RoboClaw figure (53.7% less human time) was not verified and is not in the deck.

## 小红书 notes read (search "Astra 机器人", 2026-09-11)

Recorded in `research/sources/xhs_search_astra_robot_2026-09-11.txt`. Only two notes are used: the Piper clip (slide 14) and the Real2Sim workflow note by Hello燕Sir (cited in the slide 19 script; three-view frames from InternData "put the pen into the pen holder" and a DROID episode, Blender scene modeling and motion replay, a second version adding actions, intrinsics and URDF with GPT-5.6 preprocessing; a follow-up prompt fixed a clipped wall and a missing shelf). The image-based critique note "用基模直接控制机器人有本质问题" was not transcribed.

## Not embedded

Considered and left as references: @dimentary six-legged spider with two arms in MuJoCo (50 s), @Su1eyman11 G1 DJ setup (scripted IK, sim UI), HumanCLAW comparison video, Bilibili demos (盒子桥 Loop-ROS cucumber cutting; 从来你又调皮 direct joint control where the model wrote its own IK). Bilibili downloads would need yt-dlp, which is not installed.
