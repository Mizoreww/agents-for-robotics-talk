# Agents for Robotics — 章节主线 v0.12

讲者：Zimo Huang · 2026-09-16。38页，18段内嵌视频。英文slides，中文讲稿；建议60分钟含读图、视频与讨论，未彩排。

## Introduction（1–3）

Painting demo引出三个问题：谁产生下一条action？谁生成候选资产、回放或rollout Data？谁让下一版policy更好？三章产出不同，不是一套已经端到端打通的系统。

## 1. Control：动作决策应放在哪一层？（4–19）

**导图（4）**：保留Agent直接输出q/EEF与多种Agent Tools分支，VLA / WAM / Learned policy 合为一个 learned tools 节点。Direct不等于跳过低层servo/controller。

**常见分工（5）**：保留Hi Robot、Helix和Helix 02三张原架构图。高层推理、visuomotor policy和低层tracking是常见分工，不是所有模型必须遵守的定律。

**职责迁移（6）**：删除Hi Robot结果页。上方是原先的设计假设：System 2给semantic/subtask信息，System 1 VLA/WAM作为steerable generalist policy，承担π(a | o,l)的广泛泛化。下方是正在出现的能力模式：部分spatial grounding、action selection与参数化上移到System 2，System 1可提供更窄的primitives，System 0中的Controller保留servo/tracking。这是功能性简称，analytic tools不等于learned neural System 1。“任意输入”是理想目标，robot-data对Astra的具体训练因果仍未披露。

**旧模型的接口证据（7–8）**：Claude Plays Robotics集中讲LIBERO-40。40 tasks × 5 seeds：Opus4.6 Direct 3.5%，加MolmoAct supervision 76%，MolmoAct alone 86%。保留两张原图和不同y轴。Motor prior有用，不意味着额外Agent干预总有收益。

**工具路线（9–10）**：RPent原framework后，补首篇正式工作Harness VLA的同checkpoint表。LIBERO-Pro每方法800episodes，direct frozen π0.5为400，Harness Codex为577，CC为659。Seed0建立few-shot memory，seeds1–10评测；不是Astra、zero-shot或equal-compute的纯interface消融。

**新能力与接口（11–14）**：Robocurve两任务×三模型完整完成数，保留Direct EEF→IK实机视频。Astra bowl19/20、puzzle2/20，模型差异并不均匀。Bowl rigs与日期不同、评分不盲。Plug/keyboard是定性demo。Asim完整三任务×七条件表解释同一Astra仍受interface、observations与预算影响；ΔEEF不是q，waypoint256.6平均steps超过delta200上限。

**Direct/Hybrid代表报告（15–17）**：原架构先解释π0.5的50×14joint proposal，Astra接受1–15steps或改为1–5steps EEF correction，Direct也是1–5steps。RoboDojo十任务五aligned cases分表：13/50 vs24/50，逐任务有升有降，Score分母48/50不同。RoboLab另页保留全部任务与五方法，但属于selected final slots，含history/retries、180→500决策预算变化；历史baseline取June前五次包括失败，设置未核实一致。不能混池，也不直接归因为单个组件。

**接口与耗时（18）**：Go1确实输出12D joint residual chunks，经interpolation/PD，推理时仿真暂停。Robocurve与报告Direct输出EEF；Asim输出ΔEEF、waypoints或生成waypoint的code；Hybrid审核π0.5候选。Asim prompt-v3、medium、proprio下，180回合731次查询，mean query time为30.75 / 26.08 / 41.98秒。20/25/50 Hz是底层执行，不能当LLM Hz。社媒tool call也不等于learned atomic skill。

**总结（19）**：回到第6页，讨论更强System 2需要多通用的System 1，而不是判定tools或Direct唯一正确。语义理解和有限范围的空间迁移已有展示；实时高频反馈和跨接触/动力学条件的可靠物理泛化尚未确立。成功demo不能证明全部物理问题已解决，失败也不能唯一归因于“物理理解”。更强模型改变能力前提，仍需重测model、interface与feedback budget；不推测未披露的训练配方。

