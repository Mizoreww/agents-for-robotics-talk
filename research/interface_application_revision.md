# Tool interfaces and broader applications — evidence notes

2026-09-10. Output: revised standalone HTML presentation, not a new paper-reading report.

## Scope

Claude Plays Robotics is used as an empirical interface study. Existing full-report and appendix snapshots are retained. No new model call, training run, reproduction, or implementation claim is introduced. DreamZero supplies the meaning of WAM only; it is not a fourth deep case study or a new benchmark arm of Claude Plays Robotics.

| Claim | Primary anchor | Interpretation and limit |
|---|---|---|
| Direct control exposes finer action authority. | `claude_robotics.txt`, Simple settings; Low-level manipulation; Appendix / Prompts | Commands vary by embodiment: torque/force and seven-dimensional end-effector motion are not interchangeable. This is not a claim of universal direct motor control. |
| Code control separates program generation from feedback execution. | Same report, Simple settings; Programmatic locomotion; Appendix / Code control | A generated controller can run faster than the language-model call. This does not establish stability or safety of arbitrary generated code. |
| Pretrained policies provide grounded behaviors. | Same report, Tools bridge some of the gap; High-level locomotion; High-level manipulation | Go2 uses velocity commands to a gait policy. MolmoAct supplies actions that the Agent accepts, edits or replaces. Agent + VLA can exceed direct control while remaining worse than VLA alone on familiar tasks. |
| RL supervision exposes a train-and-deploy workflow. | Same report, RL supervision; Reinforcement learning details | The Agent writes reward/network/schedule. It requires training resources and was not uniformly better than code control. |
| Informative state tools can help more than simply adding visual inputs. | Same report, Is visual perception the bottleneck? | Cursor and compass help in the tested conditions. Do not generalize this to every perception tool or task. |
| IK can expose task-space targets rather than joint-level solving. | Robocurve report and existing Astra notes / move-to interface | Engineering interpretation of the documented IK interface; requires calibration and a valid model. IK alone does not guarantee collision avoidance or successful contact. |
| WAM jointly models future world states/video and actions. | [DreamZero official project](https://dreamzero0.github.io/), Abstract; [paper](https://arxiv.org/abs/2602.15922) | Project-stated definition. The proposed Agent tool connection is our synthesis, not an evaluated combination in Claude Plays Robotics. No new performance or latency numbers are imported. |
| The hand demo is a structural-design application. | Existing @earthtojake design post and explicit limitation/follow-up posts, S24 | Classification is our synthesis; artifact is an unvalidated CAD/mechanism proposal, not proven physical hardware. No measured design-productivity gain is claimed. |
| Debugging is another engineering application. | Existing ASPIRE trace-inspection video and S17 source | Program/skill repair can overlap execution and improvement; chapter four is not a mutually exclusive taxonomy. |

## Diagram semantics

- Agent fans out to IK/motion planner, controller code, VLA/learned policy, and WAM tools; the flow is selective/composable, not a compulsory serial chain.
- Only action-capable outputs reach the execution node. Perception/state tools sit in the observation feedback path.
- The VLA detail diagram shows the report's returned-action path: VLA proposal → Agent accept/edit/replace → Robot. The calling Agent is not merely an instruction wrapper.
- The fourth opening shows an engineering goal, tools, artifact and validation. Prototype/test validation is a required next step, not a claim that the hand prototype exists.

## New source provenance

Official DreamZero project HTML is preserved in `research/sources/dreamzero_project.html`, with text in `dreamzero_project.txt`; SHA-256 `ce823a6397c5040dbfe4b0874c7495dede521f3ad5651154d276d9029757107d`. Retrieved 2026-09-10. Original artwork and all video bytes remain unchanged.

## RPent and neighboring toolkits

User-supplied source: <https://github.com/RLinf/RPent>. RPent means Recursive Physical Agent, a separate repository within the RLinf organization. It is not simply a renamed RLinf training algorithm.

- Source pinned read-only to `3fcf4b3645d2210c629974232c6182b5b7f98cc5`; downloaded files were not imported or executed.
- `robots/libero/tools.py`: `pi0_pick` (line 195), `move_to` (318), `rotate_wrist` (386), and `view_env_state` (1657) confirm the concrete tool examples. `move_to` uses OSC, not IK. Primitive-local pick heuristics are not full-task success evidence.
- `rpent/planner/utils/http_mcp_server.py`: lines 95–119 expose toolkit schemas and delegate calls through MCP.
- `rpent/memory/tools.py`: external memory file operations; no foundation-model weight-update claim follows from memory use.
- The official framework image is preserved as `research/assets/rpent_framework.png`. It illustrates architecture scope, not a proof that every depicted model/robot is integrated and evaluated. DreamZero lacks the supported checkmark in the pinned README. The architecture prose also contains some older hardware-support statements; avoid claiming blanket hardware readiness.
- [ROSA](https://github.com/nasa-jpl/rosa): an Agent framework for natural-language ROS1/ROS2 interaction, including system inspection and custom tools.
- [ROS-MCP Server](https://github.com/robotmcp/ros-mcp-server): MCP-to-ROS bridge via rosbridge; topic, service, action and state access. A bridge is not itself a reliable robotic policy.
- [EmbodiedAgents](https://github.com/automatika-robotics/embodied-agents) was also checked as a ROS2-native orchestration example, but is omitted from slides to keep the list short.

One supporting ecosystem slide uses the RPent original figure and briefly names ROSA and ROS-MCP. This does not change the three deep-case-study scope or introduce success-rate comparisons. The pick/check/correction narrative is an interface illustration, not a newly executed robot trial.


## 2026-09-11 — Direct actions to RPent

The first chapter now follows direct action → interface support → strengths/gaps → RPent. The direct branch shows q / EEF Pose as general command-space examples, not as a claim that the report uses one universal action representation. A downstream servo/controller remains explicit; this differs from both direct torque control and calling a learned skill.

Evidence distinctions preserved from `claude_robotics.txt`:
- Lines 16–24 and 60: model generations generally improve, especially with high-level interfaces, but low-level gains are uneven. The report explicitly says some newer models do not improve. This rules out a universal monotonic model-ranking claim.
- Lines 108–113: useful interface design can improve the same model. Cursor / compass provide matched examples; extra depth inputs can be neutral or harmful. “Better interface” means task-appropriate action abstraction and feedback, not simply more tools or higher abstraction.
- High-level manipulation section: the strongest supervisors can add value on novel goals, while familiar LIBERO-40 remains better with the base VLA. Semantic task adaptation and trained motor execution are distinct contributions, not a universal Agent-versus-generative-model ranking.
- Lines 21–24, 135–144: semantic goals and task decomposition are natural Agent responsibilities, but reliable long-horizon execution, persistent spatial memory and long open-loop planning remain unsolved in these tests. Do not call long-horizon robotics generally solved or robust.
- Lines 41–60: continuous dynamics, tight control timing and precise contact are execution challenges. “Contact understanding” is expressed as contact-state estimation / correction and a plausible bottleneck, not a separately established cognitive diagnosis.

Slide 10 uses wiping only as a qualitative illustration next to a synthesis of these findings; its source post is not evidence of force control. Slide 11 uses RPent as the closing engineering example; it does not claim to solve every identified limitation.


## 2026-09-11 — Three parts and community demonstrations (0.5)

The interface evidence above is unchanged. New material is documented in `research/community_demos_2026-09-11.md`: six community clips (X and 小红书), the Show-Harness paper (Table 2 from the PDF), and the comments and evaluations cited on the Gaps and Directions slide. Show-Harness and RPent are presented as two implementations of the same interface idea (an evaluable discrete action space versus a composable tool library); neither is claimed to solve contact or long-horizon execution. The Claude Plays Robotics anchors and their limits still govern slides 6–8.
