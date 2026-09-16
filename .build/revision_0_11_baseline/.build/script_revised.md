# Agents for Robotics — 中文讲稿

讲者：Zimo Huang · 2026-09-16 · 本地修订 0.10（2026-09-14）

英文 slides，中文讲解，专有名词保留英文。建议 60 分钟包含原图读图、视频、停顿和讨论，尚未彩排计时。每章先看总框图，再沿问题、方法与证据展开；community demos 用来观察新的工作范围，不与正式实验混成排行榜。


本版用框图收束第一章和全稿。表格加粗各自比较组内的最优显示值，并列值同样加粗；human oracle、样本数和实验边界另行说明。RoboLab 加粗只表示 retained slots 的行最大值，资源表只标利用率最高或 token rate 最低，不代表统计显著性或统一效率冠军。

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

图中把 VLA / WAM / Learned policy 合到一个 learned tools 节点，不再把它们当成互斥类别。它们替 Agent 承担的工作不同。IK 和 planner 把几何目标转成可执行运动；controller code 可以在本地闭环；VLA 提供从机器人数据中学到的动作先验；WAM 把世界与动作生成联系起来。图是我们的综合，不是某篇报告测试过所有工具的声明。

无论选哪条路，机器人端仍然有 servo 或 controller，观测也仍然需要返回。今天说的 Direct，重点是是否需要一个独立 learned action policy，并不是跳过所有运动学和低层控制，直接让 LLM 输出电机力矩。

我们先看现在常见的分层方案，再问：大模型应该停在哪一层？

## 05. Hierarchical Robot Control

> 读图提示：三张都是上一场 talk 的原图。先看左边 Hi Robot，再看右侧 Helix 和 Helix 02；原图可以点击放大。

Hi Robot 的分工很直观。High-level VLM 理解任务、图像和用户的临时指令，输出一个 subtask language command；low-level π0 再把这个指令、图像和 robot state 变成 action。论文明确描述的是 two-level inference，不需要把原图中没有单列的第三个网络补进去。

Helix 用另一种接口连接高低层：System 2 输出 semantic latent，System 1 负责 visuomotor action。原 Helix 的 S2 是 7B 模型，约 7–9 Hz；S1 是 80M，200 Hz。

到了 Helix 02，三层分工更加明确：S2 给语义表示，S1 给 full-body joint targets，S0 进行 whole-body tracking 和 actuator control。官网说明 S1 是 200 Hz，S0 内部是 1 kHz；不要把原图接口上的 200 Hz 都解释成 S0 的执行频率。

可以把它概括为 reasoning、visuomotor policy、low-level control 的分工。但这是常见方案，不是一个已经证明任何模型都必须遵守的定律。先补一页 Hi Robot 的量化结果，再看 Claude 在不同接口上的实验。Figure 的两篇官方发布文展示了层次分工和演示效果，但没有公布带重复试验分母的系统成功率表；61 actions 或 1 kHz 都不能替代成功率。

## 06. Hi Robot: Instruction and Progress

> 读图提示：上面保留完整原 Figure 5，可以放大；下面只提取作者给出的 cross-task average。

这里先区分两个指标。Instruction Accuracy 衡量高层命令是否符合指令和当下观测；Task Progress 衡量有多少物体被放到正确位置或配置。它们都不是整段任务一次成功的概率。

三类实机任务包括 Table Bussing、Sandwich Making 和 Grocery Shopping，每个任务、每个方法20次 trial。Hi Robot 的两个平均值是76和81；Flat VLA 是36和44，GPT-4o high-level 加相同 low-level VLA 是30和64。Human oracle 高层也只得到89的 Task Progress，说明动作执行还有自己的限制。

这支持该系统中训练过的高层策略有价值。但 Hi Robot 的模型和 synthetic data 也变了，主图不是 data-matched hierarchy ablation。我们保留官网的整数显示值，不把76%转成成功 episodes。接下来 Claude 的实验转向另一种问题：固定某个通用模型，改变接口会怎样？

## 07. Claude Plays Robotics: Interfaces

> 读图提示：从左侧单一 LLM 出发，沿中间四种 interface 读到右侧。上面三条在 execution 端进入 Controller，最下面一条产出 Learned policy；它们不是 Controller 再生成 Policy 的串联流水线。

这里不只比较模型大小，而是比较 model、embodiment 和 interface 的组合。报告涉及 classic control、Go2/G1 locomotion 和 Franka manipulation。图先概括四种接口，下一页只展开 manipulation 的结果。

Direct action 是 LLM 输出 7D EEF motion，由低层 Controller 执行。Controller code 则让 LLM 写 Python feedback program，把快循环放到本地。Policy supervision 已有 MolmoAct 的动作提议，LLM 可以 accept、edit 或 replace，再交给 Controller。这三个分支承担的计算和反馈职责不同。