**过渡**：从下一步action，转向Agent能帮助构建什么Data。

## 2. Data：候选产物怎样成为有用数据？（20–27）

**导图（20）**：Assets / scenes、Real-to-sim Replay和Data Rollout三种产物。汇到physics与downstream value验证，不声称所有demo都跑通整条链。

**代表问题与方法（21–22）**：Real/sim视频后，Agentic Real2Sim原图解释keyframe、mask、mesh/depth/pose、tracking repair和MuJoCo scene assembly。保留deterministic sweep与LLM-assisted refinement区别。

**实验（23–24）**：DROID-100全部保留在分母。Gemma48/8/44，Qwen45/11/44，Haiku37/12/51，GPT-5.4 43/12/45（accepted/partial/failed）。最多五个候选、三个judges，任意judge的best candidate≥8/10即可accepted；仅验证replay。Model bill不是pipeline总成本。

**社区产物（25–26）**：Multi-view RGB + actions回放与Office→Newton/G1场景。手部设计从Beyond移到Data资产层：190个STEP、JavaScript动画、GLB可视化，作者明确不能直接现实运行。不把可运行场景说成新policy训练成功。

**总结（27）**：DexGPT原始三联图作为边界例子。确实执行MuJoCo并记录states/actions/contacts，但physical criteria未通过，最大penetration5.623 mm超过<5 mm标准。203个logged states是一条轨迹，不是203次试验。Replay match、physics validity、downstream training value分开验证；不再增加一篇深讲。

**过渡**：ENPIRE直接组织真实实验改进policy，不要求先完成Real2Sim。

## 3. Improvement：反馈怎样成为下一版策略？（28–36）

**问题与方法（28–30）**：导图后，[ENPIRE](https://arxiv.org/html/2606.19980v1)先在人参与下建立环境，再固定safety/reset/verifier/Gym APIs。Coding Agent修改policy/training code，运行实验并分析反馈。Reset与verification视频来自不同任务。

**具体修改（31）**：保留Figure12完整idea tree，包括无收益分支。I37、I66、I76分别改objective、batch size、controller compensation。增量来自同一次best-score轨迹，不是独立因果消融。

**物理结果（32–33）**：Pin曲线保留1→8pairs的research time改善，near-perfect从>1.5h到约40min。新表读取官方plot means：Push-T@8h normalized score为0.938/0.750/0.625；Pin@4h SR为95.5/97.5/79.0%（Codex/Claude/Kimi）。每配置四条plotted traces，不声称四次独立复现。物理rollout含≤8conditional retries，不是pass@1或独立best-of-eight。

**Simulation对照（34）**：RoboCasa原Figure6比较GR00T N1.5、CaP-X* zero-shot tools和ENPIRE autoresearch。保留原图最高aggregate bar，不估计未公开的精确数值。Reported evaluations为40个固定matched episodes，每episode一次script execution，禁reset/retry/oracle。八张示例图片不代表可推导320 pooled trials。

**新范围（35）**：四足CAD/RL开发预览和physical ICL保留。四足有四个experts与未通过状态；ICL不是权重训练或持久技能的验证。

**成本与总结（36）**：保留原Figure7并补均值±官网std：1/4/8pairs的robot/GPU active-time fractions与fleet tokens/min。更多资源能缩短研究周期，不必提高per-robot利用率；Figure7的4.5/3.2/2h不能与Figure3的40min拼接。固定协议下的policy/code improvement已有证据，不等于开放世界recursive enhancement。

## Closing（37–38）

第37页用Agent三分支框图对应Control / Data / Improvement，以及Action / Assets & rollouts / Policy update。验证要求分别是可靠执行、physics与training value、held-out gain与成本。第38页感谢与讨论。

详稿：`Speaker_Script_Revised.md`。旧结果来源：`research/results_v0_9.json`；新来源冻结：`research/evidence_v0_11_sources.json`。表格用于挑关键差异讲，不要求逐格朗读。
