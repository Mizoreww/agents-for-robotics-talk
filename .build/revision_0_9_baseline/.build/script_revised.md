# Agents for Robotics — 中文讲稿

讲者：Zimo Huang · 2026-09-16 · 本地修订 0.8（2026-09-14）

英文 slides，中文讲解，专有名词保留英文。建议 60 分钟包含原图读图、视频、停顿和讨论，尚未彩排计时。每章先看总框图，再沿问题、方法与证据展开；community demos 用来观察新的工作范围，不与正式实验混成排行榜。

## 01. Agents for Robotics

大家好，我是 Zimo Huang。今天我们讨论 Agents for Robotics：当 foundation model 既能读图、写代码，也能调用机器人和模拟器接口时，它应该承担哪些工作？

我会从 Control、Simulation 和 Policy Improvement 三个位置展开。它们分别产出动作、可运行场景和下一版策略，不是一套已经端到端打通的系统。我们既看能够解释机制的研究，也看 Astra 出现后的新 demo，最后讨论哪些分工值得重新检验。

## 02. Demo: Painting with Feedback

> 播放提示：播放 painting timelapse。看目标如何变成笔触，以及后续尝试怎样调整；不要把播放速度当成 LLM 决策速度。

先看一个直观的例子。作者给 Astra 一台机器人、一支画笔和相机，让它画 Golden Gate Bridge。目标不是一串预先写好的关节角，而是一个可以由语言和视觉表达的概念。

从作者的说明看，系统会规划一段动作，再根据相机和人的反馈继续调整。人也会问它哪里可以画得更好。所以这是一个很有意思的工作流展示，但不是完全没有人工参与，也没有给出重复试验的成功率。

这段视频想引出的问题是：Agent 不再只是解释怎么做，而是在把目标变成可执行产物，并利用反馈继续工作。接下来把这些工作分开看。

## 03. Three Roles for Robotics Agents

今天有三个问题。第一，当前这一步应该怎么动，是 Agent 自己生成 action，还是交给一个 learned policy？第二，已有的真实交互记录，能不能转成可运行的 simulator scene？第三，一次实验的反馈，怎样变成下次还能复用的 policy 改进？

Control 会从常见架构和 Claude Plays Robotics 讲起，再看 Astra 的新能力。Simulation 以 Agentic Real2Sim 为代表，Improvement 以 ENPIRE 为代表。各章的 community demos 只展示新的工作范围，不扩成更多论文介绍。

这三个角色之间可以有联系，但不能把它们当成一条已经验证的流水线。例如 ENPIRE 直接使用真实机器人，不需要先运行本报告中的 Real2Sim 方法。

## 04. Agent Controls Robot

> 读图提示：从左侧 Agent 出发，先指出 Direct 分支，再顺着 Agent Tools 看不同接口，最后沿 observations 回到 Agent。

这张总框图保留了两种选择。Agent 可以直接输出 numeric action，比如 joint q 或 EEF Pose；也可以调用 IK、motion planner、controller code、VLA 或 WAM。这里的 q 和 EEF 是一般接口选项，不表示后面每个实验都测过它们。

这些接口替 Agent 承担的工作不同。IK 和 planner 把几何目标转成可执行运动；controller code 可以在本地闭环；VLA 提供从机器人数据中学到的动作先验；WAM 把世界与动作生成联系起来。图是我们的综合，不是某篇报告测试过所有工具的声明。

无论选哪条路，机器人端仍然有 servo 或 controller，观测也仍然需要返回。今天说的 Direct，重点是是否需要一个独立 learned action policy，并不是跳过所有运动学和低层控制，直接让 LLM 输出电机力矩。

我们先看现在常见的分层方案，再问：大模型应该停在哪一层？

## 05. Hierarchical Robot Control

> 读图提示：三张都是上一场 talk 的原图。先看左边 Hi Robot，再看右侧 Helix 和 Helix 02；原图可以点击放大。

Hi Robot 的分工很直观。High-level VLM 理解任务、图像和用户的临时指令，输出一个 subtask language command；low-level π0 再把这个指令、图像和 robot state 变成 action。论文明确描述的是 two-level inference，不需要把原图中没有单列的第三个网络补进去。

