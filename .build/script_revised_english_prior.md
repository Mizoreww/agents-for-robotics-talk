# Agents for Robotics: Speaker Script

英文逐页讲稿，对应新版 24 页单文件 HTML。正文可以直接讲；以 “Cue” 标记的内容是播放、指图或停顿提示，不念出。60 分钟是含视频、读图和短互动的建议节奏，不是单纯朗读时长。问题可留作停顿，不必每次展开讨论。

## 01. Agents for Robotics

Today I want to ask a practical question: where can a general-purpose agent contribute to robotics, and what makes that contribution reliable?

We will focus on three case studies. One tests robot execution, one constructs simulated worlds, and one organizes real robot experiments. Along the way, we will watch several application demos. Together, they let us separate what already works, what depends on the surrounding system, and what still needs a stronger test.

## 02. Demo: A Robot Paints with Feedback

> Cue: Play the painting clip once. Introduce the question before playback; let the audience watch the changing canvas. The clip is about 68 seconds. The explanation can overlap playback.

Let us begin with something concrete. Here, a general agent helps a robot paint. It turns a visual objective into physical actions, looks at the result, and revises what to do next.

As you watch, consider one question: what is actually changing when the result improves?

The original author describes anchor points, calibration, and human feedback across iterations, sometimes during execution. Those details help explain how the system connects image coordinates to physical marks. They also show why we should inspect the workflow behind the video.

An improved painting could come from a better plan, corrected calibration, or a more useful instruction. None of those changes requires an update to the foundation model's weights. The public demonstration does not establish such a weight update.

The video makes the opportunity easy to see. An agent can coordinate a task that combines perception with physical action. It leaves us with a more demanding question: after this run ends, what useful capability remains? That will be the thread connecting the rest of the talk.

## 03. Our Ultimate Goal

> Cue: Follow the forward path, then the return arrow. Pause at “reusable capability” and invite one example of an artifact that could survive a session.

The goal has two parts. First, the robot should finish the current job despite uncertainty. Second, useful experience should make a later job easier.

The first part concerns execution. A person states a goal, but the world rarely matches the robot's initial assumptions exactly. An object may be displaced. A grasp may slip. The robot needs observations that help it correct the next action.

The second part concerns persistence. Imagine that the agent spends twenty minutes debugging a grasp and then loses every useful change when the session ends. It may have solved today's problem, but it has not necessarily become more capable tomorrow.

A persistent artifact could be a corrected program, a reusable skill, a calibrated scene, or a trained policy. Different artifacts require different tests. A program needs execution tests. A simulator needs predictions under actions it was not fitted to. A policy needs evaluation beyond the trajectories that produced it.

This diagram describes our goal. It is our synthesis, rather than an architecture claimed by any one paper. In particular, the forward arrow does not mean every successful execution automatically creates a reusable skill. Someone must retain the change and establish when it remains useful.

We will therefore keep asking two questions. What does the agent change during the run? And what evidence tells us that the change deserves to survive the run?

Those questions give us a common language without forcing very different systems into one benchmark.

## 04. Three Questions, Three Case Studies

The first question is about execution. What can a general model do when we give it different ways to act? Claude Plays Robotics is useful because it tests several interfaces rather than showing only one successful behavior.

The second question is about world building. Can an agent turn a recorded interaction into a useful simulator? Agentic Real2Sim gives us a concrete pipeline and a complete evaluation denominator.

The third question is about improvement. Can an agent use real experiments to produce a better policy? ENPIRE puts the physical robot inside that research loop.

These are complementary roles, not compulsory stages. ENPIRE can operate directly on hardware without first using Agentic Real2Sim. Their success percentages also measure different things, so we will not rank the papers by a shared percentage.

## 05. Claude Plays Robotics

> Cue: Read the original figure by interface. Point out what the model produces in each setting before discussing the score. Allow about 20 seconds for the audience to inspect it.

Our first case study begins with a surprisingly important choice: what does it mean to let a language model control a robot?

One option is direct control. The model chooses an action, receives an observation, and chooses again. This places a large burden on its ability to connect what it sees to the consequences of a motor command.

Another option is programmatic control. The model writes code that the runtime executes. That code can contain a feedback controller that runs much faster than the model itself. We must distinguish the speed of the generated controller from the speed of the model that wrote it.