Training supervision 是另一个时间尺度：LLM 修改 RL training code，训练流程产出 Learned policy，而不是每一步都由 LLM 直接决策。这里作为接口背景，第三章再讲改进过程。

下一页的 LIBERO-40 使用40个任务、每任务5个 seeds，即每个 model / condition 200 trials。这个分母对应 manipulation 结果，不代表图里所有 embodiment 和 RL 设置都用了同一协议。

所以实验问题是：在给定模型和任务下，已有 motor prior 和 interface 的分工，怎样改变最终控制表现？

## 08. Claude: The Value of a Motor Prior

> 读图提示：两边都保留了完整 success-rate panel。纵轴范围不同，不比较柱子的视觉高度；只突出同一个 Opus 4.6。

左边 Direct 的 Opus 4.6 是 3.5%。右边 MolmoAct 加 Opus 4.6 supervision 是 76%。这说明在这组任务和模型下，learned motor prior 提供了非常大的帮助。

但右图还有一个不能忽略的 baseline：MolmoAct alone 是 86%，高于加监督后的 76%。所以结论不能写成“Agent 干预越多越好”。Supervisor 可能提供新的任务理解，也可能干扰一个原本就熟练的 policy。

报告还测试了 novel goals，其中部分 supervisor 可以帮助原 policy 做不到的事情。它的任务和评测条件不同，不能并入这里的 LIBERO-40。这里强调收益取决于目标与 policy 已有能力。

我们能从这项工作得到的是：interface 和 prior 会显著改变某个模型的控制表现。不能据此推出所有未来 LLM 都必须停留在高层。先看工具路线怎样组织成系统，再看为什么 Astra 让这个问题值得重问。

## 09. RPent: Organizing Robot Tools

> 读图提示：只沿原 framework 图讲 Agent、memory、tools、action primitives 和统一接口，不逐项展开支持列表。

RPent 是 RLinf 的 Recursive Physical Agent 项目。它把机器人操作所需的能力组织成一个可组合系统：Agent 根据任务和反馈选择工具，memory 保留工作上下文，action primitives 和统一接口连接机器人或 simulator。

它解决的是工程组织问题。感知、运动、代码和 learned policy 不必都塞进同一个接口，Agent 可以在这些能力之间协调。

这里要区分架构意图与已验证能力。图中画出的后端不代表每一个都完成了同样的评测。例如我们读过的 move_to 示例使用 OSC，不能因为名称是运动接口就一律叫 IK。

接下来不只看架构图，再看 RPent 首篇正式工作 Harness VLA 的量化实验。它能说明这套组织方式在什么条件下有效，但不能证明工具委托是唯一可能。

## 10. RPent: Harness VLA Results

> 读表提示：先看同一个 frozen π0.5-SFT baseline，再看 Harness 的两行；表中是成功次数，分母随列改变。

RPent 的官方 README 把 Harness VLA 称为首篇正式工作，论文也直接链接 RPent。这里取最新 v4 的 LIBERO-Pro Table 3，不混用其他版本和其他 benchmark。

四个 task suites 分别做 instruction redirection 和 position swap，共八个 cells。每 cell 是10 tasks乘10 held-out seeds，共100 episodes；每种方法共800。Direct frozen π0.5 是400/800，Harness VLA 的 Codex 配置是577/800，CC也就是 Claude Code 配置是659/800。

这些整数由论文每个100-trial cell的百分数求和得到，不是我们重跑或重数 raw logs。更重要的是，Harness 用 seed 0 的探索构建 memory，再在 seeds 1–10 测试；它增加 planner、analytic primitives 和计算预算。因此结果属于 few-shot harness，不是纯接口消融，也不是 Astra 的实验。

它说明同一个 learned policy 可以通过不同组织方式获得更强适应性。接下来换一个方向：foundation model 自己产生动作的能力增强后，原来的分工还需要原样保留吗？

## 11. Astra: Direct Actions in Practice

> 播放提示：两段为 Robocurve 的精选实机片段，已省略模型等待。先看 bowl，再看 precision insertion 的边界，视频不替代完整实验统计。

Robocurve 给了一个比较直接的实机例子。Astra 接收相机和 proprioception，输出 absolute EEF targets，再由 IK 和底层 controller 执行，中间没有独立 VLA。

Bowl 任务完成了 19/20，说明有些真实操作已经可以通过这条路径做得很好。但同一报告里的 round puzzle insertion 只有 2/20，所以不能由一个成功片段推论精细接触已经全面解决。