Helix 用另一种接口连接高低层：System 2 输出 semantic latent，System 1 负责 visuomotor action。原 Helix 的 S2 是 7B 模型，约 7–9 Hz；S1 是 80M，200 Hz。

到了 Helix 02，三层分工更加明确：S2 给语义表示，S1 给 full-body joint targets，S0 进行 whole-body tracking 和 actuator control。官网说明 S1 是 200 Hz，S0 内部是 1 kHz；不要把原图接口上的 200 Hz 都解释成 S0 的执行频率。

可以把它概括为 reasoning、visuomotor policy、low-level control 的分工。但这是常见方案，不是一个已经证明任何模型都必须遵守的定律。接下来 Claude 的实验就是在问：把通用模型放在不同接口上，会发生什么？

## 06. Claude Plays Robotics: Interfaces

这里不只比较模型大小，而是比较 model、embodiment 和 interface 的组合。报告涉及 classic control、Go2/G1 locomotion 和 Franka manipulation。为了不展开成 benchmark 清单，我们集中看 manipulation。

图中有四种分工。Direct action 是模型给动作；controller code 是模型写 Python 程序，由程序在执行端控制；policy supervision 是模型审查 learned policy 的提议；training supervision 则让模型参与 RL 训练过程。最后一类先作为接口背景，第三章再讨论改进过程。

具体到 LIBERO-40，报告使用 40 个任务、每个任务 5 个 seeds，也就是每个 model / condition 200 trials。Direct 模式输出 7D EEF motion。VLA-supervised 模式则看 MolmoAct 的动作提议，选择接受、编辑或替换。

所以实验问题不是抽象的“LLM 会不会机器人”，而是：同一个模型，把已有 motor prior 放进执行链之后，结果会变成什么？

## 07. Claude: The Value of a Motor Prior

> 读图提示：两边都保留了完整 success-rate panel。纵轴范围不同，不比较柱子的视觉高度；只突出同一个 Opus 4.6。

左边 Direct 的 Opus 4.6 是 3.5%。右边 MolmoAct 加 Opus 4.6 supervision 是 76%。这说明在这组任务和模型下，learned motor prior 提供了非常大的帮助。

但右图还有一个不能忽略的 baseline：MolmoAct alone 是 86%，高于加监督后的 76%。所以结论不能写成“Agent 干预越多越好”。Supervisor 可能提供新的任务理解，也可能干扰一个原本就熟练的 policy。

报告还测试了 novel goals，其中部分 supervisor 可以帮助原 policy 做不到的事情。这里不再增加另一张结果表，只强调这种收益取决于目标与 policy 已有能力。

我们能从这项工作得到的是：interface 和 prior 会显著改变某个模型的控制表现。不能据此推出所有未来 LLM 都必须停留在高层。先看工具路线怎样组织成系统，再看为什么 Astra 让这个问题值得重问。

## 08. RPent: Organizing Robot Tools

> 读图提示：只沿原 framework 图讲 Agent、memory、tools、action primitives 和统一接口，不逐项展开支持列表。

RPent 是 RLinf 的 Recursive Physical Agent 项目。它把机器人操作所需的能力组织成一个可组合系统：Agent 根据任务和反馈选择工具，memory 保留工作上下文，action primitives 和统一接口连接机器人或 simulator。

它解决的是工程组织问题。感知、运动、代码和 learned policy 不必都塞进同一个接口，Agent 可以在这些能力之间协调。

这里要区分架构意图与已验证能力。图中画出的后端不代表每一个都完成了同样的评测。例如我们读过的 move_to 示例使用 OSC，不能因为名称是运动接口就一律叫 IK。

RPent 说明工具路线可以怎样实现，不证明工具委托是唯一可能。下一步要看的是：当 foundation model 本身的直接动作能力变强，这个分工是否还应该保持原样？

## 09. Astra: Direct Actions in Practice

> 播放提示：两段为 Robocurve 的精选实机片段，已省略模型等待。先看 bowl，再看 precision insertion 的边界，视频不替代完整实验统计。