A further option places the model above an existing control system, such as a vision-language-action policy. The supervisor can choose instructions or decompose a goal while the policy supplies grounded motor behavior.

The report studies several such settings, including reinforcement-learning approaches. The original figure preserves those distinctions. We should read each result together with the interface that produced it.

Suppose a system succeeds after we replace direct joint commands with an inverse-kinematics tool. Some difficult work has moved into the tool. That can be excellent engineering. It changes the capability we should attribute to the language model, however.

This is why I chose the report as our execution case study. It makes the boundary between the model and the robotics stack visible. Before asking whether a newer model is better at robotics, we need to ask which robotics responsibilities the experiment actually gives it.

The next examples make that boundary more tangible.

## 06. Direct Control Meets Physical Constraints

> Cue: Play the two short report animations. The humanoid clip illustrates generated control code. The manipulation clip is qualitative. Point to the 0–5.5% full-success statement before moving on.

On the left, the humanoid example contrasts a generated Python controller with zero commands. This shows why executable control code can be useful. The model can spend time constructing a controller, while that controller handles subsequent updates at a much shorter time scale.

On the right, the manipulation example shows another difficulty. Reaching the object, touching it, and grasping it are intermediate achievements. A complete task may still require a stable grasp, accurate transport, and successful placement. A system can improve on intermediate events while remaining unreliable at the final objective.

In the report's direct-manipulation setting, full task success ranges from zero to about 5.5 percent. The animation should be interpreted alongside that result. One selected trajectory cannot tell us how often the entire task works.

Timing is another constraint. For some locomotion experiments, the simulator pauses while the model is being called. The report contrasts control requirements of roughly 83 hertz with model-call rates of about 0.2 to 0.4 hertz in the setting it discusses. Pausing allows the study to examine action quality without real-time latency dominating the result. A physical robot cannot generally pause the world in the same way.

The engineering response is to assign fast stabilization and motor execution to a suitable controller, then give the general model decisions at an appropriate time scale.

That sounds reasonable, but it creates a new question. If we put a supervisor above a capable policy, does the supervisor always improve the outcome? The next result shows why we need to test that assumption.

## 07. A Supervisor Can Disrupt a Capable VLA

> Cue: Identify the base VLA and supervised variants in the original plot. This plot covers familiar LIBERO-40 tasks only. Give the audience time to compare them.

Here we move from low-level action generation to supervision. The low-level policy already knows how to execute some tasks. The agent can influence that execution through task-level decisions.

The figure shows familiar LIBERO-40 tasks. In this setting, adding supervision can reduce performance relative to the base VLA. The broader report also studies novel tasks, where supervision can help. Those novel-task results are separate from the figure on this slide.

Why could a helpful-looking supervisor make a familiar task worse? Consider a policy that is already on course to succeed. If the supervisor incorrectly judges progress, changes the instruction too early, or interrupts a useful action sequence, it creates a failure that the base policy would have avoided. These are possible mechanisms for harmful intervention, rather than mechanisms isolated individually by this figure.

Conversely, when the policy cannot interpret an unfamiliar goal, decomposition or a better instruction may provide information it was missing. The value of supervision depends on the situation.

This suggests a more informative evaluation than reporting one overall improvement number. We can ask how often supervision rescues a case the base policy would fail, and how often it damages a case the base policy would complete. We should also measure the added latency and number of interventions.

The small diagram shows our simplified interpretation of the interface. The agent chooses at the task level, the VLA produces actions, and the robot determines the outcome. It is not the report's full implementation.

The important point is that an extra reasoning loop is an intervention with both potential benefits and costs. We need evidence that its decisions improve the particular execution system underneath it.

Next, a small real-robot assessment makes the difference between coarse motion and fine contact easy to see.

## 08. Demo: Placement and Fine Insertion

> Cue: Play bowl placement, then the published failed insertion clip. Keep both trial counts visible. Do not present this as an official OpenAI evaluation.

These clips come from Robocurve, an independent evaluator. They complement the previous study, but they use a different system and a much smaller protocol.

The model receives three camera views and robot state. It requests absolute end-effector poses through a move-to interface, while inverse kinematics handles the joints. Trials have a twenty-model-call budget and a speed cap of twenty-five percent, together with safety limits.

