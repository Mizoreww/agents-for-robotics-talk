## hero-title
# GPT 6 Astra as an Embodied Policy

A comparative study of direct end-effector control and hybrid control with π0.5

## hero-intro
## Abstract

Can GPT 6 Astra turn semantic understanding and reasoning into reliable robot actions? We compare two closed-loop control architectures: GPT 6 Astra Direct and π0.5 + GPT 6 Astra. Across ten bimanual manipulation tasks in RoboDojo, the hybrid architecture achieves a **48% success rate and a mean Score of 62.60**, with GPT 6 Astra correcting only **14.4% of the executed control steps** and the remaining 85.6% following π0.5 actions. GPT 6 Astra Direct achieves 26% and 37.81, respectively; the public reference for π0.5 on the same task subset is 15.67% and 24.43.

The trajectories show that GPT 6 Astra can correct goal-alignment errors, plan non-prehensile contact, and infer unmet conditions and adjust subsequent actions when the simulator has not terminated. With direct action references and object-interaction priors from π0.5, these semantic and reasoning capabilities can be combined with skilled local manipulation, substantially improving task completion. We also examine failure modes involving grasp reliability, contact geometry, and robot-arm control to understand the behavioral characteristics of both architectures.

## results-heading
## 3. Results

## chart-scope
**Figure 3. Overall results on the ten selected tasks.** The plots include the top ten models on RoboDojo's overall simulation leaderboard and the two evaluated policies. The upper and lower plots show mean Score and success rate, respectively, with the same Score-based ordering and a 0–100 range.

