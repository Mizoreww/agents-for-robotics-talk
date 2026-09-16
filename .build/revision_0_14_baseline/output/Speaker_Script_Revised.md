# Agents for Robotics — 中文讲稿

讲者：Zimo Huang · 2026-09-16 · 本地修订 0.13（2026-09-15）

英文 slides，中文讲解，专有名词保留英文。建议 55 分钟包含原图读图、视频、停顿和讨论，尚未彩排计时。每章先看总框图，再沿问题、方法与证据展开；community demos 用来观察新的工作范围，不与正式实验混成排行榜。


本版以职责迁移串起 Control：从 generalist VLA / WAM 承担泛化，直接进入 Astra 的能力、接口与 Direct/Hybrid 证据。表格加粗各自比较组内的最优显示值，并列值同样加粗；human oracle、样本数和实验边界另行说明。RoboDojo/RoboLab使用原报告结果图，RoboLab仍是retained slots口径，资源表只标利用率最高或 token rate 最低，不代表统计显著性或统一效率冠军。



## 建议时间安排

| Slide | Title | Minutes | Start |
|---:|---|---:|---:|
| 01 | Agents for Robotics | 0.5 | 00:00 |
| 02 | Demo: Painting with Feedback | 1 | 00:30 |
| 03 | Three Roles for Robotics Agents | 1 | 01:30 |
| 04 | Agent Controls Robot | 1.5 | 02:30 |
| 05 | Hierarchical Robot Control | 2 | 04:00 |
| 06 | Where Does Generalization Live? | 2 | 06:00 |
| 07 | Astra: Stronger Real-Robot Performance | 2 | 08:00 |
| 08 | Astra: More Real-Robot Demos | 1 | 10:00 |
| 09 | Same Astra, Different Action Outputs | 2 | 11:00 |
| 10 | Astra Interfaces: Three Tasks | 1.5 | 13:00 |
| 11 | Astra: Direct or Hybrid? | 2.5 | 14:30 |
| 12 | RoboDojo: Overall Results | 2 | 17:00 |
| 13 | RoboLab: Overall Results | 2 | 19:00 |
| 14 | RoboDojo: Task-Level Patterns | 1.5 | 21:00 |
| 15 | Astra Interfaces and Query Time | 1.5 | 22:30 |
| 16 | Control: Strengths and Open Gaps | 1 | 24:00 |
| 17 | Agent Creates Data | 1 | 25:00 |
| 18 | Real Episode and Its Twin | 1.5 | 26:00 |
| 19 | Agentic Real2Sim: Method | 3 | 27:30 |
| 20 | DROID-100: Protocol and Results | 1.5 | 30:30 |
| 21 | Real2Sim: All Backend Results | 2 | 32:00 |
| 22 | Data: Replay and Scene Assets | 1 | 34:00 |
| 23 | Data: Mechanism and CAD Assets | 1 | 35:00 |
| 24 | Data: Physics and Training Value | 1 | 36:00 |
| 25 | Agent Improves Policy | 1 | 37:00 |
| 26 | ENPIRE: Environment and Improvement | 2 | 38:00 |
| 27 | ENPIRE: Reset and Verification | 1.5 | 40:00 |
| 28 | ENPIRE: What Did the Agent Change? | 2.5 | 41:30 |
| 29 | ENPIRE: Pin Insertion Curve | 2 | 44:00 |
| 30 | ENPIRE: Two Physical Tasks | 2.5 | 46:00 |
| 31 | ENPIRE: Autoresearch in RoboCasa | 1.5 | 48:30 |
| 32 | Astra: Training and Context | 1 | 50:00 |
| 33 | ENPIRE: Cost and Chapter Summary | 2.5 | 51:00 |
| 34 | Takeaways | 1 | 53:30 |
| 35 | Thank You | 0.5 | 54:30 |

## 01. Agents for Robotics

建议 0.5 分钟（含读图、视频及停顿）。

大家好，我是 Zimo Huang。今天我们讨论 Agents for Robotics：当 foundation model 既能读图、写代码，也能调用机器人和模拟器接口时，它应该承担哪些工作？

我会从 Control、Data 和 Policy Improvement 三个位置展开。它们分别产出动作、候选资产与轨迹数据，以及下一版策略，不是一套已经端到端打通的系统。我们既看能够解释机制的研究，也看 Astra 出现后的新 demo，最后讨论哪些分工值得重新检验。


## 02. Demo: Painting with Feedback

建议 1 分钟（含读图、视频及停顿）。

> 播放提示：播放 painting timelapse。看目标如何变成笔触，以及后续尝试怎样调整；不要把播放速度当成 LLM 决策速度。

先看一个直观的例子。作者给 Astra 一台机器人、一支画笔和相机，让它画 Golden Gate Bridge。目标不是一串预先写好的关节角，而是一个可以由语言和视觉表达的概念。

从作者的说明看，系统会规划一段动作，再根据相机和人的反馈继续调整。人也会问它哪里可以画得更好。所以这是一个很有意思的工作流展示，但不是完全没有人工参与，也没有给出重复试验的成功率。

这段视频想引出的问题是：Agent 不再只是解释怎么做，而是在把目标变成可执行产物，并利用反馈继续工作。接下来把这些工作分开看。

### 参考来源