下表保留了同一个报告的全部 task × model 完成数。Bowl 中，Fable 5 和 Fable 5.1 分别是 1/20 与 8/20；Astra 是 19/20。Puzzle 中则是 0/20、2/20、2/20。提升主要出现在这组 bowl 任务，不能概括为所有精细接触均有提高。

协议也要看：每次最多 20 个 model calls，速度上限为 25%。Insertion 用同一个 rig；bowl 的 Astra 和 Fable 使用不同 rigs，Astra 还晚两天测试，人工评分知道模型身份。它不是完全隔离模型因素的随机对照。

这一页先不以 model latency 判胜负。我们关心的是能力边界：过去交给独立 System 1 的一部分 action 决策，现在是否可以由 foundation model 自己承担？

关于原因，公开资料没有披露足够的 Astra 机器人预训练配方或因果消融。因此我会说“能力前提变了，旧分工需要重测”，不会把“加入海量机器人数据导致这一提升”说成已证事实。

## 12. Astra: Visual Feedback in Action

> 播放提示：依次用视频自身的 controls 播放，不需要两段同时跑。左边源视频 12×，右边 20×；都不是 LLM 实时延迟展示。

再看两个 community demos。左边 GPT-Policy-Eval 给模型一次视频示范，再利用在线视觉反馈进行插头操作。它展示了不依赖独立 VLA 的具体行为路径，但作者明确这是 selected trials，没有完整试验分母。

右边是真实机器人操作键盘的片段。它根据屏幕与机器人反馈处理输入、退格并继续尝试。这里能看到的是反馈下的行为调整，不能仅凭动作变化断言它进行了 RL、更新了模型权重，或者已经保存了跨任务的稳定技能。

这两段比单纯说“能力更强了”具体得多：输入可以是示范或语义目标，输出已经落到真实动作。但接口仍然影响结果。下一页就固定为同一个 Astra，看不同 action 输出的公开比较。

## 13. Same Astra, Different Action Outputs

> 读图提示：先读三种输出，再看两段 Square ep00 replay 和 20 回合统计。数字下方的 budget 是解释的一部分。

这组作者公开实验使用同一 GPT-6 Astra、medium reasoning，在 Franka / robosuite 的 Square 任务上比较 ΔEEF chunks、absolute EEF waypoints，以及返回 waypoints 的 Python 程序。

结果分别是 1/20、18/20 和 16/20。ΔEEF 是 7D OSC_POSE action，不是 joint q。Code 生成的是 plan(scene)，返回至多 12 个 waypoints，再由同一个 waypoint controller 跟踪，不是任意高频闭环程序。

最重要的限制是预算没有配平。ΔEEF 最多 200 control steps / 10 queries；Square waypoint 最多 500 steps / 16 queries；code 最多 500 steps / 3 轮程序修改。Waypoint 平均用了 256.6 steps，已经超过 ΔEEF 的上限。因此不能把差距全部归因于表达方式。

这些是相同 proprio 档位，但该档位还包含 EEF 像素标记、相机尺度和固定地标，不是单纯只有关节状态。公开逐回合记录与表格数字一致，我们没有重跑实验。

另两个任务也提醒我们不要找统一赢家：Lift 三者都是 20/20；Can 则是 18/20、17/20、7/20。暂不讨论 latency，不等于忽略控制步数与反馈预算。下一页把完整三任务与不同 observation settings 放在一起，避免只挑 Square 这一行。

## 14. Astra Interfaces: Three Tasks

> 读表提示：先比较中间三个 proprio 列，再看没有 proprio 和 privileged observation 两列；不要逐格念数字。

Lift 几乎所有方式都达到20/20，无法区分接口。Can 中，ΔEEF和waypoint分别是18/20和17/20，code只有7/20。Square却相反：ΔEEF只有1/20，waypoint为18/20，code为16/20。因此没有跨任务通吃的接口赢家。

Observation 也影响解释。Square waypoint 没有 proprio 时是0/20，加入该档信息后是18/20；code换到privileged信息后是19/20。这里的 proprio 还含图像标记和固定参考，不能把差异都算成 action 表达的作用。

Script upper 与 random lower 只是这个实验的控制项。所有格子都是20 episodes，但控制步数与查询预算不同，特别是 Square 的waypoint平均256.6 steps已超过ΔEEF上限。当前结果说明 interface、observations 和预算都值得研究，不构成某种表达的纯因果优势。

## 15. Astra: Direct or Hybrid?

> 读图提示：先放大左侧报告原架构，讲完后再看右侧两段不同仿真任务的视频。片段省略 LLM 等待，只展示 control-time playback，不能用来比较端到端 latency。13/50 与 24/50 来自完整 RoboDojo 面板，不是这两个视频的对比。