## official-scope
For the official models, we recompute means over the ten selected tasks using the per-task aggregate results published by [RoboDojo](https://robodojo-benchmark.com/). Generalization tasks are weighted as two standard and three randomized episodes. These public references are not reruns using the same seeds as our experiment.

## results-summary
The hybrid policy succeeds in 24 of 50 task instances, compared with 13 for GPT 6 Astra Direct: success rates of **48% and 26%**, a difference of **22 percentage points**. Their mean Scores are **62.60 and 37.81**, respectively. This result supports combining skilled object-interaction priors with semantic judgment and local corrections.

## table-footnote
**Table 1. Per-task Score and success rate.** Switch between metrics; darker colors indicate higher values. The official references include the top four models on the overall leaderboard and π0.5.

## motivation-copy
## 1. Introduction

Community experiments with GPT 6 Astra reveal a broad range of possibilities, from 3D scene understanding and real-to-sim workflows to robot manipulation. Beyond whether the model can complete a particular task, we ask: **given the same observation, how do GPT 6 Astra and contemporary embodied policies differ in their action decisions?** Vision–language–action policies such as π0.5 have rich trajectory and object-interaction priors. GPT 6 Astra, in contrast, can combine semantics, execution history, and tool feedback to explicitly reconsider the goal and how to act.

We further explore whether an embodied policy can supply an approximate action trajectory while a strong semantic model handles goal deviations and exceptional situations, combining their strengths to improve success. At each decision point, we first generate a candidate action sequence with π0.5, then let GPT 6 Astra use the same observation to choose whether to accept or correct it. GPT 6 Astra Direct, which generates EEF actions directly, serves as the comparison.

We observe three characteristics of the hybrid architecture: **goal alignment**—correcting actions that select the wrong object, target position, or manipulation direction; **3D planning and non-prehensile manipulation**—nudging or repositioning objects before grasping them under more favorable geometric conditions; and **feedback-driven reasoning**—noticing that the simulator has not terminated, inferring potentially unmet success conditions, and continuing to make corrections. These behaviors occupy a relatively small share of executed control steps and co-occur with higher overall task completion. The videos below illustrate these characteristics and situations in which they still fail.

## related-work
### 1.1 Related Community Explorations

[Awesome Astra Embodied AI](https://github.com/zjwzcx/Awesome-Astra-Embodied-AI) brings together community explorations in control, planning, simulation, and training, tracing a continuous path from scene understanding to action generation and the construction of training environments.

**Direct control in simulation and on physical robots.** Simulation experiments cover tabletop pick-and-place, dexterous-hand manipulation, and motion-trajectory generation for humanoid and quadruped robots. The model may construct actions directly or provide trajectories for a low-level controller to track. Physical-robot experiments include grasping and placing, keyboard operation, drawing, and everyday manipulation, translating open-ended language goals into action sequences under visual feedback. [Robocurve](https://openai.robocurve.org/gpt-6-astra/) evaluates several types of robot-arm manipulation, providing concrete records of the model's behavior across different contact tasks.

**Demonstrations, context, and policy collaboration.** [Axel's mobile-manipulation demonstration](https://x.com/ax_pey/status/2098216469012283681) and [Innate's implementation](https://github.com/innate-inc/innate-os/pull/817) organize demonstration records, camera observations, and robot state into a continuing control context. [GPT-Policy-Eval](https://github.com/cheng-haha/GPT-Policy-Eval) demonstrates physical-robot execution from a single video demonstration, including insertion and manipulation after removing an occlusion. The community also explores a division of labor in which Astra interprets and decomposes tasks, then invokes pretrained policies such as FluxVLA to execute actions, connecting semantic planning with existing motor capabilities.

**From visual records to interactive scenes.** Real-to-sim explorations include reconstructing kitchens and articulated structures, reconstructing dexterous-hand motion, retargeting hand–object interactions, and building replayable simulations from multi-view demonstrations. [Realsee](https://www.realsee.ai/blogs/news/how-to-build-an-editable-blender-scene-from-realsee-galois-outputs-with-gpt-6-astra) and [AI for Mortals](https://www.aiformortals.co/blog/gpt-6-astra-blender-fallingwater) further demonstrate workflows that use scans, images, and tool feedback to generate and refine Blender scenes.

**Environment construction and training iteration.** The index also covers robot morphology design, motion-task specification, reinforcement-learning environment construction, and iterative training, spanning quadruped locomotion, bio-inspired robots, and dexterous-hand manipulation. Together, these explorations broaden the roles of general-purpose models in embodied work: a model can participate not only in the action loop, but also in demonstration understanding, policy invocation, scene creation, and the construction of learning systems.

## method-copy
## 2. Methods and Experimental Setup

### 2.1 Action Generation and Execution

**Hybrid control (π0.5 + GPT 6 Astra).** Given the current images, 14-dimensional proprioceptive state, and task instruction, π0.5 generates a 50-step candidate action sequence in joint space, with 14 dimensions per step. GPT 6 Astra receives the same observation, execution history, and the bimanual forward-kinematics trajectory corresponding to the candidate actions. It chooses either to execute the first 1–15 steps unchanged or to apply an end-effector (EEF) correction for 1–5 steps. After each action segment, the two models make a new decision using the updated observation.

**Direct control (GPT 6 Astra Direct).** π0.5 is neither run nor used to provide candidate actions. The model directly generates bimanual EEF targets and gripper commands from images, proprioceptive state, the task instruction, and history, executing 1–5 steps at a time. Both groups use GPT 6 Astra with xhigh reasoning, and retain the same task descriptions, success-criteria reminders, and EEF execution interface.

For π0.5, we use the task-finetuned weights released by RoboDojo. See [π0.5](https://www.pi.website/blog/pi05) and the [GPT 6 Astra documentation](https://developers.openai.com/api/docs/models/gpt-6-astra) for model background.

## method-caption
**Figure 2. Closed-loop execution of the two policies.** At each decision, the hybrid architecture chooses one of two alternatives: accept the candidate π0.5 actions or execute a GPT 6 Astra EEF correction. The two branches are not executed simultaneously. The Direct architecture generates all EEF actions itself. Python handles validation, the simulator connection, and recording; the model makes the action decisions.

## paired-settings
### 2.2 Task Selection and Evaluation Protocol

We first divide the 0–72% range of official π0.5 success rates into four equal intervals, then select **6, 2, 1, and 1 tasks**, respectively, from the lowest to the highest interval, for ten tasks in total. Selection favors tasks with room for improvement while covering semantic classification, sequence memory, packing, construction, and deformable-object manipulation; it is not dominated by high-precision insertion.

Each task is run five times. The two policies are paired instance by instance on task, scene, and eval, layout, reset, initial, and policy seeds. Number arrangement, packing, and clothes folding—the tasks with generalization scenes—use two standard and three randomized episodes; the other tasks use five standard layouts. Success rate and Score measure final success and partial completion, respectively, both using RoboDojo's native evaluation.

## intervention-copy
## 4. Behavioral Characteristics of the Hybrid Architecture

### 4.1 Fewer Corrections, Higher Completion

The 50 hybrid trajectories contain **42,750 executed control steps**. Of these, **36,576 steps (85.6%)** follow π0.5 actions, while **6,174 steps (14.4%)** are corrected by GPT 6 Astra. The model continually reviews candidate actions at decision points, but replaces only a relatively small fraction of the executed actions.

## intervention-limit


## video-note
The following clips illustrate different capabilities within the same closed-loop control framework. Click a video to enlarge it.

## grounding-heading
### 4.2 Correcting Grounding Errors

Using the instruction and visual observation, GPT 6 Astra can correct errors in target selection, spatial position, and manipulation direction in candidate actions, realigning them with the current task.

## contact-heading
### 4.3 3D Planning and Non-prehensile Manipulation

GPT 6 Astra does not simply follow a fixed approach–grasp–transport pattern. It can use the 3D relationship between an object and the gripper to nudge or push the object, or change the approach direction, before grasping. The following clips show local 3D planning around contact geometry, including handing control back to π0.5 after a correction.

## reasoning-heading
### 4.4 Reasoning from Non-termination and Making Corrections

After the apparent manipulation is complete, GPT 6 Astra can independently notice that the simulator has not terminated. It then hypothesizes that an object may have been missed, a target orientation may be incorrect, or a structure may not yet meet the requirements, and tests these hypotheses through observation and action. This illustrates reasoning that combines task semantics with termination feedback, rather than simply repeating the previous action.

## failure-heading
## 5. Where Does the Hybrid Architecture Still Fail?

Understanding the goal correctly does not guarantee reliable contact. The hybrid policy may still fail repeatedly at grasping, collide with container rims, or fail to promptly recognize lost task progress. Repeated attempts consume the native step budget. Moreover, the model receives feedback at action-segment boundaries, so an object slipping within a segment may not be detected until the next observation. The following clips illustrate four specific cases.

## gpt-only-heading
## 6. Behavioral Differences Between Direct and Hybrid Control

Without π0.5 action references, GPT 6 Astra Direct constructs manipulation plans more freely. This freedom produces interesting zero-shot behaviors while placing more responsibility on the model itself for action reliability and robot-arm geometry constraints.

### 6.1 Zero-shot Behavior: Novel Plans and Execution Stability

GPT 6 Astra Direct tries sweeping bottles into a bin with the arm, grasping a tower-building board with one hand, or using one arm for operations better suited to bimanual coordination. These behaviors demonstrate the ability to organize actions autonomously from task semantics. Without established action patterns as a reference, however, novel plans may lack reliable grasping, support, and release procedures.

## cost-heading
### 6.3 Fewer Tokens, Higher Success

The hybrid architecture achieves a **48%** success rate, compared with **26%** for Direct. The selected trajectories record approximately **624.8M and 1.13B** tokens, respectively—a reduction of about **44.8%** for the hybrid architecture. Direct executes approximately **2.05 times** as many action segments, requiring more frequent construction and checking of its own actions. The π0.5 action prior both improves completion and reduces how often the model must generate low-level actions.

## physical-time-correction
**Table 3. Execution and usage for 50 selected run instances per architecture.** Token counts include cached input and cover only the runs corresponding to the selected trajectories, not all earlier retries; they are not billed monetary amounts. Physical duration is the number of control steps multiplied by 0.04 seconds and excludes model-response latency. Direct has a shorter mean physical duration, but early failures also shorten trajectories, so this alone does not establish its end-to-end execution efficiency.

## limits-copy
## 7. Discussion and Scope

The ten tasks are stratified by π0.5 success rate, with an emphasis on lower-success tasks and five evaluations per task. The results characterize performance on this task subset. Selected videos illustrate behavioral mechanisms and manipulation characteristics; they do not estimate the prevalence of each failure type.

The current comparison simultaneously varies action priors, action-generation interfaces, and execution-segment lengths. The results support the practical value of this hybrid architecture; disentangling the contribution of each factor requires further study.

## conclusion-copy
## 8. Conclusion

GPT 6 Astra already demonstrates strong capabilities as a robot policy: it can propose actions from task semantics, correct goal-alignment errors, perform non-prehensile manipulation, and reason and recover from execution feedback. Its strength lies not only in generating actions, but also in reconsidering what should be done next when exceptional situations arise.

π0.5 can be viewed as the architecture's "cerebellum": it supplies skilled action trajectories and object-interaction priors with relatively low inference overhead. Building on these priors, GPT 6 Astra judges goals, handles exceptions, and makes targeted corrections. With GPT 6 Astra correcting just 14.4% of executed control steps, their combination achieves a higher success rate on the RoboDojo task subset while consuming fewer tokens than Direct control.

These results suggest a useful division of labor: let the embodied policy handle the continuous manipulation it performs well, and let the general-purpose model reassess when the goal, geometry, or task progress deviates from expectations. Semantic reasoning and motor experience need not replace one another; they can reinforce each other within the same closed loop.

The RoboLab results add a condition to this interpretation: on the selected semantic pick-and-place tasks, where the student is transferred zero-shot, GPT 6 Astra Direct achieves near-perfect performance. Hybrid control is slightly below Direct but remains substantially above the π0.5 baseline. Whether the student's action prior fits the task is an important consideration when interpreting the difference between the two architectures.

## reference-heading
## References

## closing-copy
This page provides evaluation results and trajectory videos. The video library supports selection by task and run instance, with paired policy comparisons using the same seed.

## skill-summary
- Observations include head and bilateral wrist RGB images, joint and gripper state, EEF poses, the original task instruction, and execution history. Codex retains file reading, image viewing, code-based computation, and persistent notes.
- π0.5 receives three 640×480 RGB views, a 14-dimensional proprioceptive state, and the instruction, and generates candidate joint-space actions. GPT 6 Astra commonly uses image previews with a longest side of 480 pixels; the originals remain accessible, and π0.5 input resolution is unchanged.
- GPT 6 Astra outputs bimanual target positions, orientations, and gripper states, executing 1–5 control steps per segment with the 5 cm / 0.35 rad action safeguards retained. The hybrid policy may execute a 1–15-step prefix of the candidate π0.5 actions.
- Shared task context includes the native step budget, current progress, partial credit, and final success criteria. A terminal outcome is recognized only when confirmed by the simulator; most tasks also require the arms to return home.
- Control runs at 25 Hz. Neither group receives ground-truth task-object states, future trajectories, environment rollback, or a hidden planner. GPT 6 Astra Direct does not run π0.5.

## clip-clip__fe2857368ce87ec2ffdcd4ac__0-analysis
### Semantic Goal Alignment

The language-based classification clip shows a correction of the manipulation target. This local behavior supports a qualitative analysis of goal alignment, but does not establish robustness to arbitrary visual changes.

## clip-clip__6f1191749b24df72921e800d__0-analysis
### Repositioning Number Blocks

The policy adjusts a number block's position using current visual feedback, illustrating a correction of a local manipulation error.

## clip-clip__182f98be14595fc71b02b377__0-analysis
### Non-prehensile Contact Assisting a Grasp

The model first changes the object's state by nudging it, then proceeds to grasp. This local recovery shows that action selection is not limited to direct grasping.

## clip-clip__4288645ef90dc53de13376eb__0-analysis
### Adjusting the Grasp Approach

When the relative geometry of the object and gripper is unfavorable for grasping, the policy adjusts its approach. The clip illustrates local contact behavior; the overall outcome remains determined by the native evaluation.

## clip-clip__cbf8658bad76fd96fef01245__1-analysis
### Final Checks Using Termination Feedback

When objects are approximately in place but the simulation has not ended, the policy continues checking and adjusting. The record shows feedback-driven behavior, not a direct observation of the model's internal reasoning.

## clip-clip__5436877e6101be2b23b24fc2__0-analysis
### A Missed Object in an Occluded Region

Near the end of the task, the policy attempts to handle an object behind the box and adjust its orientation. The episode ultimately fails, so the clip illustrates an attempted recovery.

## clip-clip__cb2554914fe8187ac98e9e45__0-analysis
### Insufficient Clearance at a Container Rim

Collisions between the container rim and the gripper or object can disrupt transport. Choosing the correct placement target does not guarantee adequate clearance along approach and retreat paths.

## clip-clip__7ef164f7a8783f3af3eb9090__0-analysis
### Delayed Feedback Within an Action Segment

Slipping or collision may occur within an action segment, while the model must wait for the next observation to correct it. The clip illustrates a limitation of the decision-feedback granularity.

## clip-clip__b34c1a832bb5123d6eb6a6af__0-analysis
### A Non-prehensile Transport Plan

GPT 6 Astra Direct attempts to sweep bottles toward the bin. The episode ultimately fails, showing that diversity of action plans does not necessarily translate into effective control.

## clip-clip__6ba3a538a3405206181aa6c6__0-analysis
### Recovering After Blocked Motion

The number-arrangement clip shows adaptation to control feedback. The model already receives proprioceptive state; the difficulty lies in using it effectively for subsequent actions, not in missing state input.

## clip-clip__71c12723687a550b770f36c0__0-analysis
### Local Reachability and Structural Stability

GPT 6 Astra Direct proposes alternative tower-building plans, but local action feasibility is not equivalent to final structural stability.

## clip-clip__9e40a74ed6b0a356a421f53b__0-analysis
### Stability of Single-arm Execution

The single-arm operation in this table-organization clip is not sufficiently stable. Action priors may influence plan selection, but the current experiment does not include a corresponding causal ablation.

## direct-control-heading
### 6.2 Proprioceptive Control Difficulties and Local Recovery

Both architectures receive proprioceptive state. Direct's difficulty lies in translating this information effectively into reachable EEF targets while handling joint limits, orientation, and contact relationships. This can lead to repeated attempts and control failures.

The number-arrangement task also contains a striking recovery: after motion is blocked, the model reinterprets the arm's control feedback, adjusts its actions, and continues execution. This demonstrates GPT 6 Astra's ability to adapt locally to control constraints, rather than passively repeating failed commands.

## robolab-intro
### 3.1 RoboLab: Zero-shot Evaluation on a Single-arm Franka

We also compare our approaches with common baselines on [RoboLab](https://arxiv.org/abs/2604.09860), a benchmark using a single-arm Franka robot. We select **10 tasks, with 5 trials per task and policy, giving 50 evaluation instances per policy**. Alongside GPT 6 Astra Direct and π0.5 + GPT 6 Astra, we include π0.5, Cosmos3-Nano-Policy, and DreamZero on the same task subset. All five methods are compared using final task success rate; this section does not use RoboDojo's Score metric.

## robolab-figure-caption
**Figure 4. Success rates on the ten selected RoboLab tasks.** Each policy is evaluated 50 times, with equal weight per task. GPT 6 Astra Direct succeeds in 49/50 trials, π0.5 + GPT 6 Astra in 46/50, π0.5 and Cosmos3-Nano-Policy each in 18/50, and DreamZero in 17/50. The horizontal axis shows success rate (0–100%).

## robolab-results-summary
**GPT 6 Astra Direct achieves near-perfect performance on this task subset: 49/50 (98%), with 5/5 successes on 9 tasks.** π0.5 + GPT 6 Astra achieves 46/50 (92%), lower by 6 percentage points, or 3 trajectories; nevertheless, it improves over π0.5's 18/50 (36%) by 56 percentage points.

## robolab-analysis
This ordering differs from RoboDojo, where the hybrid policy leads. One possible explanation is **task composition**: the selected RoboLab tasks mainly involve pick-and-place with semantic requirements, including identifying targets, distinguishing size or color, understanding containers and spatial relations, and organizing grasps and placements. They also include ordered block stacking and mug reorientation. This composition may favor GPT 6 Astra's semantic understanding, spatial judgment, and closed-loop planning, enabling high success with directly generated EEF actions.

Another possible factor is **the student policy's adaptation to the tasks**. The RoboDojo evaluation uses task-finetuned π0.5 weights. RoboLab does not provide training data for its test tasks; the π0.5, Cosmos3-Nano-Policy, and DreamZero baselines in this section use DROID-trained weights for direct zero-shot evaluation on RoboLab. With π0.5 alone succeeding only 36% of the time, its candidate actions may impose additional correction and recovery demands on hybrid control, limiting the benefit of its action prior. Direct, by contrast, can plan the operation from the current state.

Thus, **when Direct can already solve semantic pick-and-place tasks reliably and the student lacks task adaptation, adding and then correcting the student does not necessarily improve success further**.

## robolab-protocol
**Evaluation protocol.** This section reports our deployment and evaluation of all five methods in RoboLab, using 5 final evaluation results per task and policy, including both successes and failures. None of the methods is finetuned using demonstrations from these RoboLab tasks. Some evaluations include retries, and initial states and execution budgets are not fully paired across methods; the results therefore describe performance on this selected task set.

## robolab-scope-note
Except for the RoboLab results in this section, statistics elsewhere in this report—including token usage and execution duration—come from the RoboDojo evaluation.