In the reported Astra trials, bowl placement succeeds nineteen times out of twenty. Fine insertion succeeds twice out of twenty. The comparison model, Fable 5.1, records eight out of twenty for placement and two out of twenty for insertion.

The contrast is useful: a good result on a coarse placement task does not establish reliable fine contact. The failed insertion clip keeps that limitation visible beside a successful demonstration.

We should resist a stronger causal claim. The sample is small. The comparison includes different placement rigs, non-interleaved runs, manual resets, and unblinded scoring. It cannot tell us exactly how much of the gap comes from geometry, observation, policy, or experimental setup.

What it does give us is a concrete question for a future system: when the final millimeters matter, what feedback and control interface will let the agent make a dependable correction?

## 09. Demo: Wiping a Table

> Cue: Play the wiping clip. Ask the audience to name one quantity that would need feedback. Keep this interlude brief.

Wiping broadens the application picture. Unlike one discrete placement, this behavior requires sustained interaction with a surface.

As you watch, think about what the robot would need to observe. Has it covered the intended area? Is the tool still in contact? What happens if the tool slips or the surface height changes?

The public post demonstrates a behavior. It does not provide enough repeated evaluation or control detail to answer all those questions. We should not infer a force-control system just from the appearance of contact.

Still, the demonstration illustrates why general agents are interesting: they can help coordinate a practical task through available tools. Let us now collect the execution chapter into one picture.

## 10. Execution: Reasoning Through an Interface

> Cue: Follow the boxes left to right, then trace observations back to the agent. Use the two bottom statements to close the chapter.

In this execution loop, the agent changes a decision. A controller or skill turns that decision into grounded actions. The robot produces observations that inform the next decision.

The interface determines which problems belong to the agent and which belong to the controller. A move-to tool, a generated controller, and a VLA each provide different support. The first case study shows why we need to state that support before interpreting a result.

The evidence supports a useful role for general reasoning around executable interfaces. It also leaves precise contact, timing, and consistently beneficial supervision as important challenges. A successful video does not remove those challenges.

Now consider how we might investigate a failure without spending every trial on hardware. If we had a simulator that represented the relevant interaction, we could inspect the scene and test alternatives more cheaply.

That motivates the next chapter. But a simulator is only useful for such decisions if it gets the relevant consequences right. We will ask how much of that capability an agent can construct from one recorded interaction, and how to distinguish a convincing replay from a predictive model.

## 11. Agentic Real2Sim: A Real Episode and Its Twin

> Cue: Play the real and simulated clips together. They depict the same recorded episode, but this presentation does not perform synchronized numerical error measurement.

The videos show the basic objective of Agentic Real2Sim. Starting from a real interaction, the system constructs a simulated episode that resembles it.

This requires much more than a visually recognizable object. The pipeline must assemble the robot, scene geometry, camera, object poses, and trajectories into something the simulator can run. It must also choose representations and parameters that support the interaction.

The difficulty is that a video does not uniquely specify a physical model. A mismatch in camera pose might look like a mismatch in object position. A collision shape and a friction parameter might partly compensate for each other along one trajectory. Several constructions could therefore produce a similar-looking replay.

Imagine that the real robot pushed an object slowly from one side. A reconstructed scene might replay that motion well. We still need another test to know whether it predicts a faster push or contact from a different side.

That distinction gives the chapter its structure. First we will see how the agent coordinates the conversion. Then we will inspect the exact meaning of the paper's replay-acceptance result. Finally, a separate application demo will show a disclosed failure where the chosen physical representation was inadequate.

The paper's contribution is a runnable conversion workflow with a measurable outcome. We can appreciate that contribution while keeping predictive validity as a separate question. Let us look inside the workflow.

## 12. Agentic Real2Sim: The Conversion Pipeline

> Cue: Walk through the original architecture figure in four stages. Pause after each stage and identify the artifact passed to the next. Spend the extra time on the figure, rather than reciting tool names.

The first stage processes the visual evidence. It needs to identify relevant objects, estimate geometry, and track poses. Specialized components such as SAM3, SAM3D, FoundationStereo, and FoundationPose provide parts of that information.