用户提供的匿名报告进一步问：同一个 Astra，如果再给它一个 learned action prior 呢？这里是系统执行架构，不是 Astra 未公开的内部网络结构。

共享输入包括三个 RGB views、14D proprioception、task instruction，以及 Astra 的 history / notes。Direct 由 Astra 生成双臂 EEF position、orientation 和 gripper targets，每次执行 1–5 control steps 后重新观察。

Hybrid 先由 task-finetuned π0.5 产生 50×14 joint-space candidate。Astra 结合观测和 FK trajectory 审核，选择接受前缀 1–15 steps，或者给 1–5 steps 的 EEF correction。这是 OR 分支，不是每一次都先执行 policy 再附加 correction。图中的 joint q 来自 π0.5，不能拿它当 Astra-q versus Astra-EEF 的消融。

EEF 仍通过 local IK 和 controller 执行。25 Hz 是 native control rate，不是 LLM 的决策频率。RoboDojo 选定的 10 tasks × 5 paired cases 中，Direct 13/50，Hybrid 24/50。

这组结果说明新能力并不自动让 learned prior 失去价值。但 prior、action interface 和 executed segment length 一起变化，不能归因为单一因素。后面分两页展开 RoboDojo 与 RoboLab，先看逐任务差异，再看为什么两个结果不能混池。

## 16. RoboDojo: Per-Task Results

> 读表提示：每行是同一组选定任务的五个 aligned cases。先看总计，再看哪几类任务贡献了差异。

Hybrid 总计24/50，Direct为13/50。提升不是均匀发生的：例如fold clothes从2/5到5/5，bottles从1/5到5/5，build tower从0/5到3/5。但classify objects反而从5/5降到3/5，organize table两者都是0/5。

因此不能把总计解释成 Hybrid 对每个任务都更好。每任务只有五个cases，还是选定的十个任务，不是整个benchmark的无偏样本。

下方还区分 native Score 与 binary success。Direct有两个episode缺少可用Score，所以Score平均只基于48个；Hybrid基于50个。成功率的分母仍然都是50，失败或不完整case没有从成功率分母消失。

Learned prior、action interface和executed horizon一起变化，表只能支持这个整体配置的比较。下一页RoboLab的口径更不同，不能把两个面板合起来给Astra一个总成功率。

## 17. RoboLab: Selected Final Slots

> 读表提示：先念标题中的 selected final slots，再读数字。它不是重新采样、统一预算、各跑一次的配对benchmark。

报告每个方法、每个任务给五个final slots。Direct最终49/50，Hybrid46/50；三个historical baselines分别为18/50、18/50和17/50。这些是当前发布记录的描述性汇总，不能直接解读成公平试验下提升了多少。

Astra组保留历史结果，也包含明确允许的retries，initial states没有严格配对。Direct的最后两次BlocksInBin retry把decision budget从180提高到500。三个baseline则来自June cohort，每个任务按顺序取前五次，包括失败，不是成功样本筛选。

任务名字和slot数量一致，并不能证明task version、control settings和起点都一致。这里保留全部任务，是为了让结果透明，同时把选择规则摆在观众眼前。它带来很强的研究动机，但还需要fresh、统一预算、严格配对的评测来确定因果结论。

## 18. Where Should the Boundary Sit?

> 读图提示：上方三个并列框是我们综合现有证据提出的诊断问题，不是三种独立神经模块，也不对应 System 2 / 1 / 0。三条线汇到分工选择，不表示必须串行解决。

第一章最后不急着给 Direct 或 Tools 判胜负，先看任务卡在哪里。Semantic intent 问目标、对象和约束是否理解对；Spatial grounding 问 pose、frame 和 alignment 是否准确；Physical interaction 问能否建立并维持接触，处理 timing、误差和 recovery。三者耦合，仅看 end-to-end success 很难唯一定位失败原因。

例如 Claude 的特定 visual-tool ablation 中，10 tasks × 5 seeds，Mythos Preview 加入 Cursor tool 后成功率从6%到32%。这个例子支持 spatial aids 可以改变表现，并不说明所有操作失败都只是定位错误。Robocurve 的 bowl 和 puzzle 表现不同，也不能只归因于接触理解，因为 sensing、pose、controller 和 budget 都可能影响结果。

因此 interface 不只是一个函数名，它决定信息、计算和执行责任怎样分配。更强模型可以移动这个边界，Direct、Hybrid 和 Tools 的合适选择仍需要在具体 task、feedback 和 budget 下重测。直接输出 EEF 也仍需要底层控制。

还有一点要说准确：Hi Robot 的 Discussion 本身就说模型层面的角色分离 is not fundamental，并讨论统一模型在 inference 时承担不同角色。我们不是证明旧论文错了，而是在模型能力变化后重新测试旧设置下的瓶颈。Astra 的机器人预训练配方及因果对照仍未披露，不能由这些控制结果反推训练原因。