Robocurve 给了一个比较直接的实机例子。Astra 接收相机和 proprioception，输出 absolute EEF targets，再由 IK 和底层 controller 执行，中间没有独立 VLA。

Bowl 任务完成了 19/20，说明有些真实操作已经可以通过这条路径做得很好。但同一报告里的 round puzzle insertion 只有 2/20，所以不能由一个成功片段推论精细接触已经全面解决。

这一页先不以 model latency 判胜负。我们关心的是能力边界：过去交给独立 System 1 的一部分 action 决策，现在是否可以由 foundation model 自己承担？

关于原因，公开资料没有披露足够的 Astra 机器人预训练配方或因果消融。因此我会说“能力前提变了，旧分工需要重测”，不会把“加入海量机器人数据导致这一提升”说成已证事实。

## 10. Astra: Visual Feedback in Action

> 播放提示：依次用视频自身的 controls 播放，不需要两段同时跑。左边源视频 12×，右边 20×；都不是 LLM 实时延迟展示。

再看两个 community demos。左边 GPT-Policy-Eval 给模型一次视频示范，再利用在线视觉反馈进行插头操作。它展示了不依赖独立 VLA 的具体行为路径，但作者明确这是 selected trials，没有完整试验分母。

右边是真实机器人操作键盘的片段。它根据屏幕与机器人反馈处理输入、退格并继续尝试。这里能看到的是反馈下的行为调整，不能仅凭动作变化断言它进行了 RL、更新了模型权重，或者已经保存了跨任务的稳定技能。

这两段比单纯说“能力更强了”具体得多：输入可以是示范或语义目标，输出已经落到真实动作。但接口仍然影响结果。下一页就固定为同一个 Astra，看不同 action 输出的公开比较。

## 11. Same Astra, Different Action Outputs

> 读图提示：先读三种输出，再看两段 Square ep00 replay 和 20 回合统计。数字下方的 budget 是解释的一部分。

这组作者公开实验使用同一 GPT-6 Astra、medium reasoning，在 Franka / robosuite 的 Square 任务上比较 ΔEEF chunks、absolute EEF waypoints，以及返回 waypoints 的 Python 程序。

结果分别是 1/20、18/20 和 16/20。ΔEEF 是 7D OSC_POSE action，不是 joint q。Code 生成的是 plan(scene)，返回至多 12 个 waypoints，再由同一个 waypoint controller 跟踪，不是任意高频闭环程序。

最重要的限制是预算没有配平。ΔEEF 最多 200 control steps / 10 queries；Square waypoint 最多 500 steps / 16 queries；code 最多 500 steps / 3 轮程序修改。Waypoint 平均用了 256.6 steps，已经超过 ΔEEF 的上限。因此不能把差距全部归因于表达方式。

这些是相同 proprio 档位，但该档位还包含 EEF 像素标记、相机尺度和固定地标，不是单纯只有关节状态。公开逐回合记录与表格数字一致，我们没有重跑实验。

另两个任务也提醒我们不要找统一赢家：Lift 三者都是 20/20；Can 则是 18/20、17/20、7/20。暂不讨论 latency，不等于忽略控制步数与反馈预算。当前结果支持继续研究 interface，而不是宣布某一种接口永远最佳。

## 12. Astra: Direct or Hybrid?

> 读图提示：先放大左侧报告原架构，讲完后再看右侧两段不同仿真任务的视频。片段省略 LLM 等待，只展示 control-time playback，不能用来比较端到端 latency。13/50 与 24/50 来自完整 RoboDojo 面板，不是这两个视频的对比。

用户提供的匿名报告进一步问：同一个 Astra，如果再给它一个 learned action prior 呢？这里是系统执行架构，不是 Astra 未公开的内部网络结构。

共享输入包括三个 RGB views、14D proprioception、task instruction，以及 Astra 的 history / notes。Direct 由 Astra 生成双臂 EEF position、orientation 和 gripper targets，每次执行 1–5 control steps 后重新观察。