The agent coordinates these components. It does not directly invent every depth estimate or solve every pose problem inside the language model. This division of labor is important because it tells us where the pipeline's information comes from.

The second part introduces physical priors. The system needs structured hypotheses about objects and their properties. Some quantities are difficult to infer from images alone, so the pipeline must begin with assumptions and then examine whether the resulting simulation is consistent with the observation.

Scene preparation makes those pieces executable. Geometry, poses, camera settings, and motion trajectories must agree on coordinate frames and on the simulator's representation. Even good individual estimates can fail if the conversion between them is wrong.

The last part puts the simulator in the loop. The pipeline runs a candidate episode, compares what happened with the recorded interaction, and refines the construction. Deterministic optimization and search do part of this work alongside agent decisions.

One way to read the figure is to track the intermediate artifact. After perception, we have estimates. After assembly, we have a scene. After execution, we have a replay and measurements that can guide another change. Making those artifacts explicit makes failures easier to localize.

For example, suppose the object is reconstructed poorly. A later parameter search may try to compensate for the wrong geometry. A different language-model backend might not fix the underlying defect. This is a plausible explanation for a pipeline bottleneck, not a component-level causal result established merely by the diagram.

The broader lesson is that the agent can organize a substantial robotics toolchain when each component has a defined job and returns inspectable outputs. To find out how often that workflow succeeds, we need to leave the architecture and examine the evaluation rule.

## 13. Replay Acceptance on DROID-100

> Cue: Read all three outcome categories in the left plot. Then explain the candidate/judge rule. Finally point out the logarithmic cost axis on the right. Pause after the acceptance rule to make sure the distinction is clear.

The left plot includes all one hundred sampled DROID episodes. For the best observed backend, Gemma 4 31B, forty-eight episodes meet the replay-success rule, eight are partial, and forty-four fail. Episodes that stop before a valid replay record remain in the denominator.

That denominator matters. The result describes the attempted conversion set, rather than only the subset for which the system produced an attractive video.

Now, what counts as success? The evaluator first filters reconstruction candidates using conditions such as a valid grasp probe, an existing replay video, and plausible finite motion statistics. It retains at most five candidates for judging.

Three vision-language judges compare selected real and simulated keyframes. The rubric includes the target object's identity and final location, similarity of the action, and the final gripper location. Each judge chooses its own highest-scoring candidate.

An episode passes if at least one judge's best candidate scores eight out of ten or higher. This is an acceptance rule designed to find a successful candidate. It is not majority voting, agreement between all judges, or an average score over the candidates.

That definition is legitimate, but it determines how we interpret the forty-eight. The result tells us how often the pipeline found a replay accepted under this rule. It does not directly measure the accuracy of identified friction, stiffness, or predictions under a new action.

The right plot compares model bills, and its cost axis is logarithmic. The paper reports model-call costs. Those numbers do not include the complete cost of perception, simulation, or preparation. They therefore support a comparison of the reported model usage, rather than a complete deployment-cost estimate.

The other backends produce between thirty-seven and forty-five accepted episodes. This suggests that the conversion workflow can operate with different model backends. We should avoid turning the observed ordering into a universal ranking, especially when a large fraction of failures may involve the rest of the pipeline.

For our central question, the next useful test would change the action or starting condition and compare a prediction with reality. The following demo makes clear why a beautiful replay can still leave that test unresolved.

## 14. Demo: Real2Sim and a Disclosed Failure

> Cue: Play the two author demos. The microphone excerpt is the original video's 35–60 second interval. State the dynamics failure before interpreting its animation. These demos are separate from the Agentic Real2Sim paper.

These are independent author demonstrations of an agent coordinating a Real2Sim workflow. They are not additional results from the paper we just discussed.

The described workflow combines multiple RGB views, known robot actions, camera calibration, asset construction, MuJoCo execution, and Blender rendering. Coordinating that toolchain is an interesting application in its own right.

The microphone example is especially useful because the author discloses a failure. The dynamics did not work, and the displayed result is a kinematic replay. The rigid proxy did not capture the compliant snap-fit behavior needed for the interaction.

This illustrates a possible model-class problem. If a representation cannot express the relevant deformation or contact, changing a few physical parameters may never make it predictive. That interpretation follows from the disclosed failure. It should not be generalized into a claim that all Real2Sim systems fail on such tasks.

