# Agents for Robotics — 章节主线 v0.9

讲者：Zimo Huang · 2026-09-16。36页，18段内嵌视频。英文slides，中文讲稿；建议60分钟含读图、视频与讨论，未彩排。

## Introduction（1–3）

Painting demo引出三个问题：谁产生下一条action？谁把交互记录变成simulation？谁让下一版policy更好？三章产出不同，不是一套已经端到端打通的系统。

## 1. Control：动作决策应放在哪一层？（4–18）

**导图（4）**：保留Agent直接输出q/EEF与多种Agent Tools分支。Direct不等于跳过低层servo/controller。

**常见分工（5–6）**：上一场Hi Robot、Helix、Helix 02三张原架构图同页。Hi Robot是VLM → subtask language → π0 → action；Helix用semantic latent，Helix 02明确S2/S1/S0。Hi Robot原Figure 5与表格解释IA/TP收益，两项指标不等于episode success；主比较也改变了训练数据。所查Figure发布页没有带重复试验分母的成功率表。

**旧模型的接口证据（7–8）**：Claude Plays Robotics集中讲LIBERO-40。40 tasks × 5 seeds：Opus4.6 Direct 3.5%，加MolmoAct supervision 76%，MolmoAct alone 86%。保留两张原图和不同y轴。Motor prior有用，不意味着额外Agent干预总有收益。

**工具路线（9–10）**：RPent原framework后，补首篇正式工作Harness VLA的同checkpoint表。LIBERO-Pro每方法800episodes，direct frozen π0.5为400，Harness Codex为577，CC为659。Seed0建立few-shot memory，seeds1–10评测；不是Astra、zero-shot或equal-compute的纯interface消融。

**新能力与接口（11–14）**：Robocurve两任务×三模型完整完成数，保留Direct EEF→IK实机视频。Astra bowl19/20、puzzle2/20，模型差异并不均匀。Bowl rigs与日期不同、评分不盲。Plug/keyboard是定性demo。Asim完整三任务×七条件表解释同一Astra仍受interface、observations与预算影响；ΔEEF不是q，waypoint256.6平均steps超过delta200上限。

**Direct/Hybrid代表报告（15–17）**：原架构先解释π0.5的50×14joint proposal，Astra接受1–15steps或改为1–5steps EEF correction，Direct也是1–5steps。RoboDojo十任务五aligned cases分表：13/50 vs24/50，逐任务有升有降，Score分母48/50不同。RoboLab另页保留全部任务与五方法，但属于selected final slots，含history/retries、180→500决策预算变化；历史baseline取June前五次包括失败，设置未核实一致。不能混池，也不直接归因为单个组件。

**总结（18）**：分层有依据，却不是所有模型的能力定律。Astra内部训练配方和机器人数据因果未披露。需要重测model、interface、task和预算的组合，而不是宣布tools必需或Direct普遍胜出。

**过渡**：从“在已有世界里怎么动”转向“真实交互能留下什么模拟产物”。

## 2. Simulation：记录能变成可运行场景吗？（19–25）

**问题（19–20）**：总框图后用real/sim pair展示输入输出。目标是自动完成复杂episode conversion，不是任意单RGB视频恢复完整物理世界。

**方法（21）**：[Agentic Real2Sim](https://arxiv.org/html/2607.19190v3)组织keyframe、mask、mesh/depth/pose和tracking repair。结构化artifacts进入MuJoCo，后续deterministic sweep或LLM-assisted refinement。

**实验（22–23）**：原Figure 3和完整四backend表。100episodes全部在分母：Gemma48/8/44，Qwen45/11/44，Haiku37/12/51，GPT-5.4 43/12/45（accepted/partial/failed）。最多五个候选、三个judges，任意judge的best candidate≥8/10即accepted。Model bill分别$2.62/$12.97/$9.16/$82.30，只含model calls，不是整个pipeline成本。

**新workflow（24）**：保留Lingxiao real/sim和Office→Newton/G1 demos。它们展示作者报告的工程流程，不增加DROID100的统计证据，也不证明G1 policy重新训练。

**总结（25）**：Replay acceptance与新action/initial-state的predictive validity分开。可运行artifact是有用结果，但不等于通用physics model。

**过渡**：也可以直接组织实机实验改进policy，ENPIRE不以先运行Real2Sim为前提。

## 3. Improvement：反馈怎样成为下一版策略？（26–34）

**问题与方法（26–28）**：导图后，[ENPIRE](https://arxiv.org/html/2606.19980v1)先在人参与下建立环境，再固定safety/reset/verifier/Gym APIs。Coding Agent修改policy/training code，运行实验并分析反馈。Reset与verification视频来自不同任务。

**具体修改（29）**：保留Figure12完整idea tree，包括无收益分支。I37、I66、I76分别改objective、batch size、controller compensation。增量来自同一次best-score轨迹，不是独立因果消融。

**物理结果（30–31）**：Pin曲线保留1→8pairs的research time改善，near-perfect从>1.5h到约40min。新表读取官方plot means：Push-T@8h normalized score为0.938/0.750/0.625；Pin@4h SR为95.5/97.5/79.0%（Codex/Claude/Kimi）。每配置四条plotted traces，不声称四次独立复现。物理rollout含≤8conditional retries，不是pass@1或独立best-of-eight。

**Simulation对照（32）**：RoboCasa原Figure6比较GR00T N1.5、CaP-X* zero-shot tools和ENPIRE autoresearch。保留原图最高aggregate bar，不估计未公开的精确数值。Reported evaluations为40个固定matched episodes，每episode一次script execution，禁reset/retry/oracle。八张示例图片不代表可推导320 pooled trials。

**新范围（33）**：四足CAD/RL开发预览和physical ICL保留。四足有四个experts与未通过状态；ICL不是权重训练或持久技能的验证。

**成本与总结（34）**：保留原Figure7并补均值±官网std：1/4/8pairs的robot/GPU active-time fractions与fleet tokens/min。更多资源能缩短研究周期，不必提高per-robot利用率；Figure7的4.5/3.2/2h不能与Figure3的40min拼接。固定协议下的policy/code improvement已有证据，不等于开放世界recursive enhancement。

## Other Applications / Closing（35–36）

Tendon-hand属于结构设计/CAD动画，不是可工作的物理手。最后回到不同产物与验证边界，讨论哪一步分工值得随foundation model能力重新检验。

详稿：`Speaker_Script_Revised.md`。结果来源：`research/results_v0_9.json`及两份本次结果核查笔记。章节内的结果表用于挑关键差异讲，不要求逐格朗读。