Hybrid 先由 task-finetuned π0.5 产生 50×14 joint-space candidate。Astra 结合观测和 FK trajectory 审核，选择接受前缀 1–15 steps，或者给 1–5 steps 的 EEF correction。这是 OR 分支，不是每一次都先执行 policy 再附加 correction。图中的 joint q 来自 π0.5，不能拿它当 Astra-q versus Astra-EEF 的消融。

EEF 仍通过 local IK 和 controller 执行。25 Hz 是 native control rate，不是 LLM 的决策频率。RoboDojo 选定的 10 tasks × 5 paired cases 中，Direct 13/50，Hybrid 24/50。

这组结果说明新能力并不自动让 learned prior 失去价值。但 prior、action interface 和 executed segment length 一起变化，不能归因为单一因素。RoboLab 的最终选留 slots 不与这里混池。到这里，我们再回到章首的问题。

## 13. Where Should the Boundary Sit?

这一章并不是要在 Direct 和 Tools 之间选一个永久赢家。Hi Robot 和 Figure 展示常见分层；Claude 的实验展示当时模型怎样受益于 motor prior；RPent 把工具组织起来；Astra 则让直接动作的适用范围值得重新检验。

图里的两条路都通向 low-level control。真正变化的是：哪些 action 决策由 foundation model 自己承担，哪些仍值得交给独立 learned policy。答案可能随模型、任务、观测、interface 和预算而变。

新的 demo 可以提出问题，但还需要同模型、同观测、同控制预算的比较来回答。我们既不把旧实验作废，也不把它们在某些设置中的结论当成未来的能力上限。

接下来把 Agent 的位置往前移：不只是控制一个已有世界，而是把已经记录的真实交互转成可运行的模拟场景。

## 14. Agent Builds Simulation

> 读图提示：先讲 recording 与候选 replay 的两条路径，再沿 comparison 回到 Agent。暂不先读实验结果。

第二章只细讲 Agentic Real2Sim。问题是：已经有真实机器人交互记录，能不能自动得到对应的可运行 simulation episode，而不是人工逐件建模、对齐坐标和调参数？

输入不只是任意一段 RGB 视频，还包括同步视角、calibration、robot trajectory 和相关几何信息。Agent 组织感知、几何、scene preparation 和 simulator，产出 scene 与 replay artifacts，再利用 mismatch 修正候选。

这张图里的目标很具体：把一次已发生的交互转成可以运行和检查的产物。我们先看产物，再看 Agent 实际负责哪些决策，以及这套流程能处理多少记录。

## 15. Real Episode and Its Twin

> 播放提示：可同时播放两段。它们来自同一个 recorded episode，但这里不是逐帧同步的数值误差评测。

左边是真实记录，右边是重建后的模拟回放。这里不只是找一个长得像的 mesh：robot、camera、object pose、geometry 和 motion trajectory 必须在一致的坐标系里，simulator 才能真正运行。

这类工作有大量接口和中间产物。某个物体的位置误差，可能来自 camera calibration，也可能来自 tracking；geometry 不对，后面的参数调整又可能只是在补偿它。

所以 Agent 的潜在价值不是替代每一个几何算法，而是组织工具、检查输出，并把失败送回需要修正的位置。下一页具体看它做了哪些决定。

## 16. Agentic Real2Sim: Method

> 读图提示：沿论文原图走，重点追踪每一步交出的 artifact，而不是念工具名单。

Visual processing 首先选择对象和 keyframe，再进行 segmentation、geometry recovery、depth 和 pose tracking。Agent 可以拒绝不合适的 mask、重新选帧，也可以根据 tracking critic 的反馈更换初始化帧。

这里要区分决策与计算。SAM3、SAM3D、FoundationStereo 和 FoundationPose 等组件完成专门工作；Agent 组织这些调用并作受约束的选择，不是在语言模型内部直接算出所有 mesh 和 depth。

这些结果写成结构化 episode artifacts：object meshes、scale、pose tracks、robot trajectory、camera metadata 和 task semantics。Scene preparation 再校准 robot base 与 ground，把它们装进 MuJoCo。