The engineering achievement and the limitation can coexist. The agent assembled a complex workflow and produced a compelling visualization. The physical prediction remained unresolved.

We can now summarize what the world-building chapter adds to the execution chapter.

## 15. World Building: Replay and Prediction

> Cue: Trace the recording into the agent and into the comparison. Then follow the mismatch feedback. Emphasize that the top reference path and the bottom feedback path serve different roles.

Here the editable object is a scene or model, rather than the next robot action. The agent and its tools create a candidate. The simulator runs it, and comparison with the recording supplies feedback for another revision.

The reference path matters. The system is trying to explain an observed interaction. If we evaluate only against that same interaction, we are testing reconstruction consistency.

Agentic Real2Sim provides evidence that this process can produce accepted replays across a substantial attempted set, including forty-eight accepted episodes out of one hundred for the best observed backend. It also makes the remaining failures visible.

The open question is prediction. Does the resulting scene remain useful when the action changes? That requires evidence beyond matching the recording used for construction.

This gives us a choice for improvement. We can strengthen the simulator and test its predictions, or we can obtain feedback directly from the physical robot. The second route avoids relying on a reconstructed world's predictive accuracy, although it introduces the cost and difficulty of real experiments.

That is the motivation for ENPIRE. The next chapter asks what infrastructure lets a general agent run those experiments repeatedly and use their outcomes to improve a policy.

## 16. ENPIRE: Real Experiments Inside the Loop

> Cue: Play the 30-second excerpt from the original task video, source interval 300–330 seconds. It shows hardware interaction, not a complete rollout or success-rate measurement.

In ENPIRE, the agent can propose a policy change, run a real robot experiment, inspect what happened, and choose another change.

The word “improvement” can refer to several concrete artifacts. The agent might edit a heuristic program, modify a training procedure, or train a policy through the available environment. It does not need to update the general language model's own weights.

For anyone who works with robots, this should resemble part of an ordinary development day. We change something, run a trial, inspect a video or log, and try to explain the failure. Much of the time can disappear into preparing the next trial or deciding whether the previous one actually succeeded.

ENPIRE makes that surrounding workflow central. The robot needs a usable action interface. It needs hard safety constraints. It needs a way to reset and a way to report success. Without those components, the agent cannot simply repeat the experiment whenever it wants more evidence.

The video demonstrates the physical setting. The scientific question is whether a repeatable process produces better policies under a stated protocol. We will inspect the environment and improvement loop first, then reset and verification, and finally the learning curves and resource tradeoff.

This keeps the hardware demonstration connected to the claim we actually want to evaluate.

## 17. ENPIRE: Environment and Improvement

> Cue: First trace the human-assisted environment setup in the original figure. Then trace the improvement loop. Ask: “Which of these steps consumes the most time in your own robotics workflow?” Allow a short response before continuing.

The figure separates two phases that are easy to conflate when we watch a successful robot video.

During environment construction, the system uses human feedback to establish the interface and supporting tools. This includes safety constraints, automatic reset, and success verification. Once constructed, the environment exposes immutable Gym APIs to the improvement process.

That boundary gives the later experiments a stable meaning. The agent can modify its policy or training procedure, but the environment contract remains fixed during improvement. If a system could redefine success whenever its policy failed, a rising score would become difficult to interpret.

Inside that contract, policy improvement proposes and implements a change. A real rollout tests the current policy. The agent can inspect trajectories, video, and reward signals to decide what to try next.

The policy mechanism can vary. The paper explores heuristic code as well as learned approaches, including behavior cloning, reinforcement learning, and combinations with VLAs. Those are different ways of producing behavior. We should not describe the entire framework as one model learning every part of the task.

There are also two time scales. At the short time scale, a policy executes an individual trial and may react to what happens. At the longer time scale, the research agent compares evidence and changes the policy or training code for future trials. Improvement at the second time scale can persist in an artifact that later rollouts reuse.

The framework also supports multiple agent-robot pairs. Each can explore a hypothesis, and agents can exchange useful code changes. That may reduce the waiting time for a successful policy, but we will examine the resource cost separately.