接下来把问题从在已有世界里怎么动，转向真实交互记录能留下什么模拟产物。

## 19. Agent Builds Simulation

> 读图提示：先讲 recording 与候选 replay 的两条路径，再沿 comparison 回到 Agent。暂不先读实验结果。

第二章只细讲 Agentic Real2Sim。问题是：已经有真实机器人交互记录，能不能自动得到对应的可运行 simulation episode，而不是人工逐件建模、对齐坐标和调参数？

输入不只是任意一段 RGB 视频，还包括同步视角、calibration、robot trajectory 和相关几何信息。Agent 组织感知、几何、scene preparation 和 simulator，产出 scene 与 replay artifacts，再利用 mismatch 修正候选。

这张图里的目标很具体：把一次已发生的交互转成可以运行和检查的产物。我们先看产物，再看 Agent 实际负责哪些决策，以及这套流程能处理多少记录。

## 20. Real Episode and Its Twin

> 播放提示：可同时播放两段。它们来自同一个 recorded episode，但这里不是逐帧同步的数值误差评测。

左边是真实记录，右边是重建后的模拟回放。这里不只是找一个长得像的 mesh：robot、camera、object pose、geometry 和 motion trajectory 必须在一致的坐标系里，simulator 才能真正运行。

这类工作有大量接口和中间产物。某个物体的位置误差，可能来自 camera calibration，也可能来自 tracking；geometry 不对，后面的参数调整又可能只是在补偿它。

所以 Agent 的潜在价值不是替代每一个几何算法，而是组织工具、检查输出，并把失败送回需要修正的位置。下一页具体看它做了哪些决定。

## 21. Agentic Real2Sim: Method

> 读图提示：沿论文原图走，重点追踪每一步交出的 artifact，而不是念工具名单。

Visual processing 首先选择对象和 keyframe，再进行 segmentation、geometry recovery、depth 和 pose tracking。Agent 可以拒绝不合适的 mask、重新选帧，也可以根据 tracking critic 的反馈更换初始化帧。

这里要区分决策与计算。SAM3、SAM3D、FoundationStereo 和 FoundationPose 等组件完成专门工作；Agent 组织这些调用并作受约束的选择，不是在语言模型内部直接算出所有 mesh 和 depth。

这些结果写成结构化 episode artifacts：object meshes、scale、pose tracks、robot trajectory、camera metadata 和 task semantics。Scene preparation 再校准 robot base 与 ground，把它们装进 MuJoCo。

后续存在两类修正路径：deterministic sweep 根据 contact / grasp outcomes 搜索 candidate，或者 LLM-assisted loop 读取 rendered keyframes 和 structured summaries 再提出 refinement。不能把每一次候选变化都描绘成 LLM 自由调参。

这项工作的主要贡献是把长链条组织成可执行、可排查的 episode conversion workflow。我们现在可以问一个明确问题：随机抽取一批真实记录，这套流程究竟完成多少？

## 22. DROID-100: Protocol and Results

> 读图提示：先看原图左侧 accepted / partial / failure，再说明判定规则。成本图只解释统计范围，不逐个念 backend 排名。

全部一百个 DROID episodes 都保留在分母里。最好的 backend Gemma 4 31B 得到 48 accepted、8 partial 和 44 failure；还没生成有效 replay 就停止的运行，也不会被排除。

这里 accepted 的定义需要说清楚。Evaluator 先筛选符合 grasp probe、视频存在以及 motion statistics 等条件的候选，最多选五个交给三个 VLM judges。Judges 比较 real 与 sim 的关键帧，关注对象身份、最终位置、动作相似性和最终 gripper 位置。

每个 judge 选自己的最佳 candidate。只要任意一个 judge 的最佳分数达到 8/10，就算通过；这不是 majority vote，也不要求三个 judge 都认可。

因此 48/100 的含义是：在这套规则下，有多少 episode 找到了 accepted replay。它不是物理参数估计准确率。右侧 model-call bill 也不是包含 perception、simulation 和 preparation 的全部成本。

下一页把四种 backend 的所有结果列出，看看只换模型之后，完成情况和 model bill 怎样变化。

## 23. Real2Sim: All Backend Results

> 读表提示：每行的前三个计数都加起来等于100；最后一列是整组100 episodes的model-call bill。

Gemma是48 accepted、8 partial、44 failed，Qwen是45、11、44，Haiku是37、12、51，GPT-5.4是43、12、45。Partial指最佳有效评分为7；6及以下或没有合法记录都计入failure。