后续存在两类修正路径：deterministic sweep 根据 contact / grasp outcomes 搜索 candidate，或者 LLM-assisted loop 读取 rendered keyframes 和 structured summaries 再提出 refinement。不能把每一次候选变化都描绘成 LLM 自由调参。

这项工作的主要贡献是把长链条组织成可执行、可排查的 episode conversion workflow。我们现在可以问一个明确问题：随机抽取一批真实记录，这套流程究竟完成多少？

## 17. DROID-100: Protocol and Results

> 读图提示：先看原图左侧 accepted / partial / failure，再说明判定规则。成本图只解释统计范围，不逐个念 backend 排名。

全部一百个 DROID episodes 都保留在分母里。最好的 backend Gemma 4 31B 得到 48 accepted、8 partial 和 44 failure；还没生成有效 replay 就停止的运行，也不会被排除。

这里 accepted 的定义需要说清楚。Evaluator 先筛选符合 grasp probe、视频存在以及 motion statistics 等条件的候选，最多选五个交给三个 VLM judges。Judges 比较 real 与 sim 的关键帧，关注对象身份、最终位置、动作相似性和最终 gripper 位置。

每个 judge 选自己的最佳 candidate。只要任意一个 judge 的最佳分数达到 8/10，就算通过；这不是 majority vote，也不要求三个 judge 都认可。

因此 48/100 的含义是：在这套规则下，有多少 episode 找到了 accepted replay。它不是物理参数估计准确率。右侧 model-call bill 也不是包含 perception、simulation 和 preparation 的全部成本。

有了这个可衡量的起点，我们再看 Astra 社区出现的更自由的构建方式。接下来的视频不与这一百个 episode 混成同一个实验。

## 18. Astra Builds Simulation Workflows

> 播放提示：先看左侧 real/sim 对照，再单独播放 Office 场景。Office 片段是重建产物运行，不是完整开发过程的录屏。

左边 Lingxiao 的案例输入是 multi-view RGB 加 robot actions。作者报告 Astra 连接了 camera calibration、asset construction、physics system-ID、MuJoCo 和 Blender。视频展示的是相应回放，不是独立验证的新动作预测。

右边 Office 的作者描述了另一条链：从 office scan 的参考画面重建 Blender scene，导出 USD，再放进 Newton 让 G1 运行。我们看到的是最后的场景产物。原帖没有明确说明 G1 locomotion policy 是否新训练，所以不能把场景搭建直接讲成 Astra 学会了走路。

这两段让我们可以提出一个新的问题：Agent 的职责是否在从执行预先编排的 pipeline，扩展到编写、连接和修补 pipeline 本身？这是作者展示带来的研究问题，不是同条件对照已经量化的结论。

不过，流程构建得更自动，并不自动保证 physics 正确。最后用一张图把两种验证分开。

## 19. From Replay to Prediction

上面这条路是复现 recorded action：能否得到与真实记录相符的 replay？下面这条路则改变 action 或 initial state，问模拟器能否预测之后发生什么。

例如原记录是从左边缓慢推物体。一个场景可能把这次推得很像，却不能正确预测从另一边更快地推。Geometry、contact 和 friction 的误差可以在一条轨迹上互相补偿，因此两项能力不能直接画等号。

本章已经看到的产物是可运行、可检查的 simulation artifact。若要进一步支持 planning 或 policy learning，下一步应做新干预下的验证。

而改进策略不一定只能依靠模拟。下一章 ENPIRE 选择直接在真实机器人上组织实验，不要求先运行 Agentic Real2Sim。

## 20. Agent Improves Policy

> 读图提示：从固定 Task + API 出发，沿 Agent → rollout → verifier / logs → Agent 走一圈。强调更新对象是后续 trial 的 policy。

第三章的问题是：一次实验的反馈，怎样成为下次仍能使用的能力？这不同于 Control 里临时修正下一条 action。Agent 现在可以修改 policy code、training recipe，或训练 neural policy，让之后的 trial 使用新的版本。

ENPIRE 把这个过程放在真实机器人上。Environment 的 action、安全、reset 和 verification 接口先在人的反馈下建立，进入 improvement 阶段后固定下来。