- [@cdngdev, X demo and method thread (8 Sep 2026)](https://x.com/cdngdev/status/2097339677128982873)

## 03. Three Roles for Robotics Agents

建议 1 分钟（含读图、视频及停顿）。

今天有三个问题。第一，当前这一步应该怎么动，是 Agent 自己生成 action，还是交给 learned policy？第二，Agent 能帮助生成什么 Data：assets、Real-to-sim Replay，还是执行出来的 Data Rollout？第三，一次实验反馈怎样变成下一次还能复用的 policy 改进？

Control 围绕一个问题展开：机器人泛化能力应该主要由哪一层承担？先看把希望寄托于 generalist VLA / WAM 的分工，再用Astra 的实机、接口与 Direct/Hybrid 证据，检查哪些空间理解和动作决策可以上移到 Agent。Data 仍只细讲 Agentic Real2Sim，随后用几个 demo 区分场景、回放和设计资产。Improvement 以 ENPIRE 为代表。Tendon-hand 设计就是 Data 资产层的一个例子。

这三个角色可以联系起来，但不是已经验证的流水线。例如 ENPIRE 直接使用真实机器人，不需要先运行本报告中的 Real2Sim 方法。


## 04. Agent Controls Robot

建议 1.5 分钟（含读图、视频及停顿）。

> 读图提示：从左侧 Agent 出发，先指出 Direct 分支，再顺着 Agent Tools 看不同接口，最后沿 observations 回到 Agent。

这张总框图保留了两种选择。Agent 可以直接输出 numeric action，比如 joint q 或 EEF Pose；也可以调用 IK、motion planner、controller code、VLA 或 WAM。这里的 q 和 EEF 是一般接口选项，不表示后面每个实验都测过它们。

图中把 VLA / WAM / Learned policy 合到一个 learned tools 节点，不再把它们当成互斥类别。它们替 Agent 承担的工作不同。IK 和 planner 把几何目标转成可执行运动；controller code 可以在本地闭环；VLA 提供从机器人数据中学到的动作先验；WAM 把世界与动作生成联系起来。图是我们的综合，不是某篇报告测试过所有工具的声明。

无论选哪条路，机器人端仍然有 servo 或 controller，观测也仍然需要返回。今天说的 Direct，重点是是否需要一个独立 learned action policy，并不是跳过所有运动学和低层控制，直接让 LLM 输出电机力矩。

这章不把工具多少作为主问题。我们关心的是：通用的任务理解、空间泛化和动作决策由谁完成，执行层又必须保留哪些能力？先看常见分层，再用一张示意图把这条主线说清楚。

### 参考来源

- [Robocurve · GPT-6 Astra direct EEF evaluation (Sep 2026)](https://openai.robocurve.org/gpt-6-astra/)
- [Astra control dashboard · prompt-v3, same-model interface records; unequal budgets](https://asimfish.github.io/astra-control-dashboard/#sec3)
- [Technical report · GPT 6 Astra as an Embodied Policy (result images captured 15 Sep 2026)](https://anonymous-report-421.github.io/public-website/?lang=en&view=1)
- [DreamZero · World Action Models are Zero-shot Policies (2026)](https://dreamzero0.github.io/)

## 05. Hierarchical Robot Control

建议 2 分钟（含读图、视频及停顿）。

> 读图提示：三张都是上一场 talk 的原图。先看左边 Hi Robot，再看右侧 Helix 和 Helix 02；原图可以点击放大。

Hi Robot 的分工很直观。High-level VLM 理解任务、图像和用户的临时指令，输出一个 subtask language command；low-level π0 再把这个指令、图像和 robot state 变成 action。论文明确描述的是 two-level inference，不需要把原图中没有单列的第三个网络补进去。

Helix 用另一种接口连接高低层：System 2 输出 semantic latent，System 1 负责 visuomotor action。原 Helix 的 S2 是 7B 模型，约 7–9 Hz；S1 是 80M，200 Hz。

到了 Helix 02，三层分工更加明确：S2 给语义表示，S1 给 full-body joint targets，S0 进行 whole-body tracking 和 actuator control。官网说明 S1 是 200 Hz，S0 内部是 1 kHz；不要把原图接口上的 200 Hz 都解释成 S0 的执行频率。

可以把它概括为 reasoning、visuomotor policy、low-level control 的分工。但这是常见方案，不是一个已经证明任何模型都必须遵守的定律。接下来先抽象出这类设计把 generalization 放在哪里，再看 Astra 的实验怎样改变这一预期。Figure 的两篇官方发布文展示了层次分工和演示效果，但没有公布带重复试验分母的系统成功率表；61 actions 或 1 kHz 都不能替代成功率。

### 参考来源

- [Hi Robot · original hierarchical architecture (Feb 2025)](https://www.pi.website/research/hirobot)
- [Figure Helix · original S2/S1 architecture (Feb 2025)](https://www.figure.ai/news/helix)
- [Figure Helix 02 · original S2/S1/S0 architecture (Jan 2026)](https://www.figure.ai/news/helix-02)

## 06. Where Does Generalization Live?

建议 2 分钟（含读图、视频及停顿）。

> 读图提示：深绿色表示被寄托广泛泛化能力的一侧。先读上方原先的设计设想，再沿红色箭头读到下方的新能力模式；箭头只表示部分职责迁移。

先把接口符号说明白：o是observation，l是subtask language。上方System 2传l，System 1用π(a | o, l)生成交给Controller的目标a。下方System 2传更具体的c = (k, g)，k选择primitive，g给出目标或参数；System 1写成π(a | o, c)，再输出a给Controller。这里的π是统一的功能表达，可以包含确定性的IK或控制程序，不表示所有primitive都必须是随机神经网络。两条链的a都是控制目标，不特指torque。

我们原先有一个很自然的设想：System 2主要理解目标、分解任务，交出semantic information或subtask language。真正把观测和语言变成动作的工作，交给System 1，也就是VLA、WAM或其他learned visuomotor policy。

我们希望它是一个steerable generalist policy。写成公式就是π(a | o, l)：o是当前observation，l是language instruction，a是希望执行的action。理想上，换一个场景、对象、指令，甚至新的任务组合，它都能生成符合意图的行为。但“任意(o,l)都得到正确a”在这里是设计目标，不是某个已有模型的能力保证。WAM还可能联合生成世界演化，图中只抽出其action职责。

因此，过去我们把很多泛化与动作智能的希望寄托在System 1：不仅会动，还要把语义落到空间、选择运动方式，并应对新的任务。System 2则可以相对只负责高层语义。

现在观察到的变化是，更强的foundation model开始自己做其中一部分工作：根据observation理解空间关系、选择动作、生成EEF目标或joint参数，再根据反馈继续调整。图中这些职责从上方System 1移向下方System 2。不是整层搬走，而是原来需要专门visuomotor policy承担的一部分决策，现在可以由Agent承担。

机器人经验进入foundation-model训练，是理解这种变化的一条重要研究假设。不过，Astra的具体robot-data配方与因果对照尚未披露。我们能直接讨论的是能力变化，以及它怎样改变系统分工；不能把训练数据原因当作已经证明的结论。

这样一来，在部分任务上，System 2加比较窄的action primitives就可能做得很好，未必需要一个独立、覆盖所有任务的generalist VLA。Primitive可以是受约束的EEF运动、joint chunk、局部控制程序，也可以是learned motor skill。这里把它们放在System 1，是本talk对执行职能的简称，不代表IK或OSC本身都是learned System 1网络。底层servo和tracking仍由System 0中的Controller负责。

这也不是说VLA失去价值。Narrow primitives仍然需要足够的动作能力，精细接触、高频反馈和跨动力学条件的泛化也没有因此自动解决。我们真正要检验的是：随着System 2变强，System 1还必须有多通用、多聪明？

下面直接看Astra。先看没有独立VLA的实机控制，再看同一模型的不同action interfaces，最后用Direct/Hybrid报告检验什么时候仍需要learned motor prior。关键不是提前选边，而是让任务和实验决定分工。

### 参考来源

- [Hi Robot v2 §6 · model-level separation is not fundamental](https://arxiv.org/html/2502.19417v2#S6)
- [Robocurve · GPT-6 Astra direct EEF evaluation (Sep 2026)](https://openai.robocurve.org/gpt-6-astra/)
- [Astra control dashboard · prompt-v3, same-model interface records; unequal budgets](https://asimfish.github.io/astra-control-dashboard/#sec3)
- [Technical report · GPT 6 Astra as an Embodied Policy (result images captured 15 Sep 2026)](https://anonymous-report-421.github.io/public-website/?lang=en&view=1)

## 07. Astra: Stronger Real-Robot Performance

建议 2 分钟（含读图、视频及停顿）。

> 播放提示：两段为 Robocurve 的精选实机片段，已省略模型等待。先看 bowl，再看 precision insertion 的边界，视频不替代完整实验统计。

这一页先看能力变化：Astra在真实机器人上完成任务的表现，相比此前模型有了明显提升。Robocurve的bowl任务中，完成数从Fable 5的1/20、Fable 5.1的8/20，提高到Astra的19/20。重点是模型能把任务真正做成，而不是先讨论它采用哪种action interface。

Bowl 任务完成了 19/20，说明有些真实操作已经可以通过这条路径做得很好。但同一报告里的 round puzzle insertion 只有 2/20，所以不能由一个成功片段推论精细接触已经全面解决。

下表保留了同一个报告的全部 task × model 完成数。Bowl 中，Fable 5 和 Fable 5.1 分别是 1/20 与 8/20；Astra 是 19/20。Puzzle 中则是 0/20、2/20、2/20。提升主要出现在这组 bowl 任务，不能概括为所有精细接触均有提高。

协议也要看：每次最多 20 个 model calls，速度上限为 25%。Insertion 用同一个 rig；bowl 的 Astra 和 Fable 使用不同 rigs，Astra 还晚两天测试，人工评分知道模型身份。它不是完全隔离模型因素的随机对照。

这正是职责迁移的具体例子。Bowl里不需要独立VLA来决定每段动作，Astra自己根据视觉和proprio生成EEF目标，下面保留IK与controller。这说明一些任务的空间与动作决策可以上移，但puzzle的低成功率也提醒我们：更窄的执行接口并没有解决所有接触问题。下一页继续看这种路径的定性表现，稍后再单独核对latency。

关于原因，公开资料没有披露足够的 Astra 机器人预训练配方或因果消融。因此我会说“能力前提变了，旧分工需要重测”，不会把“加入海量机器人数据导致这一提升”说成已证事实。

### 参考来源

- [Robocurve · GPT-6 Astra direct EEF evaluation (Sep 2026)](https://openai.robocurve.org/gpt-6-astra/)

## 08. Astra: More Real-Robot Demos

建议 1 分钟（含读图、视频及停顿）。

> 播放提示：依次用视频自身的 controls 播放，不需要两段同时跑。左边源视频 12×，右边 20×；都不是 LLM 实时延迟展示。

这一页补充两个Astra操作真实机器人的demo：插头操作和键盘输入，展示更丰富的任务形式。左边 GPT-Policy-Eval 给模型一次视频示范，再利用在线视觉反馈进行插头操作。它展示了不依赖独立 VLA 的具体行为路径，但作者明确这是 selected trials，没有完整试验分母。

右边是真实机器人操作键盘的片段。它根据屏幕与机器人反馈处理输入、退格并继续尝试。这里能看到的是反馈下的行为调整，不能仅凭动作变化断言它进行了 RL、更新了模型权重，或者已经保存了跨任务的稳定技能。

接口备注需要保守：截至2026年9月15日，GPT-Policy-Eval的公开仓库只提供README和媒体，没有action schema或控制实现；keyboard作者原帖也没有说明接口。因此不能仅从Franka外观或末端运动判断使用了IK goal，图中标注Control interface: not disclosed。没有公开接口细节，不等于没有底层controller。

这两段比单纯说“能力更强了”具体得多：输入可以是示范或语义目标，输出已经落到真实动作。但接口仍然影响结果。下一页就固定为同一个 Astra，看不同 action 输出的公开比较。

### 参考来源

- [GPT-Policy-Eval · selected visual-context robot trials (Sep 2026)](https://github.com/cheng-haha/GPT-Policy-Eval)
- [Kaifeng Zhang (@kaiwynd) · Astra keyboard feedback demo, 20×](https://x.com/kaiwynd/status/2098823484474348008)
- [Awesome-Astra-Embodied-AI · curated discovery list, not an evaluation](https://github.com/zjwzcx/Awesome-Astra-Embodied-AI)

## 09. Same Astra, Different Action Outputs

建议 2 分钟（含读图、视频及停顿）。

> 读图提示：先读三种输出，再看两段 Square ep00 replay 和 20 回合统计。数字下方的 budget 是解释的一部分。

这组作者公开实验使用同一 GPT-6 Astra、medium reasoning，在 Franka / robosuite 的 Square 任务上比较 ΔEEF chunks、absolute EEF waypoints，以及返回 waypoints 的 Python 程序。

结果分别是 1/20、18/20 和 16/20。ΔEEF 是 7D OSC_POSE action，不是 joint q。Code 生成的是 plan(scene)，返回至多 12 个 waypoints，再由同一个 waypoint controller 跟踪，不是任意高频闭环程序。

最重要的限制是预算没有配平。ΔEEF 最多 200 control steps / 10 queries；Square waypoint 最多 500 steps / 16 queries；code 最多 500 steps / 3 轮程序修改。Waypoint 平均用了 256.6 steps，已经超过 ΔEEF 的上限。因此不能把差距全部归因于表达方式，也不能单凭这一行断言哪种primitive最通用。

这些是相同 proprio 档位，但该档位还包含 EEF 像素标记、相机尺度和固定地标，不是单纯只有关节状态。公开逐回合记录与表格数字一致，我们没有重跑实验。

另两个任务也提醒我们不要找统一赢家：Lift 三者都是 20/20；Can 则是 18/20、17/20、7/20。暂不讨论 latency，不等于忽略控制步数与反馈预算。下一页把完整三任务与不同 observation settings 放在一起，避免只挑 Square 这一行。

### 参考来源

- [Astra control dashboard · prompt-v3, same-model interface records; unequal budgets](https://asimfish.github.io/astra-control-dashboard/#sec3)

## 10. Astra Interfaces: Three Tasks

建议 1.5 分钟（含读图、视频及停顿）。

> 读表提示：先比较中间三个 proprio 列，再看没有 proprio 和 privileged observation 两列；不要逐格念数字。

Lift 几乎所有方式都达到20/20，无法区分接口。Can 中，ΔEEF和waypoint分别是18/20和17/20，code只有7/20。Square却相反：ΔEEF只有1/20，waypoint为18/20，code为16/20。因此没有跨任务通吃的接口赢家。

Observation 也影响解释。Square waypoint 没有 proprio 时是0/20，加入该档信息后是18/20；code换到privileged信息后是19/20。这里的 proprio 还含图像标记和固定参考，不能把差异都算成 action 表达的作用。

Script upper 与 random lower 只是这个实验的控制项。所有格子都是20 episodes，但控制步数与查询预算不同，特别是 Square 的waypoint平均256.6 steps已超过ΔEEF上限。当前结果说明 interface、observations 和预算都值得研究，不构成某种表达的纯因果优势。

### 参考来源

- [Astra control dashboard · prompt-v3, same-model interface records; unequal budgets](https://asimfish.github.io/astra-control-dashboard/#sec3)

## 11. Astra: Direct or Hybrid?

建议 2.5 分钟（含读图、视频及停顿）。

> 读图提示：先放大左侧报告原架构，讲完后再看右侧两段不同仿真任务的视频。片段省略 LLM 等待，只展示 control-time playback，不能用来比较端到端 latency。13/50 与 24/50 来自完整 RoboDojo 面板，不是这两个视频的对比。

这份匿名报告把问题推得更具体：当System 2已经能自己作动作决策时，再保留一个learned action prior还有什么价值？这里是系统执行架构，不是 Astra 未公开的内部网络结构。

共享输入包括三个 RGB views、14D proprioception、task instruction，以及 Astra 的 history / notes。Direct 由 Astra 生成双臂 EEF position、orientation 和 gripper targets，每次执行 1–5 control steps 后重新观察。

Hybrid 先由 task-finetuned π0.5 产生 50×14 joint-space candidate。Astra 结合观测和 FK trajectory 审核，选择接受前缀 1–15 steps，或者给 1–5 steps 的 EEF correction。这是 OR 分支，不是每一次都先执行 policy 再附加 correction。图中的 joint q 来自 π0.5，不能拿它当 Astra-q versus Astra-EEF 的消融。

EEF 仍通过 local IK 和 controller 执行。25 Hz 是 native control rate，不是 LLM 的决策频率。RoboDojo 选定的 10 tasks × 5 paired cases 中，Direct 13/50，Hybrid 24/50。

这组结果说明新能力并不自动让 learned prior 失去价值。但 prior、action interface 和 executed segment length 一起变化，不能归因为单一因素。接下来先看 RoboDojo 与 RoboLab 的两组整体结果，再用 RoboDojo 逐任务热力图检查差异；两组实验不能混池。

### 参考来源

- [Technical report · GPT 6 Astra as an Embodied Policy (result images captured 15 Sep 2026)](https://anonymous-report-421.github.io/public-website/?lang=en&view=1)

## 12. RoboDojo: Overall Results

建议 2 分钟（含读图、视频及停顿）。

> 读图提示：两张都是报告原始结果图，左边Score，右边success rate；可以点击放大。两图沿用同一Score排序，不要按右图行次误读为success-rate排名。

先只看三条彩色柱。Hybrid是24/50，success rate 48%；Direct是13/50，也就是26%。对应的mean Score是62.60与37.81。橙色π0.5是公开参考，不是用我们的五组种子重新跑出来的baseline。

灰色柱同样来自公开RoboDojo统计，作者重算了这十个选定任务以及standard/randomized场景的权重，因此不能拿它当整个benchmark的最新排行榜，也不能声称这些模型与Astra做了同种子配对比较。

Direct有两个episode缺少可用native Score，所以37.81基于48个scored episodes，Hybrid基于50个；两组success rate的分母都保持50。Learned prior、action interface和执行段长一起变化，结果支持整体Hybrid配置的价值，不能把提升归因于单个组件。

下一页换到RoboLab，排序会反过来。我们要看任务与prior的适配，而不是从一个汇总图宣布一种架构普遍最好。

### 参考来源

- [Technical report · GPT 6 Astra as an Embodied Policy (result images captured 15 Sep 2026)](https://anonymous-report-421.github.io/public-website/?lang=en&view=1)

## 13. RoboLab: Overall Results

建议 2 分钟（含读图、视频及停顿）。

> 读图提示：这是报告原始整体结果图。先说明selected final slots的口径，再看Direct与Hybrid的位置；可点击放大。

Direct最终49/50，Hybrid46/50；π0.5与Cosmos3-Nano-Policy各18/50，DreamZero为17/50。报告认为，选定的semantic pick-and-place任务，以及student prior未针对这些任务适配，可能解释与RoboDojo不同的排序。这是解释假设，不是隔离因素后的因果结论。

特别要保留选择规则：Astra组使用retained final slots，包含历史结果和authorized retries，initial states没有严格配对。Direct最后两次BlocksInBin retry把decision budget从180提高到500。三个baseline来自June cohort，每任务按顺序取前五次，包括失败。

所以这些数字是已发布记录的描述性汇总，不是fresh、统一预算、每条件只跑一次的配对试验。相同task名称和slot数量也不能证明task version、control settings或起点一致。不要和RoboDojo合成一个总成功率。

随后回到RoboDojo的逐任务热力图，检查整体均值背后的任务差异。

### 参考来源

- [Technical report · GPT 6 Astra as an Embodied Policy (result images captured 15 Sep 2026)](https://anonymous-report-421.github.io/public-website/?lang=en&view=1)

## 14. RoboDojo: Task-Level Patterns

建议 1.5 分钟（含读图、视频及停顿）。

> 读图提示：先看右侧Hybrid与Direct两列，再横向比较对应任务。颜色越深Score越高；这是partial-completion Score，不是success rate。可点击放大原图。

总体数会掩盖分工差异。Classify objects中Direct的Score是100，Hybrid是71；但Fold clothes中Hybrid是100，Direct是40，Build tower则是64与12。Hybrid不是逐任务都赢，Direct也不是所有操作都能替代动作先验。

把这张图连回开头的问题：更强System 2确实可以承担更多语义、空间和动作决策，但System 1需要多强、多通用，仍然取决于任务和prior是否适配。热力图提供任务层面的线索，不是“语义”和“物理”两种能力被严格分离的测量。

前五列是公开参考值，后两列是报告的实验。它们不是同种子重跑；Direct缺失Score的分母限制仍然适用。图中保留原报告全部十个任务、Overall和七种方法，没有重新挑选最有利的任务。

最后核对视频容易掩盖的另一个问题：这些系统具体输出什么，模型多久才返回一次？

### 参考来源

- [Technical report · GPT 6 Astra as an Embodied Policy (result images captured 15 Sep 2026)](https://anonymous-report-421.github.io/public-website/?lang=en&view=1)

## 15. Astra Interfaces and Query Time

建议 1.5 分钟（含读图、视频及停顿）。

> 读图提示：左边看模型真正输出什么，右边看公开的单次查询耗时。数字是特定设置的观测，不是所有Astra系统的统一速度。

接口没有统一到一种形式。Robocurve与匿名报告的Direct是EEF pose targets，经local IK与controller执行。Asim则比较7D ΔEEF、absolute waypoints，以及返回waypoints的代码；底层OSC_POSE是20 Hz。匿名Hybrid则先由π0.5给出joint-space candidate，Astra决定accept prefix或EEF correction。这是已有policy参与执行，不是Astra直接输出那些joint targets。另有G1 demo明确经过official SONIC planner与SONIC policy；但许多社媒案例只公开了视频，不能统一称为atomic skills，也无法确认其底层API。

也确实有直接关节输出。GPT Dog Eval让Astra生成Go1四条腿全部12个关节的归一化position residual keyframes，最多4个keyframes、15个control steps。实际目标是q_nominal + 0.5a rad，经interpolation、guardrails和PD执行。这不是humanoid的全身角度，也不是裸motor torque。最关键的是：推理时simulator暂停。50 Hz是动作执行频率，报告的simulation-time feedback Hz也不是wall-clock推理速度。

右侧来自Asim prompt-v3、medium reasoning、proprio设置下Lift、Can、Square各20个episodes，共180回合的逐query日志。ΔEEF有414次查询，平均30.75秒；waypoint有241次，平均26.08秒；code有76次，平均41.98秒。按显示秒数计算，不是我们独立计时。三种查询的内容与执行预算不同，不能据此给接口排统一的速度冠军。

均值的倒数约0.024–0.038 queries/s，只是这些记录的sequential query-time倒数，不是完整闭环的decision rate；执行、渲染和工具调用还有额外开销。即使机器人端以20或25 Hz运行，也不代表Astra每秒推理20或25次。加速demo更不能用于推算频率。

目前能回答的是：公开实例从joint chunks、EEF、code到learned-policy delegation都存在；明确披露的部分运行需要数十秒一次query，其他来源没有可比的端到端频率。下面用这条真实控制链路，总结能力与缺口。

### 参考来源

- [Astra control dashboard · prompt-v3, same-model interface records; unequal budgets](https://asimfish.github.io/astra-control-dashboard/#sec3)
- [GPT Dog Eval · bounded Go1 joint-chunk loop, source pinned 15 Sep 2026](https://github.com/guajun/gpt-dog-eval/tree/04ef36d8120545341f6f1e77a464327c801e03aa)
- [Robocurve · GPT-6 Astra direct EEF evaluation (Sep 2026)](https://openai.robocurve.org/gpt-6-astra/)
- [Technical report · GPT 6 Astra as an Embodied Policy (result images captured 15 Sep 2026)](https://anonymous-report-421.github.io/public-website/?lang=en&view=1)
- [Flood G1 demo · official SONIC planner/policy; overlay rate is not LLM timing](https://x.com/RotekSong/status/2099104628562608371)

## 16. Control: Strengths and Open Gaps

建议 1 分钟（含读图、视频及停顿）。

> 读图提示：先看左边已经展示的能力，再看右边尚不可靠或尚未证实的能力。这不是三种独立神经模块，也不是把任务机械地分成 System 2 / 1 / 0。

回到第6页的职责迁移图。我们不再预设System 2只传语义，也不要求所有泛化都由一个generalist VLA / WAM承担。部分空间与动作决策可以由更强Agent完成，下面的action primitives则保留必要的motor competence。Agent 已经能理解语义目标、识别任务对象并利用视觉反馈；在已测试的设置中，也展示了目标重定位和一定的 spatial generalization。左边说的是有条件的能力，不是任意新机器人、新相机和新环境都能成功。

右边有两种不同的缺口。High-frequency control 是实时闭环问题：目前看到的系统仍依赖 local controller、interpolation、短动作片段或已有 policy。模拟器在 LLM 思考时暂停，并不能证明机器人在真实扰动下也来得及纠正。Physical generalization 则问接触、摩擦、质量、柔顺性或动力学变化后是否仍可靠。现有报告没有建立全面的跨物理条件泛化结论。

Robocurve 的 bowl 是19/20，puzzle只有2/20，说明成功的语义任务不能代替精细接触验证。但单次失败也不能唯一定位为物理理解不足，sensing、pose、controller和budget都可能参与。Asim在同一个Astra上更换观测和action interface，也出现明显差异，但预算并不匹配，不能据此分离单一原因。

因此不能把新模式概括为“System 1不需要智能”。更准确的表述是：语义理解与有限空间泛化已经展示，高频反馈控制和可靠物理泛化仍是短板。不是断言模型永远做不到，也不是说当前模型完全不懂物理。选择 Direct、Hybrid 还是 Tools，需要一起考察 model、interface 和 feedback budget。

Hi Robot 的 Discussion 本身就说模型层面的角色分离 is not fundamental。我们不是宣布旧实验失效，而是在模型能力变化后重新检验旧结论。Astra 的机器人预训练配方及因果对照仍未披露，不能由成功 demo 反推训练原因。

接下来从“怎样生成下一步 action”，转向“Agent 可以帮助生成哪些 Data”。

### 参考来源

- [Hi Robot v2 §6 · model-level separation is not fundamental](https://arxiv.org/html/2502.19417v2#S6)
- [Astra control dashboard · prompt-v3, same-model interface records; unequal budgets](https://asimfish.github.io/astra-control-dashboard/#sec3)
- [Technical report · GPT 6 Astra as an Embodied Policy (result images captured 15 Sep 2026)](https://anonymous-report-421.github.io/public-website/?lang=en&view=1)
- [Robocurve · GPT-6 Astra direct EEF evaluation (Sep 2026)](https://openai.robocurve.org/gpt-6-astra/)
- [Axel Peytavin · mobile ICL demo; author-reported spatial transfer, no trial denominator](https://x.com/ax_pey/status/2098216469012283681)

## 17. Agent Creates Data

建议 1 分钟（含读图、视频及停顿）。

> 读图提示：从输入与 Agent 出发，沿三条分支看产物，最后汇到验证要求。这是 Data 工作的分类，不是所有案例都完成了整条链。

第二章统一称为 Data。输入可以是真实视频、扫描结果或设计目标。Agent 调用或编写工程工具，产物可能是 assets / scenes、Real-to-sim Replay，也可能是 Data Rollout。机械手设计属于第一类，放在这一章就更自然。

三者需要区分。Assets 是几何、关节结构和场景；replay 尝试重现已有行为；rollout 则实际执行 controller 或 policy，记录 states、actions和contacts。生成过这些文件，不代表它们已经构成高质量训练数据。

下面仍只细讲 Agentic Real2Sim：有了真实交互记录，能不能自动得到可运行的 simulation episode？它的输入含同步视角、calibration和robot trajectory，不是只给一段任意RGB视频。之后再看社区把这条工作链扩展到哪些产物。

### 参考来源

- [Awesome-Astra-Embodied-AI · curated discovery list, not an evaluation](https://github.com/zjwzcx/Awesome-Astra-Embodied-AI)
- [Agentic Real2Sim, arXiv:2607.19190v3 (24 Jul 2026)](https://arxiv.org/html/2607.19190v3)
- [DexGPT · recorded contact rollout; physical acceptance not met](https://github.com/Hu-xiao-max/dexgpt/tree/03ba8a26eaef9dfd272ac1a22c0fd06ccb9b2e5b)

## 18. Real Episode and Its Twin

建议 1.5 分钟（含读图、视频及停顿）。

> 播放提示：可同时播放两段。它们来自同一个 recorded episode，但这里不是逐帧同步的数值误差评测。

左边是真实记录，右边是重建后的模拟回放。这里不只是找一个长得像的 mesh：robot、camera、object pose、geometry 和 motion trajectory 必须在一致的坐标系里，simulator 才能真正运行。

这类工作有大量接口和中间产物。某个物体的位置误差，可能来自 camera calibration，也可能来自 tracking；geometry 不对，后面的参数调整又可能只是在补偿它。

所以 Agent 的潜在价值不是替代每一个几何算法，而是组织工具、检查输出，并把失败送回需要修正的位置。下一页具体看它做了哪些决定。

### 参考来源

- [Agentic Real2Sim, arXiv:2607.19190v3 (24 Jul 2026)](https://arxiv.org/html/2607.19190v3)

## 19. Agentic Real2Sim: Method

建议 3 分钟（含读图、视频及停顿）。

> 读图提示：沿论文原图走，重点追踪每一步交出的 artifact，而不是念工具名单。

Visual processing 首先选择对象和 keyframe，再进行 segmentation、geometry recovery、depth 和 pose tracking。Agent 可以拒绝不合适的 mask、重新选帧，也可以根据 tracking critic 的反馈更换初始化帧。

这里要区分决策与计算。SAM3、SAM3D、FoundationStereo 和 FoundationPose 等组件完成专门工作；Agent 组织这些调用并作受约束的选择，不是在语言模型内部直接算出所有 mesh 和 depth。

这些结果写成结构化 episode artifacts：object meshes、scale、pose tracks、robot trajectory、camera metadata 和 task semantics。Scene preparation 再校准 robot base 与 ground，把它们装进 MuJoCo。

后续存在两类修正路径：deterministic sweep 根据 contact / grasp outcomes 搜索 candidate，或者 LLM-assisted loop 读取 rendered keyframes 和 structured summaries 再提出 refinement。不能把每一次候选变化都描绘成 LLM 自由调参。

这项工作的主要贡献是把长链条组织成可执行、可排查的 episode conversion workflow。我们现在可以问一个明确问题：随机抽取一批真实记录，这套流程究竟完成多少？

### 参考来源

- [Agentic Real2Sim, arXiv:2607.19190v3 (24 Jul 2026)](https://arxiv.org/html/2607.19190v3)

## 20. DROID-100: Protocol and Results

建议 1.5 分钟（含读图、视频及停顿）。

> 读图提示：先看原图左侧 accepted / partial / failure，再说明判定规则。成本图只解释统计范围，不逐个念 backend 排名。

全部一百个 DROID episodes 都保留在分母里。最好的 backend Gemma 4 31B 得到 48 accepted、8 partial 和 44 failure；还没生成有效 replay 就停止的运行，也不会被排除。

这里 accepted 的定义需要说清楚。Evaluator 先筛选符合 grasp probe、视频存在以及 motion statistics 等条件的候选，最多选五个交给三个 VLM judges。Judges 比较 real 与 sim 的关键帧，关注对象身份、最终位置、动作相似性和最终 gripper 位置。

每个 judge 选自己的最佳 candidate。只要任意一个 judge 的最佳分数达到 8/10，就算通过；这不是 majority vote，也不要求三个 judge 都认可。

因此 48/100 的含义是：在这套规则下，有多少 episode 找到了 accepted replay。它不是物理参数估计准确率。右侧 model-call bill 也不是包含 perception、simulation 和 preparation 的全部成本。

下一页把四种 backend 的所有结果列出，看看只换模型之后，完成情况和 model bill 怎样变化。

### 参考来源

- [Agentic Real2Sim, arXiv:2607.19190v3 (24 Jul 2026)](https://arxiv.org/html/2607.19190v3)

## 21. Real2Sim: All Backend Results

建议 2 分钟（含读图、视频及停顿）。

> 读表提示：每行的前三个计数都加起来等于100；最后一列是整组100 episodes的model-call bill。

Gemma是48 accepted、8 partial、44 failed，Qwen是45、11、44，Haiku是37、12、51，GPT-5.4是43、12、45。Partial指最佳有效评分为7；6及以下或没有合法记录都计入failure。

在这套固定pipeline中，更高model bill没有带来更多observed accepted replays。GPT-5.4的82.30美元与Gemma的2.62美元，也只涵盖model calls，不能据此声称完成整个重建只需这些钱，或者速度快了多少。

这提示瓶颈可能在几何、跟踪、候选和验证的组合中，不只是推理模型强弱。但我们没有独立critic ablation，也没有统计等效性检验。Accepted replay仍不能代替新action的预测测试。下面再看社区如何把Agent的职责扩展到搭建workflow本身。

### 参考来源

- [Agentic Real2Sim, arXiv:2607.19190v3 (24 Jul 2026)](https://arxiv.org/html/2607.19190v3)

## 22. Data: Replay and Scene Assets

建议 1 分钟（含读图、视频及停顿）。

> 播放提示：先看左侧 real/sim 对照，再单独播放 Office 场景。Office 片段是重建产物运行，不是完整开发过程的录屏。

左边 Lingxiao 的案例输入是 multi-view RGB 加 robot actions。作者报告 Astra 连接了 camera calibration、asset construction、physics system-ID、MuJoCo 和 Blender。视频展示的是相应回放，不是独立验证的新动作预测。

右边 Office 的作者描述了另一条链：从 office scan 的参考画面重建 Blender scene，导出 USD，再放进 Newton 让 G1 运行。我们看到的是最后的场景产物。原帖没有明确说明 G1 locomotion policy 是否新训练，所以不能把场景搭建直接讲成 Astra 学会了走路。

这两段让我们可以提出一个新的问题：Agent 的职责是否在从执行预先编排的 pipeline，扩展到编写、连接和修补 pipeline 本身？这是作者展示带来的研究问题，不是同条件对照已经量化的结论。

作者对 microphone 示例还明确标注 kinematic replay，而非 validated dynamics。外观像与接触过程正确是两种要求。接下来再看手部设计：它属于 Data 的资产生成层，而不是已经验证的物理训练轨迹。

### 参考来源

- [@Lingxiao234, X Real2Sim and failure thread (8 Sep 2026)](https://x.com/Lingxiao234/status/2096992059731443923)
- [Jiarui Xu (@Jiarui_X) · office reference to Newton/G1 scene; author-reported workflow](https://x.com/Jiarui_X/status/2098439950991806804)
- [Awesome-Astra-Embodied-AI · curated discovery list, not an evaluation](https://github.com/zjwzcx/Awesome-Astra-Embodied-AI)

## 23. Data: Mechanism and CAD Assets

建议 1 分钟（含读图、视频及停顿）。

> 播放提示：这是 CAD / mechanism asset 的可视化，不是物理机械手测试。

Tendon-hand 设计也属于 Data 的资产层。作者用 build123d生成190个STEP文件，再用JavaScript制作animation，导出GLB进行展示。这个案例的产物是可供后续工程迭代的设计资产，不是控制数据集，也不是已验证的physical rollout。

作者明确说“Would this model work irl? Def not.”。所以不能把动画当作 tendon transmission、负载、接触或可靠性验证。还需要检查 actuator requirement、routing、friction、tolerance和装配，再制作prototype。

把它纳入Data，是把Agent帮助构建的资产也纳入视野，不是降低训练数据的质量标准。下一页用一个真正记录了physics rollout、但验证未通过的例子，说明这道边界。

### 参考来源

- [@earthtojake, X hand design and limitation thread (10 Sep 2026)](https://x.com/earthtojake/status/2097789988670709821)
- [Author limitation and follow-up](https://x.com/earthtojake/status/2097789991426335015)
- [Author limitation and follow-up](https://x.com/earthtojake/status/2097801101890207893)

## 24. Data: Physics and Training Value

建议 1 分钟（含读图、视频及停顿）。

> 读图提示：这张 DexGPT 原图从左到右是 source human demonstration、imposed-hinge kinematic reconstruction、passive-hinge contact physics。用它区分外观回放与接触物理验证。

用它收束 Data，是因为“真的跑过 physics”与“physics 验证通过”也不同。DexGPT 的公开代码调用 MuJoCo 的 mj_step，rollout 文件记录 qpos、qvel、ctrl和contact信息，所以不只是动画文件。

但作者报告的 physical criteria 是 NOT met，task_success 是 false；maximum penetration为5.623 mm，高于小于5 mm的要求。这203个 logged states来自一条轨迹，不是203次试验。图像逼真或确实执行了 simulator，都不能直接改写这个验证结论。

因此本章的结论是：Agent 已能帮助生成 geometry、mechanism、scene、replay和记录下来的rollout。它们是候选 Data。Replay 是否匹配、对新 action 的 physics 是否正确、用于训练是否真的带来收益，必须分别验证。

例如一段从左边慢推的回放很像，换成从右边快推却可能失败；geometry、contact和friction误差可能在同一条轨迹上互相补偿。最终要声称 Data 有用，还需要 held-out downstream training 或 planning test。

改进策略并不只能依靠模拟。下一章 ENPIRE 直接在真实机器人上组织实验，不要求先跑完 Agentic Real2Sim。

### 参考来源

- [Agentic Real2Sim, arXiv:2607.19190v3 (24 Jul 2026)](https://arxiv.org/html/2607.19190v3)
- [DexGPT · recorded contact rollout; physical acceptance not met](https://github.com/Hu-xiao-max/dexgpt/tree/03ba8a26eaef9dfd272ac1a22c0fd06ccb9b2e5b)

## 25. Agent Improves Policy

建议 1 分钟（含读图、视频及停顿）。

> 读图提示：从固定 Task + API 出发，沿 Agent → rollout → verifier / logs → Agent 走一圈。强调更新对象是后续 trial 的 policy。

第三章的问题是：一次实验的反馈，怎样成为下次仍能使用的能力？这不同于 Control 里临时修正下一条 action。Agent 现在可以修改 policy code、training recipe，或训练 neural policy，让之后的 trial 使用新的版本。

ENPIRE 把这个过程放在真实机器人上。Environment 的 action、安全、reset 和 verification 接口先在人的反馈下建立，进入 improvement 阶段后固定下来。

这可以放在 robot self-improvement 的方向下讨论，但具体要看留下什么：是 policy weights、代码，还是 context？存在一个循环，并不自动意味着改进者自身获得了递归增强能力。下面先看实验环境怎样搭建。

### 参考来源

- [ENPIRE, arXiv:2606.19980v1 (Jun 2026)](https://arxiv.org/html/2606.19980v1)

## 26. ENPIRE: Environment and Improvement

建议 2 分钟（含读图、视频及停顿）。

> 读图提示：沿原图区分 human-assisted environment setup 与 autonomous improvement；不要把两阶段压成无人参与的一步。

第一阶段建立环境接口。系统在 human feedback 下实现 safety constraints、automatic reset 和 success verification。完成以后，这些能力通过固定的 Gym APIs 给下一阶段使用。

第二阶段，coding Agent 获得训练代码的修改权限。它可以读资料、提出 hypothesis、修改 BC 或 RL 程序，再调用真实 rollout，查看 trajectory、video 和 reward，判断下一步值得改什么。

这里固定环境与成功标准非常重要：策略做不好，不能通过修改 verifier 让自己看起来成功。否则分数的变化就没有稳定含义。

多个 agent–robot pairs 还可以异步试验不同想法，并通过代码协作保留有效修改。它是否真的更快、是否更省，要留给实验回答。先把支持反复试验的 reset 和 verification 看具体。

### 参考来源

- [ENPIRE, arXiv:2606.19980v1 (Jun 2026)](https://arxiv.org/html/2606.19980v1)

## 27. ENPIRE: Reset and Verification

建议 1.5 分钟（含读图、视频及停顿）。

> 播放提示：依次播放 pin reset 和 zip-tie verification，两段来自不同任务，不是同一个 rollout 的同步镜头。

Automatic reset 让一次机器人实验变成可重复过程。如果每次失败都需要人恢复现场，Agent 的自主实验就在这里停住。

Pin reset 展示怎样准备下一次 trial。ENPIRE 的部分任务从最困难的 subphase 开始，这是把研究聚焦到关键操作，但不能改述成任意初始状态下的完整任务能力。Reset 的状态分布也影响实验是否可比。

Zip-tie 例子展示如何检查结果。论文讨论结合多个 camera view 降低视觉 verifier 的 false positives，其他任务还可结合 proprioception 或 torque 信号。

所以 safety、reset 和 verification 是不同职责：安全不等于做对，能够 reset 也不证明 success test 可靠。把这些条件建立好后，我们终于可以看 Agent 实际改了哪些东西。

### 参考来源

- [ENPIRE, arXiv:2606.19980v1 (Jun 2026)](https://arxiv.org/html/2606.19980v1)

## 28. ENPIRE: What Did the Agent Change?

建议 2.5 分钟（含读图、视频及停顿）。

> 读图提示：放大 Figure 12。先读 idea tree 的实心与空心节点，再跟随虚线读下面的 best-score curve；不要逐个念所有节点。

这张原图比抽象地说“改代码、跑实验”更具体。上面每个节点是一项探索过的 idea，新的分支代表不同方向。实心绿色节点提高了 team-average best success rate，空心节点则评估过但没有收益。

例如 I37 是 BC regularization，论文在这次 run 上标注 +10.8 percentage points。后面的 I66 调整 batch size，从 1024 到 512，标注 +0.9 pp；I76 的 controller compensation 标注 +1.3 pp。

这里的重点不是记住三个数，而是看见修改对象：Agent 可以改变学习目标和训练程序，也可以改变执行补偿，而不是只负责启动训练。没有收益的分支同样是这段探索过程的一部分。

这不是三项独立随机消融，不能把这些增量当成在所有条件下都能复现的平均因果效果。下图也不是每个当前 policy 的性能，而是随 research wall-clock 推进的 team-average best score。接下来用正式 learning curve 和 scaling 实验看总体表现。

### 参考来源

- [ENPIRE, arXiv:2606.19980v1 (Jun 2026)](https://arxiv.org/html/2606.19980v1)

## 29. ENPIRE: Pin Insertion Curve

建议 2 分钟（含读图、视频及停顿）。

> 读图提示：先看随 research time 变化的性能，再看不同 fleet size；横轴不是 action inference latency。

这组结果回答两个问题：真实反馈能否支持 policy improvement，以及更多并行实验能否更早找到高性能策略。

Pin insertion 中，从一个 agent–robot pair 扩到八个，达到接近完美 success rate 的 research time，从超过一个半小时缩短到大约四十分钟。这里研究的是发现好策略需要多久，不是机器人执行一次动作有多快。

Success rate 的口径也必须保留。每个 rollout 允许最多八次 conditional retries，后续尝试可以利用前面失败的信息。因此它包含 precision 和 recovery，不是 one-shot insertion precision，也不是相互独立的 best-of-eight；不能套独立 Bernoulli 假设反推单次成功率。

在这个固定环境和 protocol 内，实验支持策略随研究推进改善，也支持并行资源带来更短 time-to-target。更快是否更省，最后再看资源图。在那之前，先补两页正式结果：两个真实任务的模型对照，以及 RoboCasa 中 tools、VLA 与 autoresearch 的对照。

### 参考来源

- [ENPIRE, arXiv:2606.19980v1 (Jun 2026)](https://arxiv.org/html/2606.19980v1)

## 30. ENPIRE: Two Physical Tasks

建议 2.5 分钟（含读图、视频及停顿）。

> 读图提示：左侧保留完整Figure 3和原曲线，右侧列官网实际绘图数据的终点均值。两列不是同一种分数。

Physical Push-T研究heuristic policy discovery，在8小时位置，Codex、Claude、Kimi的normalized score分别为0.938、0.750、0.625。Pin insertion研究gradient-based policy improvement，在4小时位置，success rate分别为95.5%、97.5%、79.0%。不能把Push-T的0.938改称93.8% binary success。

论文对应配置是Codex/GPT-5.5 xhigh、Claude Code/Opus4.7 High和Kimi Code/Kimi K2.6 thinking。这些不是Astra模型对比。不同任务的排序也不同，不应据此宣布统一的coding agent冠军。

官网每个configuration提供四条plotted traces及means，但没有充分披露独立seed数量或专门held-out test set的大小。我们没有把四条线叫四次独立复现。Physical rollout仍允许最多八次conditional retries，因此也不是pass@1 precision。

这些结果回答在固定实机环境中能否改进策略。下一页换到RoboCasa，观察autoresearch如何改善工具和VLA的组合，注意评测协议也会改变。

### 参考来源

- [ENPIRE, arXiv:2606.19980v1 (Jun 2026)](https://arxiv.org/html/2606.19980v1)
- [ENPIRE official interactive plots · model and resource data (accessed 14 Sep 2026)](https://research.nvidia.com/labs/gear/enpire/)

## 31. ENPIRE: Autoresearch in RoboCasa

建议 1.5 分钟（含读图、视频及停顿）。

> 读图提示：上方保留原Figure 6，包括task示例和三个aggregate bars。原图未给精确数字标签，不从柱高补造百分比。

三个对照分别是GR00T N1.5端到端VLA、CaP-X*的zero-shot agentic tool use，以及加入反复开发反馈的ENPIRE。原图中ENPIRE的aggregate最高。它说明改进对象也可以是工具调用和执行程序，不一定只能训练新权重。

例如Agent找到的策略会先用detection与motion planning移动到目标上方，再进入grasp，必要时组合VLA。关键是先根据实验反馈改程序，再检验留下来的程序。

Appendix描述的reported evaluations每项使用40个预先固定的seed/layout/style组合，同一task的方法共享这些设置。每episode运行一次generated script，禁止oracle、reset和重复retry API。不要把上一页实机最多八次conditional retries搬到这张仿真表上。

图里八张task图片是示例，不等于已披露八行数表，也不能据此乘出320 pooled trials。我们能陈述的结果是原图的相对表现，aggregate pooling的细节和精确百分比没有充分公布。

### 参考来源

- [ENPIRE, arXiv:2606.19980v1 (Jun 2026)](https://arxiv.org/html/2606.19980v1)

## 32. Astra: Training and Context

建议 1 分钟（含读图、视频及停顿）。

> 播放提示：左边四足完整 14 秒，点击原生 fullscreen 可以读九宫格状态；不要裁掉 FULL EVAL NOT MET。右边是 8× 的 physical ICL 展示，两者分别播放。

左边作者报告 Astra 参与 Fusion360 / STL 设计、simulation 和 RL 迭代。视频是九种行为的开发预览，不是九种行为全部通过验证：原片明确保留 FULL EVAL NOT MET，Wave 和 Sit 还只展示 partial first cycles，并标注四个 separate experts。实机部署仍属于后续计划。

它展示的方向是 Agent 开始覆盖设计、环境、训练和修错的一整段工程工作。开发过程来自作者描述，视频本身是训练产物预览，不是完整过程记录。

右边是 Astra 的 physical in-context learning。人给出示范，Agent 利用 context，通过已有 motion-planning tools 产生行为。作者报告 first-pass success，但没有完整试验分母；也没有由此证明模型权重更新或技能已持久化。

把它们放在一起，是为了区分 training、code revision 和 in-context adaptation。它们都可能让行为变化，但不是同一种 post-training。ENPIRE 的正式结果仍按原论文的 policy-improvement protocol 理解，不借社区 demo 增加它的成功率。

### 参考来源

- [Akira Sasaki (@gclue_akira) · quadruped CAD/RL development preview; partial evaluation gates](https://x.com/gclue_akira/status/2098300921658868185)
- [Wenli Xiao (@_wenlixiao), X · human video to robot arm with GPT-6 Astra (9 Sep 2026)](https://x.com/_wenlixiao/status/2097801944119349455)
- [Awesome-Astra-Embodied-AI · curated discovery list, not an evaluation](https://github.com/zjwzcx/Awesome-Astra-Embodied-AI)

## 33. ENPIRE: Cost and Chapter Summary

建议 2.5 分钟（含读图、视频及停顿）。

> 读图提示：不逐项介绍所有指标，重点看 time-to-success 与 token-to-success 为什么可能朝相反方向变化。

更多 agent–robot pairs 可以更早找到好策略，但可能消耗更多 tokens；每台机器人的 utilization 也未必随规模单调提高。Research wall-clock、policy latency、token consumption 和 robot utilization 不是同一个“效率”。

下表来自官网 Figure 7 的精确绘图数据，保留 mean 和 std。1、4、8 对 agent–robot 的 per-robot utilization 分别约为 49.1%、30.9%、29.8%，GPU active-time fraction 为 29.4%、32.5%、49.0%；整队 token rate 是每分钟 9.3k、40.0k、140.3k。后者不是每个 Agent 的消耗，GPU 指标也不是直接读取 nvidia-smi 的 occupancy。

这些 std 的具体统计层次没有充分披露，不叫 confidence interval。Figure 7 自己的 time-to-success 是 4.5/3.2/2.0 小时，与前面 pin 曲线的约40分钟不是同一组数；不能把两个图的 token 数和时间拼成一个实验。

如果最稀缺的是研究周期，增加资源可能值得；如果预算更紧，最合适的配置就不一样。图中的实测曲线与 linear projection 也要区分，不能都当成实际运行结果。

本章可以收束为：在可重复、可验证的真实实验接口内，Agent 能把 feedback 转成后续 policy 或 training code 的改进；扩大并行度还可以缩短研究周期。Human-assisted setup、conditional retries、verifier 的可靠性与成本，都是这项结果成立的条件。

这是一种具体的 robot self-improvement 实践，不等于已证明开放世界的 recursive self-improvement。最后把三个角色的产物与验证要求放回同一张图。

### 参考来源

- [ENPIRE, arXiv:2606.19980v1 (Jun 2026)](https://arxiv.org/html/2606.19980v1)
- [ENPIRE official interactive plots · model and resource data (accessed 14 Sep 2026)](https://research.nvidia.com/labs/gear/enpire/)

## 34. Takeaways

建议 1 分钟（含读图、视频及停顿）。

> 读图提示：从 Agent 分别沿三条支路看 Role、Artifact 和 Evidence。三章是不同工作位置，不是一条已打通的端到端流水线。

最后只留三个对应关系。Control 产出 Action，要看执行是否可靠。Data 产出候选 assets 和 rollouts，要分别验证 physics 与 downstream training value。Improvement 产出下一版 Policy 或程序，要看 held-out gain 和总成本。

更强模型让这些分工值得重测，但新 demo 不能替代相应的验证。我们真正要问的是：在自己的机器人工作中，哪些信息、判断和执行责任，现在可以重新分配给 Agent？

### 参考来源

- [Technical report · GPT 6 Astra as an Embodied Policy (result images captured 15 Sep 2026)](https://anonymous-report-421.github.io/public-website/?lang=en&view=1)
- [Agentic Real2Sim, arXiv:2607.19190v3 (24 Jul 2026)](https://arxiv.org/html/2607.19190v3)
- [ENPIRE, arXiv:2606.19980v1 (Jun 2026)](https://arxiv.org/html/2606.19980v1)
- [Awesome-Astra-Embodied-AI · curated discovery list, not an evaluation](https://github.com/zjwzcx/Awesome-Astra-Embodied-AI)

## 35. Thank You

建议 0.5 分钟（含读图、视频及停顿）。

谢谢大家。欢迎讨论，也欢迎结合你们自己的机器人系统，说说最想让 Agent 接手哪一部分，以及需要什么实验才能放心交给它。

