# Agents for Robotics — 章节主线 v0.15

讲者：Zimo Huang · 2026-09-16。33页，18段内嵌视频。英文slides，中文讲稿；建议50.5分钟含读图、视频与讨论，未彩排。

## Introduction（1–3）

Painting demo引出三个问题：谁产生下一条action？谁生成候选资产、回放或rollout Data？谁让下一版policy更好？三章产出不同，不是一套已经端到端打通的系统。

## 1. Control：动作决策应放在哪一层？（4–16）

**导图（4）**：保留Agent直接输出q/EEF与多种Agent Tools分支，VLA / WAM / Learned policy 合为一个 learned tools 节点。Direct不等于跳过低层servo/controller。

**常见分工（5）**：保留Hi Robot、Helix和Helix 02三张原架构图。高层推理、visuomotor policy和低层tracking是常见分工，不是所有模型必须遵守的定律。

**职责迁移（6）**：接口标注为上方l→π(a | o,l)→a，下方c=(k,g)→π(a | o,c)→a；o是observation，k/g是primitive选择及目标，a为Controller target。π是功能表达，不要求所有primitive都是learned网络。删除Hi Robot结果页。上方是原先的设计假设：System 2给semantic/subtask信息，System 1 VLA/WAM作为steerable generalist policy，承担π(a | o,l)的广泛泛化。下方是正在出现的能力模式：部分spatial grounding、action selection与参数化上移到System 2，System 1可提供更窄的primitives，System 0中的Controller保留servo/tracking。这是功能性简称，analytic tools不等于learned neural System 1。“任意输入”是理想目标，robot-data对Astra的具体训练因果仍未披露。

**新能力与接口（7–10）**：第7页先突出Astra真实机器人任务表现提升，不以Direct action作为主论点；bowl的提升不外推为所有精细操作均有提升。Robocurve两任务×三模型完整完成数，保留Direct EEF→IK实机视频。Astra bowl19/20、puzzle2/20，模型差异并不均匀。Bowl rigs与日期不同、评分不盲。Plug/keyboard是更多真实机器人操作的定性demo；公开材料没有披露具体action interface，不将它们猜测成IK goal。P9增加真实code/proprio ep00（6.4秒replay，不是42.42秒wall-clock），与delta/waypoint并列。P10整列加粗Waypoint proprio仅作接口高亮，Square中非privileged最好，Can中却低于delta。Asim完整三任务×七条件表解释同一Astra仍受interface、observations与预算影响；ΔEEF不是q，waypoint256.6平均steps超过delta200上限。

**Direct/Hybrid代表报告（11–14）**：第11页原架构解释π0.5的50×14 joint proposal，Astra接受1–15 steps或改为1–5 steps EEF correction，Direct也是1–5 steps。第12页并列原报告的RoboDojo Score与SR图：Direct 13/50、Hybrid 24/50；有效Score分母分别48和50。公开baseline为重加权历史结果，不是配对重跑。第13页RoboLab原图保留五种方法：98/92/36/36/34%，每方法50 retained slots；含history/retries、Direct BlocksInBin的180→500决策预算变化，历史baseline取June前五次包括失败，设置未核实一致。第14页原报告Score热力图完整呈现十任务、Overall与七方法；只展开原DOM滚动区，未改数值/颜色。聚合改善不代表每个任务改善，更不能拆出prior、interface、horizon的独立因果。

**高latency（15）**：移除左侧接口清单，只展示Asim prompt-v3、medium、proprio设置下180回合731次query的平均30.75 / 26.08 / 41.98秒。强调数十秒等待让快速反馈困难，不将query time冒称完整闭环latency，也不将不同工作量的query排成统一速度榜。