Notice how much of the contribution lies around the optimizer. A clever next hypothesis is not enough if the robot cannot reset, if failures are invisible in the logs, or if the verifier gives the wrong reward. The experimental interface determines what the agent can learn from a trial.

This is why the setup phase should remain visible. The paper demonstrates autonomous improvement within an engineered environment. It does not imply that a robot can arrive in an arbitrary laboratory, establish every safety and evaluation condition by itself, and then begin reliable research.

The next slide shows two parts of that environment in operation: resetting the physical task and verifying an outcome.

## 18. ENPIRE: Reset and Verification

> Cue: Play the pin reset and zip-tie verification clips, preferably sequentially. The reset clip is about 62 seconds. They illustrate different tasks, not two synchronized stages of one rollout.

A reset turns one experiment into a repeatable experiment. If a person has to restore the scene after every failure, the agent's autonomy ends at that boundary.

The pin example shows how the environment can prepare another trial. Reset quality also affects the scientific comparison. If later policies receive easier starting states, an apparent improvement may partly come from the changed distribution rather than from the policy.

Some ENPIRE reset procedures begin at a difficult task subphase. That is a reasonable way to study a hard manipulation problem, provided we state the starting condition. Success from that condition should not be relabeled as success from any arbitrary initial state.

The second clip illustrates verification on a zip tie. The system uses visual processing to judge whether the strap passes through the head, and the paper discusses using two camera views to reduce false positives. Other tasks can use additional signals such as proprioception or torque.

The verifier supplies the outcome against which the agent improves. A false positive can reward the wrong behavior. A false negative can hide a useful change. We therefore need to distinguish a safe action interface, a correct reset, and a trustworthy success test. Each serves a different purpose.

With that infrastructure in mind, we can read the policy-improvement results more carefully.

## 19. ENPIRE: Improvement on Pin Insertion

> Cue: Read the left learning curves by backend, then the middle scaling curves by team size. Keep the retry qualification visible while discussing near-perfect final success. Ask what extra information one-shot precision would require.

This is the pin-insertion portion of the paper's result figure. The axes and legends remain visible so that we can interpret the curves in their original context.

The left curves track policy performance as research time increases. The horizontal axis concerns experimental development time. It does not measure how quickly the final policy generates an action during deployment.

The middle comparison changes the number of agent-robot pairs. More parallel experiments can reach a high-performing policy sooner. The paper reports that, for pin insertion, moving from one to eight pairs reduces the time to a near-perfect success rate from more than one and a half hours to roughly forty minutes.

Before interpreting the final success level, we need the rollout definition. ENPIRE evaluates task completion with a fixed budget of up to eight retries. Later retries can use information from the previous failure. The outcome therefore includes both initial precision and recovery within the rollout.

A near-ninety-nine-percent result under this protocol is not a ninety-nine-percent one-shot insertion rate. It is also not an independent best-of-eight experiment. The attempts are conditional, so we cannot use an independent Bernoulli formula to infer the underlying one-attempt probability.

That qualification does not make recovery unimportant. A deployed robot often needs to detect an error and try again. It means that we should credit the capability the protocol actually measures and keep its time and retry budget visible.

The result supports a concrete claim: within the defined environment, the research workflow improves policies over time, and additional parallel resources can accelerate that process.

It leaves further questions. How reliable is the policy on the first attempt? How much time does recovery add? How well does the retained policy work on new starting conditions or related tasks? Those questions need their own measurements.

There is one more distinction before we close the results. A system can discover a good policy faster while using more resources overall. The next figure makes that tradeoff explicit.

## 20. More Robots Shorten Time, but Raise Cost

> Cue: Read the utilization panel, the measured token-use curve versus its linear projection, and the time/cost panel in that order. Briefly ask whether the audience's priority is minimum elapsed time or minimum total cost.

This figure separates several meanings of scaling.

The first concerns utilization. As the fleet grows, GPU utilization can rise while average utilization per robot falls. Adding physical robots does not guarantee that every robot spends a larger fraction of its time executing useful experiments.

The next panel concerns token usage. The paper compares observed token utilization with a linear projection. These are different curves: one reports measured behavior, while the other provides a reference for how usage would grow under a simpler scaling assumption.