这可以放在 robot self-improvement 的方向下讨论，但具体要看留下什么：是 policy weights、代码，还是 context？存在一个循环，并不自动意味着改进者自身获得了递归增强能力。下面先看实验环境怎样搭建。

## 21. ENPIRE: Environment and Improvement

> 读图提示：沿原图区分 human-assisted environment setup 与 autonomous improvement；不要把两阶段压成无人参与的一步。

第一阶段建立环境接口。系统在 human feedback 下实现 safety constraints、automatic reset 和 success verification。完成以后，这些能力通过固定的 Gym APIs 给下一阶段使用。

第二阶段，coding Agent 获得训练代码的修改权限。它可以读资料、提出 hypothesis、修改 BC 或 RL 程序，再调用真实 rollout，查看 trajectory、video 和 reward，判断下一步值得改什么。

这里固定环境与成功标准非常重要：策略做不好，不能通过修改 verifier 让自己看起来成功。否则分数的变化就没有稳定含义。

多个 agent–robot pairs 还可以异步试验不同想法，并通过代码协作保留有效修改。它是否真的更快、是否更省，要留给实验回答。先把支持反复试验的 reset 和 verification 看具体。

## 22. ENPIRE: Reset and Verification

> 播放提示：依次播放 pin reset 和 zip-tie verification，两段来自不同任务，不是同一个 rollout 的同步镜头。

Automatic reset 让一次机器人实验变成可重复过程。如果每次失败都需要人恢复现场，Agent 的自主实验就在这里停住。

Pin reset 展示怎样准备下一次 trial。ENPIRE 的部分任务从最困难的 subphase 开始，这是把研究聚焦到关键操作，但不能改述成任意初始状态下的完整任务能力。Reset 的状态分布也影响实验是否可比。

Zip-tie 例子展示如何检查结果。论文讨论结合多个 camera view 降低视觉 verifier 的 false positives，其他任务还可结合 proprioception 或 torque 信号。

所以 safety、reset 和 verification 是不同职责：安全不等于做对，能够 reset 也不证明 success test 可靠。把这些条件建立好后，我们终于可以看 Agent 实际改了哪些东西。

## 23. ENPIRE: What Did the Agent Change?

> 读图提示：放大 Figure 12。先读 idea tree 的实心与空心节点，再跟随虚线读下面的 best-score curve；不要逐个念所有节点。

这张原图比抽象地说“改代码、跑实验”更具体。上面每个节点是一项探索过的 idea，新的分支代表不同方向。实心绿色节点提高了 team-average best success rate，空心节点则评估过但没有收益。

例如 I37 是 BC regularization，论文在这次 run 上标注 +10.8 percentage points。后面的 I66 调整 batch size，从 1024 到 512，标注 +0.9 pp；I76 的 controller compensation 标注 +1.3 pp。

这里的重点不是记住三个数，而是看见修改对象：Agent 可以改变学习目标和训练程序，也可以改变执行补偿，而不是只负责启动训练。没有收益的分支同样是这段探索过程的一部分。

这不是三项独立随机消融，不能把这些增量当成在所有条件下都能复现的平均因果效果。下图也不是每个当前 policy 的性能，而是随 research wall-clock 推进的 team-average best score。接下来用正式 learning curve 和 scaling 实验看总体表现。

## 24. ENPIRE: Pin Insertion Curve

> 读图提示：先看随 research time 变化的性能，再看不同 fleet size；横轴不是 action inference latency。

这组结果回答两个问题：真实反馈能否支持 policy improvement，以及更多并行实验能否更早找到高性能策略。

Pin insertion 中，从一个 agent–robot pair 扩到八个，达到接近完美 success rate 的 research time，从超过一个半小时缩短到大约四十分钟。这里研究的是发现好策略需要多久，不是机器人执行一次动作有多快。

Success rate 的口径也必须保留。每个 rollout 允许最多八次 conditional retries，后续尝试可以利用前面失败的信息。因此它包含 precision 和 recovery，不是 one-shot insertion precision，也不是相互独立的 best-of-eight；不能套独立 Bernoulli 假设反推单次成功率。