在这套固定pipeline中，更高model bill没有带来更多observed accepted replays。GPT-5.4的82.30美元与Gemma的2.62美元，也只涵盖model calls，不能据此声称完成整个重建只需这些钱，或者速度快了多少。

这提示瓶颈可能在几何、跟踪、候选和验证的组合中，不只是推理模型强弱。但我们没有独立critic ablation，也没有统计等效性检验。Accepted replay仍不能代替新action的预测测试。下面再看社区如何把Agent的职责扩展到搭建workflow本身。

## 24. Astra Builds Simulation Workflows

> 播放提示：先看左侧 real/sim 对照，再单独播放 Office 场景。Office 片段是重建产物运行，不是完整开发过程的录屏。

左边 Lingxiao 的案例输入是 multi-view RGB 加 robot actions。作者报告 Astra 连接了 camera calibration、asset construction、physics system-ID、MuJoCo 和 Blender。视频展示的是相应回放，不是独立验证的新动作预测。

右边 Office 的作者描述了另一条链：从 office scan 的参考画面重建 Blender scene，导出 USD，再放进 Newton 让 G1 运行。我们看到的是最后的场景产物。原帖没有明确说明 G1 locomotion policy 是否新训练，所以不能把场景搭建直接讲成 Astra 学会了走路。

这两段让我们可以提出一个新的问题：Agent 的职责是否在从执行预先编排的 pipeline，扩展到编写、连接和修补 pipeline 本身？这是作者展示带来的研究问题，不是同条件对照已经量化的结论。

不过，流程构建得更自动，并不自动保证 physics 正确。最后用一张图把两种验证分开。

## 25. From Replay to Prediction

上面这条路是复现 recorded action：能否得到与真实记录相符的 replay？下面这条路则改变 action 或 initial state，问模拟器能否预测之后发生什么。

例如原记录是从左边缓慢推物体。一个场景可能把这次推得很像，却不能正确预测从另一边更快地推。Geometry、contact 和 friction 的误差可以在一条轨迹上互相补偿，因此两项能力不能直接画等号。

本章已经看到的产物是可运行、可检查的 simulation artifact。若要进一步支持 planning 或 policy learning，下一步应做新干预下的验证。

而改进策略不一定只能依靠模拟。下一章 ENPIRE 选择直接在真实机器人上组织实验，不要求先运行 Agentic Real2Sim。

## 26. Agent Improves Policy

> 读图提示：从固定 Task + API 出发，沿 Agent → rollout → verifier / logs → Agent 走一圈。强调更新对象是后续 trial 的 policy。

第三章的问题是：一次实验的反馈，怎样成为下次仍能使用的能力？这不同于 Control 里临时修正下一条 action。Agent 现在可以修改 policy code、training recipe，或训练 neural policy，让之后的 trial 使用新的版本。

ENPIRE 把这个过程放在真实机器人上。Environment 的 action、安全、reset 和 verification 接口先在人的反馈下建立，进入 improvement 阶段后固定下来。

这可以放在 robot self-improvement 的方向下讨论，但具体要看留下什么：是 policy weights、代码，还是 context？存在一个循环，并不自动意味着改进者自身获得了递归增强能力。下面先看实验环境怎样搭建。

## 27. ENPIRE: Environment and Improvement

> 读图提示：沿原图区分 human-assisted environment setup 与 autonomous improvement；不要把两阶段压成无人参与的一步。

第一阶段建立环境接口。系统在 human feedback 下实现 safety constraints、automatic reset 和 success verification。完成以后，这些能力通过固定的 Gym APIs 给下一阶段使用。

第二阶段，coding Agent 获得训练代码的修改权限。它可以读资料、提出 hypothesis、修改 BC 或 RL 程序，再调用真实 rollout，查看 trajectory、video 和 reward，判断下一步值得改什么。

这里固定环境与成功标准非常重要：策略做不好，不能通过修改 verifier 让自己看起来成功。否则分数的变化就没有稳定含义。

多个 agent–robot pairs 还可以异步试验不同想法，并通过代码协作保留有效修改。它是否真的更快、是否更省，要留给实验回答。先把支持反复试验的 reset 和 verification 看具体。

## 28. ENPIRE: Reset and Verification

> 播放提示：依次播放 pin reset 和 zip-tie verification，两段来自不同任务，不是同一个 rollout 的同步镜头。

Automatic reset 让一次机器人实验变成可重复过程。如果每次失败都需要人恢复现场，Agent 的自主实验就在这里停住。

Pin reset 展示怎样准备下一次 trial。ENPIRE 的部分任务从最困难的 subphase 开始，这是把研究聚焦到关键操作，但不能改述成任意初始状态下的完整任务能力。Reset 的状态分布也影响实验是否可比。