Finally, the figure separates tokens to success from time to success. A larger fleet can reach the objective sooner while consuming substantially more tokens. In the paper's setting, larger fleets trade token efficiency for shorter development time.

Whether that tradeoff is attractive depends on the objective. If access to a deployment window is urgent, lower elapsed time may justify higher total cost. If the budget is the constraint, the preferred configuration may differ.

For our talk, the important point is to name the quantity. Research wall-clock time, policy latency, token consumption, and robot utilization answer different questions. We should avoid summarizing all of them with the single word “efficiency.”

Together with the earlier curves, this gives a bounded view of ENPIRE's benefit: a repeatable real-experiment workflow that can improve policies, with explicit infrastructure requirements and resource tradeoffs.

## 21. Improvement: A Repeatable Real Experiment

> Cue: Follow the fixed API into policy changes and real rollout, then trace verifier outcomes and logs back to the agent. Pause before the transition to the application coda.

Here the agent changes a policy or training procedure. The physical rollout returns evidence. Verification and logs help the agent decide whether to retain the change and what to investigate next.

The fixed environment contract distinguishes this loop from unconstrained trial and error. The meaning of an action, a reset, and a success signal stays stable while the policy changes.

ENPIRE shows that this arrangement can improve robot policies under its stated protocol. Its boundaries include human-assisted setup, reset quality, verifier errors, conditional retries, and the question of transfer beyond the tested setting.

We can now compare the three chapters without comparing their percentages. In execution, the agent changes a decision. In world building, it changes a simulated scene. In improvement, it changes a policy or training procedure. Each role receives different feedback and produces a different artifact.

Before the conclusion, I want to widen the application view with two brief demos. They do not introduce a fourth detailed case study. They show other artifacts an agent can create or retain, so we can apply the same evidence questions beyond robot control itself.

## 22. Demo: Designing a Tendon-Driven Hand

> Cue: Play the CAD animation. Keep “Not a validated physical hand” visible. Ask for one physical test the design would need next.

This example moves from controlling a robot to helping design one. The author describes agent-assisted CAD and visualization, including generated geometry and an animated hand.

The resulting artifact is visually impressive. The author also states that the current design cannot directly work in reality. We should preserve both facts. This is a design artifact, rather than evidence of a manufactured, functioning hand.

A next test might examine tendon routing, friction, actuator requirements, or manufacturing tolerances, followed by a physical prototype. The right test depends on which engineering claim we want to make.

That is the same principle we used for a simulated replay: a convincing visual output is useful, but physical validity requires evidence appropriate to the artifact.

## 23. Demo: Inspecting and Repairing an Execution

> Cue: Play the 30-second ASPIRE trace-inspection excerpt. Point to the connection between recorded observations and the program being repaired. Keep this at demo depth.

ASPIRE gives another example of something an agent can retain: repaired code and reusable skills.

The project records multimodal execution traces, uses them to inspect failures, and repairs programs. The demonstration makes the relation between a physical observation and a code change visible.

A repaired skill library can preserve useful work beyond the current debugging session. This is external memory and executable code. It need not involve an update to the foundation model's weights.

To establish useful accumulation, we would test whether those retained skills help on later tasks. The video alone cannot establish open-world continual learning, and we are not adding another benchmark claim here.

Together, the hand and debugging demos show that an agent's contribution can extend beyond choosing the next action. It can help produce engineering artifacts that other parts of the robotics workflow reuse. The final question is what evidence makes those artifacts dependable.

## 24. Conclusion

Let us return to the painting robot. The interesting capability is the agent's ability to coordinate decisions and tools around a physical objective. The case studies tell us how to examine that capability more carefully.

Claude Plays Robotics shows why the control interface and time scale matter. Agentic Real2Sim shows an inspectable conversion workflow, while leaving predictive validity beyond the recorded replay as a separate test. ENPIRE shows how real hardware can support iterative policy improvement when reset, safety, and verification are in place.

The application demos expand the range of possible outputs, from physical behavior to simulated scenes, mechanical designs, and repaired programs. Their value becomes clearer when we state exactly which artifact each one produces.

My closing question is: what survives the run, and does it help on a new task?

That question gives us a concrete way to evaluate progress without losing either the excitement of the demos or the discipline of the experiments. Thank you.