在这个固定环境和 protocol 内，实验支持策略随研究推进改善，也支持并行资源带来更短 time-to-target。更快是否更省，最后再看资源图。在那之前，用两个 Astra demo 区分新的训练工作范围与另一种 adaptation 路径。

## 25. Astra: Training and Context

> 播放提示：左边四足完整 14 秒，点击原生 fullscreen 可以读九宫格状态；不要裁掉 FULL EVAL NOT MET。右边是 8× 的 physical ICL 展示，两者分别播放。

左边作者报告 Astra 参与 Fusion360 / STL 设计、simulation 和 RL 迭代。视频是九种行为的开发预览，不是九种行为全部通过验证：原片明确保留 FULL EVAL NOT MET，Wave 和 Sit 还只展示 partial first cycles，并标注四个 separate experts。实机部署仍属于后续计划。

它展示的方向是 Agent 开始覆盖设计、环境、训练和修错的一整段工程工作。开发过程来自作者描述，视频本身是训练产物预览，不是完整过程记录。

右边是 Astra 的 physical in-context learning。人给出示范，Agent 利用 context，通过已有 motion-planning tools 产生行为。作者报告 first-pass success，但没有完整试验分母；也没有由此证明模型权重更新或技能已持久化。

把它们放在一起，是为了区分 training、code revision 和 in-context adaptation。它们都可能让行为变化，但不是同一种 post-training。ENPIRE 的正式结果仍按原论文的 policy-improvement protocol 理解，不借社区 demo 增加它的成功率。

## 26. ENPIRE: Cost and Chapter Summary

> 读图提示：不逐项介绍所有指标，重点看 time-to-success 与 token-to-success 为什么可能朝相反方向变化。

更多 agent–robot pairs 可以更早找到好策略，但可能消耗更多 tokens；每台机器人的 utilization 也未必随规模单调提高。Research wall-clock、policy latency、token consumption 和 robot utilization 不是同一个“效率”。

如果最稀缺的是研究周期，增加资源可能值得；如果预算更紧，最合适的配置就不一样。图中的实测曲线与 linear projection 也要区分，不能都当成实际运行结果。

本章可以收束为：在可重复、可验证的真实实验接口内，Agent 能把 feedback 转成后续 policy 或 training code 的改进；扩大并行度还可以缩短研究周期。Human-assisted setup、conditional retries、verifier 的可靠性与成本，都是这项结果成立的条件。

这是一种具体的 robot self-improvement 实践，不等于已证明开放世界的 recursive self-improvement。最后补充一个不属于前三类的工程应用。

## 27. Beyond: Structural Design

> 播放提示：介绍为 CAD / structural design application。动画不是物理机械手测试。

Agent 对 robotics 的帮助不止控制、建模和策略改进，还可以是结构设计。这里它生成了 tendon-hand 的设计与 animation，产物是工程方案，而不是一只已经在现实运行的机械手。

作者明确说当前设计不能直接在现实里工作。所以我们可以把它看作设计表达和迭代的起点，不能把动画当成 tendon transmission、负载、接触或可靠性验证。

下一步还需要检查 actuator requirement、routing、friction、tolerance 和装配，再制作 prototype。这些是后续工程问题，不是这个 demo 已经完成的测试。

## 28. Changing the Division of Work

最后回到三个产物。Control 留下的是动作；Simulation 留下的是可运行场景；Improvement 留下的是下一版 policy 或程序。它们需要不同的验证，不能放进同一张成功率排行榜。

过去常见的分工有实际依据，但 foundation model 能力在变化。Astra 的直接控制和工程 demo 让我们有理由重新问：哪些步骤还应固定在外部 policy 或手写 pipeline 里，哪些可以交给 Agent 来生成、连接和修正？

今天的态度不是宣布旧论文作废，也不是从几个漂亮视频断言所有问题解决。用原工作解释机制，用实验限定结论，再用新能力提出更好的问题。

可以把最后的讨论留给这个问题：在你们自己的机器人工作中，最值得重新划分给 Agent 的是哪一步？谢谢大家。