Zip-tie 例子展示如何检查结果。论文讨论结合多个 camera view 降低视觉 verifier 的 false positives，其他任务还可结合 proprioception 或 torque 信号。

所以 safety、reset 和 verification 是不同职责：安全不等于做对，能够 reset 也不证明 success test 可靠。把这些条件建立好后，我们终于可以看 Agent 实际改了哪些东西。

## 29. ENPIRE: What Did the Agent Change?

> 读图提示：放大 Figure 12。先读 idea tree 的实心与空心节点，再跟随虚线读下面的 best-score curve；不要逐个念所有节点。

这张原图比抽象地说“改代码、跑实验”更具体。上面每个节点是一项探索过的 idea，新的分支代表不同方向。实心绿色节点提高了 team-average best success rate，空心节点则评估过但没有收益。

例如 I37 是 BC regularization，论文在这次 run 上标注 +10.8 percentage points。后面的 I66 调整 batch size，从 1024 到 512，标注 +0.9 pp；I76 的 controller compensation 标注 +1.3 pp。

这里的重点不是记住三个数，而是看见修改对象：Agent 可以改变学习目标和训练程序，也可以改变执行补偿，而不是只负责启动训练。没有收益的分支同样是这段探索过程的一部分。

这不是三项独立随机消融，不能把这些增量当成在所有条件下都能复现的平均因果效果。下图也不是每个当前 policy 的性能，而是随 research wall-clock 推进的 team-average best score。接下来用正式 learning curve 和 scaling 实验看总体表现。

## 30. ENPIRE: Pin Insertion Curve

> 读图提示：先看随 research time 变化的性能，再看不同 fleet size；横轴不是 action inference latency。

这组结果回答两个问题：真实反馈能否支持 policy improvement，以及更多并行实验能否更早找到高性能策略。

Pin insertion 中，从一个 agent–robot pair 扩到八个，达到接近完美 success rate 的 research time，从超过一个半小时缩短到大约四十分钟。这里研究的是发现好策略需要多久，不是机器人执行一次动作有多快。

Success rate 的口径也必须保留。每个 rollout 允许最多八次 conditional retries，后续尝试可以利用前面失败的信息。因此它包含 precision 和 recovery，不是 one-shot insertion precision，也不是相互独立的 best-of-eight；不能套独立 Bernoulli 假设反推单次成功率。

在这个固定环境和 protocol 内，实验支持策略随研究推进改善，也支持并行资源带来更短 time-to-target。更快是否更省，最后再看资源图。在那之前，先补两页正式结果：两个真实任务的模型对照，以及 RoboCasa 中 tools、VLA 与 autoresearch 的对照。

## 31. ENPIRE: Two Physical Tasks

> 读图提示：左侧保留完整Figure 3和原曲线，右侧列官网实际绘图数据的终点均值。两列不是同一种分数。

Physical Push-T研究heuristic policy discovery，在8小时位置，Codex、Claude、Kimi的normalized score分别为0.938、0.750、0.625。Pin insertion研究gradient-based policy improvement，在4小时位置，success rate分别为95.5%、97.5%、79.0%。不能把Push-T的0.938改称93.8% binary success。

论文对应配置是Codex/GPT-5.5 xhigh、Claude Code/Opus4.7 High和Kimi Code/Kimi K2.6 thinking。这些不是Astra模型对比。不同任务的排序也不同，不应据此宣布统一的coding agent冠军。

官网每个configuration提供四条plotted traces及means，但没有充分披露独立seed数量或专门held-out test set的大小。我们没有把四条线叫四次独立复现。Physical rollout仍允许最多八次conditional retries，因此也不是pass@1 precision。

这些结果回答在固定实机环境中能否改进策略。下一页换到RoboCasa，观察autoresearch如何改善工具和VLA的组合，注意评测协议也会改变。

## 32. ENPIRE: Autoresearch in RoboCasa

> 读图提示：上方保留原Figure 6，包括task示例和三个aggregate bars。原图未给精确数字标签，不从柱高补造百分比。

三个对照分别是GR00T N1.5端到端VLA、CaP-X*的zero-shot agentic tool use，以及加入反复开发反馈的ENPIRE。原图中ENPIRE的aggregate最高。它说明改进对象也可以是工具调用和执行程序，不一定只能训练新权重。

例如Agent找到的策略会先用detection与motion planning移动到目标上方，再进入grasp，必要时组合VLA。关键是先根据实验反馈改程序，再检验留下来的程序。

Appendix描述的reported evaluations每项使用40个预先固定的seed/layout/style组合，同一task的方法共享这些设置。每episode运行一次generated script，禁止oracle、reset和重复retry API。不要把上一页实机最多八次conditional retries搬到这张仿真表上。