**总结（16）**：四项能力/短板配风格一致的原生SVG小图，箭头收束到降低foundation-model latency，以及设计更好的interface/action primitive来获得更流畅、更稳定的contact-rich执行。回到第6页，讨论更强System 2需要多通用的System 1，而不是判定tools或Direct唯一正确。语义理解和有限范围的空间迁移已有展示；实时高频反馈和跨接触/动力学条件的可靠物理泛化尚未确立。成功demo不能证明全部物理问题已解决，失败也不能唯一归因于“物理理解”。更强模型改变能力前提，仍需重测model、interface与feedback budget；不推测未披露的训练配方。

**过渡**：从下一步action，转向Agent能帮助构建什么Data。

## 2. Data：用四个 Demo 看 Agent 的产物（17–22）

**导图（17）**：保留 Assets / scenes、Real-to-sim Replay、Data Rollout 三分支，汇到 physics 与 downstream value 验证。

**Office scene（18）**：参考画面 → Blender / USD → Newton / G1。大视频展示场景产物，不归因为新 locomotion policy 训练。

**Hand CAD（19）**：build123d / STEP → animation / GLB。候选机械结构，不是硬件验证。

**Multi-view replay（20）**：RGB + robot actions → reconstruction tools → simulation replay。大视频看真实/模拟视角，不外推新 action 的预测能力。

**DexGPT rollout（21）**：原20.3秒三联视频，区分 source、kinematic reference 和 contact physics。实际记录 states/actions/contacts，但 physical criteria 未通过，不制造成功率或训练收益。

**总结（22）**：三类产物分别需要可用资产、回放匹配和物理检查，最终还要验证 downstream training value。无 Agentic Real2Sim 论文方法/结果页。

## 3. Improvement：反馈怎样成为下一版策略？（23–31）

**问题与方法（23–25）**：导图后，[ENPIRE](https://arxiv.org/html/2606.19980v1)先在人参与下建立环境，再固定safety/reset/verifier/Gym APIs。Coding Agent修改policy/training code，运行实验并分析反馈。Reset与verification视频来自不同任务。

**具体修改（26）**：保留Figure12完整idea tree，包括无收益分支。I37、I66、I76分别改objective、batch size、controller compensation。增量来自同一次best-score轨迹，不是独立因果消融。

**物理结果（27–28）**：Pin曲线保留1→8pairs的research time改善，near-perfect从>1.5h到约40min。新表读取官方plot means：Push-T@8h normalized score为0.938/0.750/0.625；Pin@4h SR为95.5/97.5/79.0%（Codex/Claude/Kimi）。每配置四条plotted traces，不声称四次独立复现。物理rollout含≤8conditional retries，不是pass@1或独立best-of-eight。

**Simulation对照（29）**：RoboCasa原Figure6比较GR00T N1.5、CaP-X* zero-shot tools和ENPIRE autoresearch。保留原图最高aggregate bar，不估计未公开的精确数值。Reported evaluations为40个固定matched episodes，每episode一次script execution，禁reset/retry/oracle。八张示例图片不代表可推导320 pooled trials。

**新范围（30）**：四足CAD/RL开发预览和physical ICL保留。四足有四个experts与未通过状态；ICL不是权重训练或持久技能的验证。

**成本与总结（31）**：保留原Figure7并补均值±官网std：1/4/8pairs的robot/GPU active-time fractions与fleet tokens/min。更多资源能缩短研究周期，不必提高per-robot利用率；Figure7的4.5/3.2/2h不能与Figure3的40min拼接。固定协议下的policy/code improvement已有证据，不等于开放世界recursive enhancement。

## Closing（32–33）

第32页用Agent三分支框图对应Control / Data / Improvement，以及Action / Assets & rollouts / Policy update。验证要求分别是可靠执行、physics与training value、held-out gain与成本。第33页感谢与讨论。

详稿：`Speaker_Script_Revised.md`。旧结果来源：`research/results_v0_9.json`；新来源冻结：`research/evidence_v0_11_sources.json`。新原图来源：`research/report_figures_v0_13_sources.json`。原图可放大；挑关键差异讲，不逐格朗读。