图里八张task图片是示例，不等于已披露八行数表，也不能据此乘出320 pooled trials。我们能陈述的结果是原图的相对表现，aggregate pooling的细节和精确百分比没有充分公布。

## 33. Astra: Training and Context

> 播放提示：左边四足完整 14 秒，点击原生 fullscreen 可以读九宫格状态；不要裁掉 FULL EVAL NOT MET。右边是 8× 的 physical ICL 展示，两者分别播放。

左边作者报告 Astra 参与 Fusion360 / STL 设计、simulation 和 RL 迭代。视频是九种行为的开发预览，不是九种行为全部通过验证：原片明确保留 FULL EVAL NOT MET，Wave 和 Sit 还只展示 partial first cycles，并标注四个 separate experts。实机部署仍属于后续计划。

它展示的方向是 Agent 开始覆盖设计、环境、训练和修错的一整段工程工作。开发过程来自作者描述，视频本身是训练产物预览，不是完整过程记录。

右边是 Astra 的 physical in-context learning。人给出示范，Agent 利用 context，通过已有 motion-planning tools 产生行为。作者报告 first-pass success，但没有完整试验分母；也没有由此证明模型权重更新或技能已持久化。

把它们放在一起，是为了区分 training、code revision 和 in-context adaptation。它们都可能让行为变化，但不是同一种 post-training。ENPIRE 的正式结果仍按原论文的 policy-improvement protocol 理解，不借社区 demo 增加它的成功率。

## 34. ENPIRE: Cost and Chapter Summary

> 读图提示：不逐项介绍所有指标，重点看 time-to-success 与 token-to-success 为什么可能朝相反方向变化。

更多 agent–robot pairs 可以更早找到好策略，但可能消耗更多 tokens；每台机器人的 utilization 也未必随规模单调提高。Research wall-clock、policy latency、token consumption 和 robot utilization 不是同一个“效率”。

下表来自官网 Figure 7 的精确绘图数据，保留 mean 和 std。1、4、8 对 agent–robot 的 per-robot utilization 分别约为 49.1%、30.9%、29.8%，GPU active-time fraction 为 29.4%、32.5%、49.0%；整队 token rate 是每分钟 9.3k、40.0k、140.3k。后者不是每个 Agent 的消耗，GPU 指标也不是直接读取 nvidia-smi 的 occupancy。

这些 std 的具体统计层次没有充分披露，不叫 confidence interval。Figure 7 自己的 time-to-success 是 4.5/3.2/2.0 小时，与前面 pin 曲线的约40分钟不是同一组数；不能把两个图的 token 数和时间拼成一个实验。

如果最稀缺的是研究周期，增加资源可能值得；如果预算更紧，最合适的配置就不一样。图中的实测曲线与 linear projection 也要区分，不能都当成实际运行结果。

本章可以收束为：在可重复、可验证的真实实验接口内，Agent 能把 feedback 转成后续 policy 或 training code 的改进；扩大并行度还可以缩短研究周期。Human-assisted setup、conditional retries、verifier 的可靠性与成本，都是这项结果成立的条件。

这是一种具体的 robot self-improvement 实践，不等于已证明开放世界的 recursive self-improvement。最后补充一个不属于前三类的工程应用。

## 35. Beyond: Structural Design

> 播放提示：介绍为 CAD / structural design application。动画不是物理机械手测试。

Agent 对 robotics 的帮助不止控制、建模和策略改进，还可以是结构设计。这里它生成了 tendon-hand 的设计与 animation，产物是工程方案，而不是一只已经在现实运行的机械手。

作者明确说当前设计不能直接在现实里工作。所以我们可以把它看作设计表达和迭代的起点，不能把动画当成 tendon transmission、负载、接触或可靠性验证。

下一步还需要检查 actuator requirement、routing、friction、tolerance 和装配，再制作 prototype。这些是后续工程问题，不是这个 demo 已经完成的测试。

## 36. Takeaways

> 读图提示：从 Agent 分别沿三条支路看 Role、Artifact 和 Evidence。三章是不同工作位置，不是一条已打通的端到端流水线。

最后只留三个对应关系。Control 产出 Action，要看执行是否可靠。Simulation 产出 Scene，除了重放相似，还要单独测试 new action 下是否有效。Improvement 产出下一版 Policy 或程序，要看 held-out gain 和总成本。

更强模型让这些分工值得重测，但新 demo 不能替代相应的验证。我们真正要问的是：在自己的机器人工作中，哪些信息、判断和执行责任，现在可以重新分配给 Agent？

## 37. Thank You

谢谢大家。欢迎讨论，也欢迎结合你们自己的机器人系统，说说最想让 Agent 接手哪一部分，以及需要什么实验才能放心交给它。
