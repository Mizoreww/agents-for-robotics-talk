# Agents for Robotics — 中文讲稿

讲者：Zimo Huang · 2026-09-16 · 本地修订 0.18（2026-09-16）

英文 slides，中文讲解，专有名词保留英文。建议 59 分钟包含原图读图、视频、停顿和讨论，尚未彩排计时。每章先看总框图。Control 看能力与接口证据；Data 只看 Awesome-Astra 收录的社区 demos；Improvement 细讲 ENPIRE。


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
| 09 | Robot Puzzle Demos in Simulation | 1 | 11:00 |
| 10 | One Model, Different Control Interfaces | 2 | 12:00 |
| 11 | Astra Interfaces: Three Tasks | 1.5 | 14:00 |
| 12 | Astra: Introducing a Hybrid Architecture | 2.5 | 15:30 |
| 13 | RoboDojo: Overall Results | 2 | 18:00 |
| 14 | RoboLab: Overall Results | 2 | 20:00 |
| 15 | RoboDojo: Task-Level Patterns | 1.5 | 22:00 |
| 16 | High Latency Limits Real-Time Control | 1.5 | 23:30 |
| 17 | Control: Strengths and Open Gaps | 1 | 25:00 |
| 18 | Agent Creates Data | 1 | 26:00 |
| 19 | Astra: Scene Reconstruction | 2 | 27:00 |
| 20 | Astra: Hand Assets | 2 | 29:00 |
| 21 | Astra: Replay and Data Rollout | 2 | 31:00 |
| 22 | Data: From Demos to Useful Data | 1 | 33:00 |
| 23 | Agent Improves Policy | 1 | 34:00 |
| 24 | ENPIRE: Environment and Improvement | 2 | 35:00 |
| 25 | ENPIRE: Reset and Verification | 2 | 37:00 |
| 26 | ENPIRE: Two Ways to Improve Policy | 2 | 39:00 |
| 27 | ENPIRE: What Did the Agent Change? | 2.5 | 41:00 |
| 28 | ENPIRE: Two Physical Tasks | 2.5 | 43:30 |
| 29 | ENPIRE: Parallel Physical Research | 2 | 46:00 |
| 30 | ENPIRE: Autoresearch in RoboCasa | 1.5 | 48:00 |
| 31 | ENPIRE: Learned Manipulation Demos | 2 | 49:30 |
| 32 | ENPIRE: Experience Across Tasks | 2 | 51:30 |
| 33 | ENPIRE: Cost of Physical Research | 2.5 | 53:30 |
| 34 | Toward Recursive Self-Improvement | 1.5 | 56:00 |
| 35 | Takeaways | 1 | 57:30 |
| 36 | Thank You | 0.5 | 58:30 |

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

Control 围绕一个问题展开：机器人泛化能力应该主要由哪一层承担？先看把希望寄托于 generalist VLA / WAM 的分工，再用Astra 的实机、接口与 Direct/Hybrid 证据，检查哪些空间理解和动作决策可以上移到 Agent。Data 只看 Awesome-Astra 收录的六个 demo，依次区分场景、设计资产、回放和 rollout。Improvement 以 ENPIRE 为代表。Tendon-hand 设计就是 Data 资产层的一个例子。

这三个角色可以联系起来，但不是已经验证的流水线。例如 ENPIRE 直接使用真实机器人，不要求先完成 Data 章节里的重建与回放。


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

这两段比单纯说“能力更强了”具体得多：输入可以是示范或语义目标，输出已经落到真实动作。但接口仍然影响结果。下一页先看两个 simulation puzzle，再回到同一 Astra 的不同 action interface 比较。

### 参考来源

- [GPT-Policy-Eval · selected visual-context robot trials (Sep 2026)](https://github.com/cheng-haha/GPT-Policy-Eval)
- [Kaifeng Zhang (@kaiwynd) · Astra keyboard feedback demo, 20×](https://x.com/kaiwynd/status/2098823484474348008)
- [Awesome-Astra-Embodied-AI · curated discovery list, not an evaluation](https://github.com/zjwzcx/Awesome-Astra-Embodied-AI)

## 09. Robot Puzzle Demos in Simulation

建议 1 分钟（含读图、视频及停顿）。

> 播放提示：左边是作者发布的完整 Rubik’s Cube 视频，未额外加速；右边是作者网站导出视频中的完整 Claw 段。两边分别播放，先看动作，再区分验证条件。

前一页是真机 demo，这一页补两个更复杂的 simulation puzzle。左边 Yanjie Ze 展示 Astra 用 robot hands 操作 Rubik’s Cube。Awesome-Astra 将它描述为 zero-shot manipulation，但本次可核验的原帖只明确写了解魔方，没有公开完整 trial denominator 和 action API。这里不把 zero-shot 当成经过独立验证的评测结论，也不猜测它是直接 joint q、IK goal 或 atomic skill。

右边 Unlocking the Claw 展示双臂如何绕开相互锁住的几何约束，把两部分分离、放到支架、松手和撤离。它从已有 object-space reference path 出发，实现局部路径修正、grasp 选择、full-robot IK 和 motion planning。起始时物体已经抓住，使用 ideal rigid grasps，记录的是 kinematic joint motion。

所以这两个例子展示了很强的空间任务表现，但不是相同证据。尤其 Claw 验证的是特定路径的几何可行性，不是接触动力学、frictional force closure，也不是能从任意新初态在线解题的 policy。下面继续看同一个基础模型使用不同 action interface，表现会怎样改变。

### 参考来源

- [Yanjie Ze · GPT6 Astra Rubik’s Cube robot-hand simulation demo · 10 Sep 2026](https://x.com/ZeYanjie/status/2098118164626501669)
- [Unlocking the Claw · methods, reference path attribution and kinematic limits](https://qinengwang-aiden.github.io/demos/constraint_demos/methods.html)

## 10. One Model, Different Control Interfaces

建议 2 分钟（含读图、视频及停顿）。

> 读图提示：先读三种输出，再看三段 Square ep00 replay 和 20 回合统计。数字下方的 budget 是解释的一部分。

这组作者公开实验使用同一 GPT-6 Astra、medium reasoning，在 Franka / robosuite 的 Square 任务上比较 ΔEEF chunks、absolute EEF waypoints，以及返回 waypoints 的 Python 程序。

结果分别是 1/20、18/20 和 16/20。ΔEEF 是 7D OSC_POSE action，不是 joint q。Code 生成的是 plan(scene)，返回至多 12 个 waypoints，再由同一个 waypoint controller 跟踪，不是任意高频闭环程序。第三列现在是该code/proprio组真实的Square ep00：作者记录为成功，125 steps、1 query。视频只有6.4秒，但query本身花了41.339秒，整个episode为42.42秒；播放省略了模型等待，不能当作实时控制。

最重要的限制是预算没有配平。ΔEEF 最多 200 control steps / 10 queries；Square waypoint 最多 500 steps / 16 queries；code 最多 500 steps / 3 轮程序修改。Waypoint 平均用了 256.6 steps，已经超过 ΔEEF 的上限。因此不能把差距全部归因于表达方式，也不能单凭这一行断言哪种primitive最通用。

这些是相同 proprio 档位，但该档位还包含 EEF 像素标记、相机尺度和固定地标，不是单纯只有关节状态。公开逐回合记录与表格数字一致，我们没有重跑实验。

另两个任务也提醒我们不要找统一赢家：Lift 三者都是 20/20；Can 则是 18/20、17/20、7/20。暂不讨论 latency，不等于忽略控制步数与反馈预算。下一页把完整三任务与不同 observation settings 放在一起，避免只挑 Square 这一行。

### 参考来源

- [Astra control dashboard · prompt-v3, same-model interface records; unequal budgets](https://asimfish.github.io/astra-control-dashboard/#sec3)

## 11. Astra Interfaces: Three Tasks

建议 1.5 分钟（含读图、视频及停顿）。

> 读表提示：先比较中间三个 proprio 列，再看没有 proprio 和 privileged observation 两列；不要逐格念数字。

Waypoint proprio整列加粗是为了突出这条接口路线，不表示它在每个任务都最好。Square中，排除privileged观测后，它的18/20最高；但Can中ΔEEF为18/20，高于waypoint的17/20。Lift几乎所有方式都达到20/20，无法区分接口。Can 中，ΔEEF和waypoint分别是18/20和17/20，code只有7/20。Square却相反：ΔEEF只有1/20，waypoint为18/20，code为16/20。因此没有跨任务通吃的接口赢家。

Observation 也影响解释。Square waypoint 没有 proprio 时是0/20，加入该档信息后是18/20；code换到privileged信息后是19/20。这里的 proprio 还含图像标记和固定参考，不能把差异都算成 action 表达的作用。

Script upper 与 random lower 只是这个实验的控制项。所有格子都是20 episodes，但控制步数与查询预算不同，特别是 Square 的waypoint平均256.6 steps已超过ΔEEF上限。当前结果说明 interface、observations 和预算都值得研究，不构成某种表达的纯因果优势。

### 参考来源

- [Astra control dashboard · prompt-v3, same-model interface records; unequal budgets](https://asimfish.github.io/astra-control-dashboard/#sec3)

## 12. Astra: Introducing a Hybrid Architecture

建议 2.5 分钟（含读图、视频及停顿）。

> 读图提示：先放大左侧报告原架构，讲完后再看右侧两段不同仿真任务的视频。片段省略 LLM 等待，只展示 control-time playback，不能用来比较端到端 latency。13/50 与 24/50 来自完整 RoboDojo 面板，不是这两个视频的对比。

接下来引入另一种Hybrid架构：把learned action prior与Astra的判断、修正结合起来。这份报告把问题推得更具体：当System 2已经能自己作动作决策时，再保留一个learned action prior还有什么价值？这里是系统执行架构，不是 Astra 未公开的内部网络结构。

共享输入包括三个 RGB views、14D proprioception、task instruction，以及 Astra 的 history / notes。Direct 由 Astra 生成双臂 EEF position、orientation 和 gripper targets，每次执行 1–5 control steps 后重新观察。

Hybrid 先由 task-finetuned π0.5 产生 50×14 joint-space candidate。Astra 结合观测和 FK trajectory 审核，选择接受前缀 1–15 steps，或者给 1–5 steps 的 EEF correction。这是 OR 分支，不是每一次都先执行 policy 再附加 correction。图中的 joint q 来自 π0.5，不能拿它当 Astra-q versus Astra-EEF 的消融。

EEF 仍通过 local IK 和 controller 执行。25 Hz 是 native control rate，不是 LLM 的决策频率。RoboDojo 选定的 10 tasks × 5 paired cases 中，Direct 13/50，Hybrid 24/50。

这组结果说明新能力并不自动让 learned prior 失去价值。但 prior、action interface 和 executed segment length 一起变化，不能归因为单一因素。接下来先看 RoboDojo 与 RoboLab 的两组整体结果，再用 RoboDojo 逐任务热力图检查差异；两组实验不能混池。

### 参考来源

- [Technical report · GPT 6 Astra as an Embodied Policy (result images captured 15 Sep 2026)](https://anonymous-report-421.github.io/public-website/?lang=en&view=1)

## 13. RoboDojo: Overall Results

建议 2 分钟（含读图、视频及停顿）。

> 读图提示：两张都是报告原始结果图，左边Score，右边success rate；可以点击放大。两图沿用同一Score排序，不要按右图行次误读为success-rate排名。

先只看三条彩色柱。Hybrid是24/50，success rate 48%；Direct是13/50，也就是26%。对应的mean Score是62.60与37.81。橙色π0.5是公开参考，不是用我们的五组种子重新跑出来的baseline。

灰色柱同样来自公开RoboDojo统计，作者重算了这十个选定任务以及standard/randomized场景的权重，因此不能拿它当整个benchmark的最新排行榜，也不能声称这些模型与Astra做了同种子配对比较。

Direct有两个episode缺少可用native Score，所以37.81基于48个scored episodes，Hybrid基于50个；两组success rate的分母都保持50。Learned prior、action interface和执行段长一起变化，结果支持整体Hybrid配置的价值，不能把提升归因于单个组件。

下一页换到RoboLab，排序会反过来。我们要看任务与prior的适配，而不是从一个汇总图宣布一种架构普遍最好。

### 参考来源

- [Technical report · GPT 6 Astra as an Embodied Policy (result images captured 15 Sep 2026)](https://anonymous-report-421.github.io/public-website/?lang=en&view=1)

## 14. RoboLab: Overall Results

建议 2 分钟（含读图、视频及停顿）。

> 读图提示：这是报告原始整体结果图。先说明selected final slots的口径，再看Direct与Hybrid的位置；可点击放大。

Direct最终49/50，Hybrid46/50；π0.5与Cosmos3-Nano-Policy各18/50，DreamZero为17/50。报告认为，选定的semantic pick-and-place任务，以及student prior未针对这些任务适配，可能解释与RoboDojo不同的排序。这是解释假设，不是隔离因素后的因果结论。

特别要保留选择规则：Astra组使用retained final slots，包含历史结果和authorized retries，initial states没有严格配对。Direct最后两次BlocksInBin retry把decision budget从180提高到500。三个baseline来自June cohort，每任务按顺序取前五次，包括失败。

所以这些数字是已发布记录的描述性汇总，不是fresh、统一预算、每条件只跑一次的配对试验。相同task名称和slot数量也不能证明task version、control settings或起点一致。不要和RoboDojo合成一个总成功率。

随后回到RoboDojo的逐任务热力图，检查整体均值背后的任务差异。

### 参考来源

- [Technical report · GPT 6 Astra as an Embodied Policy (result images captured 15 Sep 2026)](https://anonymous-report-421.github.io/public-website/?lang=en&view=1)

## 15. RoboDojo: Task-Level Patterns

建议 1.5 分钟（含读图、视频及停顿）。

> 读图提示：先看右侧Hybrid与Direct两列，再横向比较对应任务。颜色越深Score越高；这是partial-completion Score，不是success rate。可点击放大原图。

总体数会掩盖分工差异。Classify objects中Direct的Score是100，Hybrid是71；但Fold clothes中Hybrid是100，Direct是40，Build tower则是64与12。Hybrid不是逐任务都赢，Direct也不是所有操作都能替代动作先验。

把这张图连回开头的问题：更强System 2确实可以承担更多语义、空间和动作决策，但System 1需要多强、多通用，仍然取决于任务和prior是否适配。热力图提供任务层面的线索，不是“语义”和“物理”两种能力被严格分离的测量。

前五列是公开参考值，后两列是报告的实验。它们不是同种子重跑；Direct缺失Score的分母限制仍然适用。图中保留原报告全部十个任务、Overall和七种方法，没有重新挑选最有利的任务。

最后核对视频容易掩盖的另一个问题：这些系统具体输出什么，模型多久才返回一次？

### 参考来源

- [Technical report · GPT 6 Astra as an Embodied Policy (result images captured 15 Sep 2026)](https://anonymous-report-421.github.io/public-website/?lang=en&view=1)

## 16. High Latency Limits Real-Time Control

建议 1.5 分钟（含读图、视频及停顿）。

> 读图提示：这一页只看latency。三张卡是同一个公开harness的平均model-query time，不是所有Astra部署的统一速度。

前面的simulation replay省略了模型等待；真实系统不可能把环境也一同暂停。这正是目前很严重的问题：模型作一次决策要等待数十秒，碰到扰动和持续接触时，很难及时根据新反馈调整。

数字来自Asim prompt-v3、medium reasoning、proprio设置下Lift、Can、Square各20个episodes，共180回合、731次查询的公开日志。ΔEEF有414次查询，平均30.75秒；waypoint有241次，平均26.08秒；code有76次，平均41.98秒。这是根据已发布日志汇总，不是我们重新计时。

三种query完成的工作量不同，不能把数值顺序直接当作接口速度排行榜。Query time也不是完整闭环latency，执行、工具调用和渲染还可能增加时间；机器人端的Controller Hz不等于Agent inference Hz。这里的结论不是给所有模型设一个速度上限，而是当前这组系统的数十秒级等待已经明显限制快速反馈。

因此，下一页的第一个open problem是如何降低foundation model的latency，让更强的决策能力真正进入及时的交互闭环，而不只是在省略等待的视频中完成任务。

### 参考来源

- [Astra control dashboard · prompt-v3, same-model interface records; unequal budgets](https://asimfish.github.io/astra-control-dashboard/#sec3)

## 17. Control: Strengths and Open Gaps

建议 1 分钟（含读图、视频及停顿）。

> 读图提示：先看左边已经展示的能力，再看右边尚不可靠或尚未证实的能力。这不是三种独立神经模块，也不是把任务机械地分成 System 2 / 1 / 0。

回到第6页的职责迁移图。我们不再预设System 2只传语义，也不要求所有泛化都由一个generalist VLA / WAM承担。部分空间与动作决策可以由更强Agent完成，下面的action primitives则保留必要的motor competence。Agent 已经能理解语义目标、识别任务对象并利用视觉反馈；在已测试的设置中，也展示了目标重定位和一定的 spatial generalization。左边说的是有条件的能力，不是任意新机器人、新相机和新环境都能成功。

右边有两种不同的缺口。High-frequency control 是实时闭环问题：目前看到的系统仍依赖 local controller、interpolation、短动作片段或已有 policy。模拟器在 LLM 思考时暂停，并不能证明机器人在真实扰动下也来得及纠正。Physical generalization 则问接触、摩擦、质量、柔顺性或动力学变化后是否仍可靠。现有报告没有建立全面的跨物理条件泛化结论。

Robocurve 的 bowl 是19/20，puzzle只有2/20，说明成功的语义任务不能代替精细接触验证。但单次失败也不能唯一定位为物理理解不足，sensing、pose、controller和budget都可能参与。Asim在同一个Astra上更换观测和action interface，也出现明显差异，但预算并不匹配，不能据此分离单一原因。

因此不能把新模式概括为“System 1不需要智能”。更准确的表述是：语义理解与有限空间泛化已经展示，高频反馈控制和可靠物理泛化仍是短板。不是断言模型永远做不到，也不是说当前模型完全不懂物理。

Hi Robot 的 Discussion 本身就说模型层面的角色分离 is not fundamental。我们不是宣布旧实验失效，而是在模型能力变化后重新检验旧结论。Astra 的机器人预训练配方及因果对照仍未披露，不能由成功 demo 反推训练原因。

从这四项能力和缺口，箭头收束到两个当前open problems。第一，如何降低foundation model的latency，让系统能更及时地利用反馈。第二，如何为Agent设计更好的interface和action primitives，让动作段之间衔接更流畅，让contact-rich任务中的执行更稳定。这不仅是让模型选对目标，也涉及执行器提供什么抽象、如何保持连续性，以及怎样处理接触变化。它们是待研究问题，不是这组demo已经解决的结论。

接下来从“怎样生成下一步 action”，转向“Agent 可以帮助生成哪些 Data”。

### 参考来源

- [Hi Robot v2 §6 · model-level separation is not fundamental](https://arxiv.org/html/2502.19417v2#S6)
- [Astra control dashboard · prompt-v3, same-model interface records; unequal budgets](https://asimfish.github.io/astra-control-dashboard/#sec3)
- [Technical report · GPT 6 Astra as an Embodied Policy (result images captured 15 Sep 2026)](https://anonymous-report-421.github.io/public-website/?lang=en&view=1)
- [Robocurve · GPT-6 Astra direct EEF evaluation (Sep 2026)](https://openai.robocurve.org/gpt-6-astra/)
- [Axel Peytavin · mobile ICL demo; author-reported spatial transfer, no trial denominator](https://x.com/ax_pey/status/2098216469012283681)

## 18. Agent Creates Data

建议 1 分钟（含读图、视频及停顿）。

> 读图提示：三条分支是产物分类，不代表每个 demo 都完成了整条链。

第二章只看 Awesome-Astra 收录的六个 demo，合成三组：先看 Office 与 kitchen 的场景重建，再看两个 hand assets，最后对比 Real-to-sim Replay 和 Data Rollout。

Agent 把工程工具组织起来，交出可检查的场景、模型和轨迹。顺着这三组看，我们要区分“生成了产物”和“产物已经适合训练”。

### 参考来源

- [Awesome-Astra-Embodied-AI · curated discovery list, not an evaluation](https://github.com/zjwzcx/Awesome-Astra-Embodied-AI)
- [DexGPT · recorded contact rollout; physical acceptance not met](https://github.com/Hu-xiao-max/dexgpt/tree/03ba8a26eaef9dfd272ac1a22c0fd06ccb9b2e5b)

## 19. Astra: Scene Reconstruction

建议 2 分钟（含读图、视频及停顿）。

> 播放与读图提示：先看左边 Office，再看右边 kitchen。右侧为作者 X 原帖的完整20.9秒展示。20秒指输入 footage，不是重建耗时。

这两个案例都把现实空间重建为可编辑的3D场景资产。左边 Jiarui Xu 从 office scan 出发，经 Astra 辅助构建 Blender scene，导出 USD，再接入 Newton。G1 出现在场景中，不代表 Astra 在这里训练了 locomotion policy，原帖没有披露这部分。

右边 Frank ZY Dou 用约20秒 monocular RGB 视频重建实验室厨房，进一步加入可以移动的 cabinets 和 articulated objects。作者在 LinkedIn 说明，这个过程约用一天，包含过夜等待和 human-in-the-loop；20秒不是建模耗时。公开 kitchen-twin 的链路是 ViPE metric scan、instance segmentation 与 measurement，再让 Astra 编写 Blender assets，并由 independent verifier 检查。Agent 主要是在组织工具、构造可编辑资产，不是自己完成所有几何估计。

这里从“复原外观”推进到了“表达哪些部分能动”。作者描述产物可输出 MJCF / URDF with joints，但仍在 adding simulation，thin / shiny objects 也有不足。因此这是一组可交互的候选资产，不是已经验证的 simulation dynamics 或 training data。公开仓库提供输出和 metadata，不是完整 pipeline。

### 参考来源

- [Jiarui Xu (@Jiarui_X) · office reference to Newton/G1 scene; author-reported workflow](https://x.com/Jiarui_X/status/2098439950991806804)
- [Zhiyang (Frank) Dou · original kitchen viewer demo, 12 Sep 2026 local time](https://x.com/frankzydou/status/2098460193319186578)
- [Zhiyang (Frank) Dou · workflow, human-in-the-loop and simulation status](https://lnkd.in/p/e8YszUkv)
- [Frank ZY Dou · public kitchen-twin output and workflow description](https://github.com/frank-zy-dou/kitchen-twin/tree/d34e0f8983bcb6ce040130d023cac9623d0efce7)
- [Awesome-Astra-Embodied-AI · curated discovery list, not an evaluation](https://github.com/zjwzcx/Awesome-Astra-Embodied-AI)

## 20. Astra: Hand Assets

建议 2 分钟（含读图、视频及停顿）。

> 播放提示：先播放左侧 Jake，再播放右侧 Dmytro；两段都可以单独全屏。

这页是两个不同的 hand asset。Jake 偏向设计文件：用 build123d 生成190个STEP文件，再用 JavaScript 做 animation，导出 GLB。Dmytro 则以1X演示视频为参考，在 MuJoCo 中重建 hand model 与运动；这里用的是9月10日原片，不是9月12日的后续版本。

两者共同说明 Agent 可以交出结构和运动的候选模型。但 Jake 明确说模型不能直接用于真实硬件；Dmytro 也说明 mechanics 是 simplified，cable deformation 是 illustrative。动画里的绳子在动，不等于 tendon transmission、friction 或 contact physics 已经验证。

从可编辑的资产，接下来进入随时间变化的行为和数据。

### 参考来源

- [@earthtojake, X hand design and limitation thread (10 Sep 2026)](https://x.com/earthtojake/status/2097789988670709821)
- [Dmytro Hrybov (@dimentary) · simplified rope-driven hand reconstruction (10 Sep 2026)](https://x.com/dimentary/status/2097857980150763900)
- [Awesome-Astra-Embodied-AI · curated discovery list, not an evaluation](https://github.com/zjwzcx/Awesome-Astra-Embodied-AI)
- [Author limitation and follow-up](https://x.com/earthtojake/status/2097789991426335015)
- [Author limitation and follow-up](https://x.com/earthtojake/status/2097801101890207893)

## 21. Astra: Replay and Data Rollout

建议 2 分钟（含读图、视频及停顿）。

> 播放提示：先看左侧 replay；再将右侧 DexGPT 单独全屏播放，原片20.3秒。其三栏是 source、imposed-hinge kinematic reference、passive-hinge contact physics，只有最后一栏检验接触驱动的物体运动。

Lingxiao 的输入是 multi-view RGB 加 robot actions。Astra 组织 camera calibration、asset construction、system-ID、MuJoCo 和 Blender，生成相应的 replay。它说明一段真实行为可以被重放，但没有独立的新 action 预测测试，不能把视觉相似直接当成 validated dynamics。

DexGPT 再往前走一步：把 monocular GIF 的手部运动 retarget 到两只22-DOF Sharpa Wave hands，用 MuJoCo 的 mj_step 运行，保存 qpos、qvel、controls、contacts 和 forces。所以右边不只是 animation，确实产生了 rollout data。

不过它的 physical validation not met：task_success=false，maximum penetration 为5.623 mm，超过小于5 mm的要求。203个 logged states 来自一条轨迹，不是203次试验，也没有报告 downstream training 收益。这里最值得强调的区别就是：有数据，与有物理可信、对训练有用的数据，不是同一件事。

### 参考来源

- [@Lingxiao234, X Real2Sim and failure thread (8 Sep 2026)](https://x.com/Lingxiao234/status/2096992059731443923)
- [DexGPT · recorded contact rollout; physical acceptance not met](https://github.com/Hu-xiao-max/dexgpt/tree/03ba8a26eaef9dfd272ac1a22c0fd06ccb9b2e5b)
- [Awesome-Astra-Embodied-AI · curated discovery list, not an evaluation](https://github.com/zjwzcx/Awesome-Astra-Embodied-AI)

## 22. Data: From Demos to Useful Data

建议 1 分钟（含读图、视频及停顿）。

> 读图提示：三种产物对应三类检查，最后汇到 training value。

六个案例可以收束成三类：Assets / scenes、Real-to-sim Replay、Data Rollout。Agent 已经能帮助产出更复杂的候选资产和轨迹，但每类都要有自己的检验：资产能否正确运行，replay 是否匹配记录，rollout 是否符合物理约束。

最后还有共同的一问：如何利用这些产物帮助 downstream training？下一步要探索如何把候选资产、replay 和 rollout 转化为可用的训练数据，并验证它们的实际价值。第三章换到另一个位置：Agent 直接组织实验，修改下一版 policy，再用反馈验证改进。

### 参考来源

- [Awesome-Astra-Embodied-AI · curated discovery list, not an evaluation](https://github.com/zjwzcx/Awesome-Astra-Embodied-AI)
- [DexGPT · recorded contact rollout; physical acceptance not met](https://github.com/Hu-xiao-max/dexgpt/tree/03ba8a26eaef9dfd272ac1a22c0fd06ccb9b2e5b)

## 23. Agent Improves Policy

建议 1 分钟（含读图、视频及停顿）。

> 读图提示：沿 Task + API、Agent、真实 rollout、Verifier + logs 走一圈。先问改进留下了什么。

第三章的问题是：一次实验的反馈，怎样成为下次仍能使用的能力？Control 关心这一步怎么动，这里关心下一版 policy 怎样变好。Agent 可以修改 policy code、training recipe，或训练 neural policy，让后续 trial 使用新的版本。

ENPIRE 的切入点是，软件实验可以自动重跑，机器人实验却常常需要人收拾现场、判断成功、调代码。只要这些环节还依赖人工，autonomous research 就无法真正持续。

因此它先建立可重复、可验证的环境，再让 Agent 提出假设、组织实验和保留有效修改。章末我们再把这件事接到 RSI，也就是本 talk 所说的 Recursive Self-Improvement：能否连“如何改进”的经验也留下来，让以后做研究更有效？

### 参考来源

- [ENPIRE, arXiv:2606.19980v1 (Jun 2026)](https://arxiv.org/html/2606.19980v1)

## 24. ENPIRE: Environment and Improvement

建议 2 分钟（含读图、视频及停顿）。

> 读图提示：沿原图区分 human-assisted environment setup 与 autonomous improvement；不要把两阶段压成无人参与的一步。

第一阶段建立环境接口。系统在 human feedback 下实现 safety constraints、automatic reset 和 success verification。完成以后，这些能力通过固定的 Gym APIs 给下一阶段使用。

第二阶段，coding Agent 获得训练代码的修改权限。它可以读资料、提出 hypothesis、修改 BC 或 RL 程序，再调用真实 rollout，查看 trajectory、video 和 reward，判断下一步值得改什么。

这里固定环境与成功标准非常重要：策略做不好，不能通过修改 verifier 让自己看起来成功。否则分数的变化就没有稳定含义。

多个 agent–robot pairs 还可以异步试验不同想法，并通过代码协作保留有效修改。它是否真的更快、是否更省，要留给实验回答。先把支持反复试验的 reset 和 verification 看具体。

### 参考来源

- [ENPIRE, arXiv:2606.19980v1 (Jun 2026)](https://arxiv.org/html/2606.19980v1)

## 25. ENPIRE: Reset and Verification

建议 2 分钟（含读图、视频及停顿）。

> 播放提示：左边为完整 pin reset，压缩到 8×；右边为完整 zip-tie detector 视频，1×。两段来自不同任务，不是同一 rollout 的同步画面。

Automatic reset 解决下一次试验从哪里开始。Agent 组合 SAM3 的物体检测、pose tracking、cuRobo motion planning 和 gripper torque 检查，把现场恢复到指定起点。部分任务直接从最难的 subphase 开始，不能解释成从任意初态解决完整任务。

Verification 解决结果到底有没有变好。右边展示 top/right 两个视角的检测框；完整判定还包括 segmentation 和几何测试，避免一个视角看起来穿过、实际上没有穿过的 false positive。Pin insertion 则结合视觉对齐、插入深度与力矩信号。

环境构造仍需要 human feedback，也需要成功和失败样例。之后进入 policy improvement，reset、verifier、安全约束和评测规则固定，不能为了得高分而修改成功定义。有了稳定的实验接口，才谈得上自动改进。

### 参考来源

- [ENPIRE, arXiv:2606.19980v1 (Jun 2026)](https://arxiv.org/html/2606.19980v1)
- [ENPIRE official interactive plots · model and resource data (accessed 16 Sep 2026)](https://research.nvidia.com/labs/gear/enpire/)

## 26. ENPIRE: Two Ways to Improve Policy

建议 2 分钟（含读图、视频及停顿）。

> 读图提示：两张官网原图分别对应 Push-T 和 Pin insertion。对比下方 f(o) 与 πθ(a | o)，不要把 coding Agent 和部署 policy 混成同一个模型。

ENPIRE 没有规定必须使用某一个 RL 算法。左边 Push-T 的改进对象可以直接是 heuristic code：根据 observation 算接触位置、推的方向和反馈修正，写成可执行函数 f。

右边 Pin insertion 则会训练 neural policy。Agent 可以选择 BC、iterative BC / data aggregation、offline RL、online RL，或带 BC regularization 的组合。它修改学习目标、数据混合和训练程序，再用实机结果判断这一版值不值得保留。

训练栈把 robot deployment、learner 和 actor 分开。Rollout buffer 保存 observation、action 来源和视频；online transitions 与 demonstrations 分开进入 buffer，再按训练配方混合。这里更新的 θ 是机器人 policy 的参数，不是 coding foundation model 的权重。

原论文的 robot policy 以 30 Hz 运行，底层 joint controller 为 100 Hz；这也不是 coding Agent 的推理频率。Agent 在更慢的研究循环中组织改进，训练出的 policy 在执行循环中产生动作。下面看它实际提出过什么修改。

### 参考来源

- [ENPIRE, arXiv:2606.19980v1 (Jun 2026)](https://arxiv.org/html/2606.19980v1)
- [ENPIRE official interactive plots · model and resource data (accessed 16 Sep 2026)](https://research.nvidia.com/labs/gear/enpire/)
- [ENPIRE public autoresearch contract · pinned source 99ee90a](https://github.com/NVlabs/ENPIRE/blob/99ee90acf65b5b18957c8382ad580db999528be3/enpire/policy/autoresearch_instruction.md)

## 27. ENPIRE: What Did the Agent Change?

建议 2.5 分钟（含读图、视频及停顿）。

> 读图提示：放大 Figure 12。先读 idea tree 的实心与空心节点，再跟随虚线读下面的 best-score curve；不要逐个念所有节点。

这张原图比抽象地说“改代码、跑实验”更具体。上面每个节点是一项探索过的 idea，新的分支代表不同方向。实心绿色节点提高了 team-average best success rate，空心节点则评估过但没有收益。

例如 I37 是 BC regularization，论文在这次 run 上标注 +10.8 percentage points。后面的 I66 调整 batch size，从 1024 到 512，标注 +0.9 pp；I76 的 controller compensation 标注 +1.3 pp。

这里的重点不是记住三个数，而是看见修改对象：Agent 可以改变学习目标和训练程序，也可以改变执行补偿，而不是只负责启动训练。没有收益的分支同样是这段探索过程的一部分。

这不是三项独立随机消融，不能把这些增量当成在所有条件下都能复现的平均因果效果。下图也不是每个当前 policy 的性能，而是随 research wall-clock 推进的 team-average best score。接下来用正式的模型对照和 fleet scaling 看总体表现。

### 参考来源

- [ENPIRE, arXiv:2606.19980v1 (Jun 2026)](https://arxiv.org/html/2606.19980v1)

## 28. ENPIRE: Two Physical Tasks

建议 2.5 分钟（含读图、视频及停顿）。

> 读图提示：左侧保留完整Figure 3和原曲线，右侧列官网实际绘图数据的终点均值。两列不是同一种分数。

Physical Push-T研究heuristic policy discovery，在8小时位置，Codex、Claude、Kimi的normalized score分别为0.938、0.750、0.625。Pin insertion研究gradient-based policy improvement，在4小时位置，success rate分别为95.5%、97.5%、79.0%。不能把Push-T的0.938改称93.8% binary success。

论文对应配置是Codex/GPT-5.5 xhigh、Claude Code/Opus4.7 High和Kimi Code/Kimi K2.6 thinking。这些不是Astra模型对比。不同任务的排序也不同，不应据此宣布统一的coding agent冠军。

官网每个configuration提供四条plotted traces及means，但没有充分披露独立seed数量或专门held-out test set的大小。我们没有把四条线叫四次独立复现。Physical rollout仍允许最多八次conditional retries，因此也不是pass@1 precision。

这些结果回答在固定实机环境中能否改进策略。下一页先看扩大并行实验，能否更早找到高性能策略。

### 参考来源

- [ENPIRE, arXiv:2606.19980v1 (Jun 2026)](https://arxiv.org/html/2606.19980v1)
- [ENPIRE official interactive plots · model and resource data (accessed 16 Sep 2026)](https://research.nvidia.com/labs/gear/enpire/)

## 29. ENPIRE: Parallel Physical Research

建议 2 分钟（含读图、视频及停顿）。

> 播放提示：左边是完整的官方 pin fleet 视频，8×。右边原曲线保留 axes 和 legend，可以点击放大。

每个 station 有自己的 robot、compute 和 coding Agent。不同 Agent 异步探索训练思路，通过 Git 分支共享代码、读取其他分支的结果，把有用的修改继续试下去。这不仅是把一个固定策略复制到八台机器上评估，而是并行寻找更好的策略。

Pin insertion 从一个 agent–robot pair 扩到八个，达到接近完美表现的 research time，从超过一个半小时缩短到大约四十分钟。横轴是研究时间，不是 action inference latency。

这里的物理 rollout 允许最多八次 conditional retries，后一次尝试能利用前面失败的信息。因此不是 one-shot precision，也不是相互独立的 best-of-eight，不能由此反推 pass@1。Fleet 视频展示并行执行的形态，不给视频里的动作自行统计新成功率。

这组证据支持更多资源缩短 time-to-target，但更快不等于更省。后面会回到成本，现在先看同一套 autoresearch 思路在 RoboCasa 中怎样使用。

### 参考来源

- [ENPIRE, arXiv:2606.19980v1 (Jun 2026)](https://arxiv.org/html/2606.19980v1)
- [ENPIRE official interactive plots · model and resource data (accessed 16 Sep 2026)](https://research.nvidia.com/labs/gear/enpire/)

## 30. ENPIRE: Autoresearch in RoboCasa

建议 1.5 分钟（含读图、视频及停顿）。

> 读图提示：上方保留原Figure 6，包括task示例和三个aggregate bars。原图未给精确数字标签，不从柱高补造百分比。

三个对照分别是GR00T N1.5端到端VLA、CaP-X*的zero-shot agentic tool use，以及加入反复开发反馈的ENPIRE。原图中ENPIRE的aggregate最高。它说明改进对象也可以是工具调用和执行程序，不一定只能训练新权重。

例如Agent找到的策略会先用detection与motion planning移动到目标上方，再进入grasp，必要时组合VLA。关键是先根据实验反馈改程序，再检验留下来的程序。

Appendix描述的reported evaluations每项使用40个预先固定的seed/layout/style组合，同一task的方法共享这些设置。每episode运行一次generated script，禁止oracle、reset和重复retry API。不要把上一页实机最多八次conditional retries搬到这张仿真表上。

图里八张task图片是示例，不等于已披露八行数表，也不能据此乘出320 pooled trials。我们能陈述的结果是原图的相对表现，aggregate pooling的细节和精确百分比没有充分公布。

### 参考来源

- [ENPIRE, arXiv:2606.19980v1 (Jun 2026)](https://arxiv.org/html/2606.19980v1)

## 31. ENPIRE: Learned Manipulation Demos

建议 2 分钟（含读图、视频及停顿）。

> 播放提示：依次看 Pin insertion、Tie zip-tie、Cut zip-tie，均为官网下载原文件完整内容，统一转为 8×。可单独全屏观察接触与恢复，不必三段同时解说。

这页只看 ENPIRE 自己的任务 demo，不再放 CAD + RL 开发预览或另一个 physical ICL 项目。关注点不只是最后有没有做成，也包括接触失败后如何继续尝试、调整，再走向完成。

官网把这些任务的结果描述为高 pass@8，其中 retry 不是八个互相独立的随机样本，而是同一长程 rollout 内利用失败信息恢复。这里没有把片段裁到只剩成功动作，也不从几个展示视频额外推算成功率。

这些是作者展示的已得到的行为。它们不能单独证明训练算法更强，也不自动证明跨物体、跨任务的泛化。更接近自进化的问题是：在一个任务里学会如何做实验，能不能帮助下一个任务？

### 参考来源

- [ENPIRE, arXiv:2606.19980v1 (Jun 2026)](https://arxiv.org/html/2606.19980v1)
- [ENPIRE official interactive plots · model and resource data (accessed 16 Sep 2026)](https://research.nvidia.com/labs/gear/enpire/)

## 32. ENPIRE: Experience Across Tasks

建议 2 分钟（含读图、视频及停顿）。

> 读图提示：沿 Pin autoresearch、Written recipes、GPU autoresearch 看传递的是什么。下方 GPU insertion 为官网完整原片转 8×，它展示目标任务，不是迁移消融视频。

ENPIRE §3.4 给了一个很有意思的桥梁。完成 Pin insertion 的 autoresearch 后，Agent 被要求总结和反思有效的 training recipes，再把这份经验加入 GPU insertion 新任务的 instructions。作者报告这些经验可以转移到相似的新 dexterous task。

Appendix B.1 进一步说明，传过去的是明确的 Markdown summary，旧任务的 raw trajectories、hidden logs 和 checkpoints 都没有直接带过去。所以这不是把旧 policy 换个名字部署，也不是 foundation model 的 weights 更新，而是把研究经验放进下次能够读到的外部记忆。

这已经比“只让下一版 policy 更好”更接近 self-improving Agent：过去的实验能影响以后怎样提出和选择方法。不过，当前证据还不能说明改进者的能力会不断增强，更没有证明递归加速。要支持更强的 RSI 结论，还需要 held-out tasks 上有无记忆的比较、相同预算以及重复验证。

### 参考来源

- [ENPIRE §3.4 and Appendix B.1 · written experience transfer from pin to GPU insertion](https://arxiv.org/html/2606.19980v1#S3.SS4)
- [ENPIRE official interactive plots · model and resource data (accessed 16 Sep 2026)](https://research.nvidia.com/labs/gear/enpire/)

## 33. ENPIRE: Cost of Physical Research

建议 2.5 分钟（含读图、视频及停顿）。

> 读图提示：不逐项介绍所有指标，重点看 time-to-success 与 token-to-success 为什么可能朝相反方向变化。

更多 agent–robot pairs 可以更早找到好策略，但可能消耗更多 tokens；每台机器人的 utilization 也未必随规模单调提高。Research wall-clock、policy latency、token consumption 和 robot utilization 不是同一个“效率”。

下表来自官网 Figure 7 的精确绘图数据，保留 mean 和 std。1、4、8 对 agent–robot 的 per-robot utilization 分别约为 49.1%、30.9%、29.8%，GPU active-time fraction 为 29.4%、32.5%、49.0%；整队 token rate 是每分钟 9.3k、40.0k、140.3k。后者不是每个 Agent 的消耗，GPU 指标也不是直接读取 nvidia-smi 的 occupancy。

这些 std 的具体统计层次没有充分披露，不叫 confidence interval。Figure 7 自己的 time-to-success 是 4.5/3.2/2.0 小时，与前面 pin 曲线的约40分钟不是同一组数；不能把两个图的 token 数和时间拼成一个实验。

如果最稀缺的是研究周期，增加资源可能值得；如果预算更紧，最合适的配置就不一样。图中的实测曲线与 linear projection 也要区分，不能都当成实际运行结果。

因此，把经验保存下来并减少重复探索，可能不仅是能力问题，也是成本问题。最后用一张框图把 ENPIRE 已经做到的部分和 RSI 的下一步分开。

### 参考来源

- [ENPIRE, arXiv:2606.19980v1 (Jun 2026)](https://arxiv.org/html/2606.19980v1)
- [ENPIRE official interactive plots · model and resource data (accessed 16 Sep 2026)](https://research.nvidia.com/labs/gear/enpire/)

## 34. Toward Recursive Self-Improvement

建议 1.5 分钟（含读图、视频及停顿）。

> 读图提示：先看上面已运行的 policy improvement 循环，再看下方从 retained recipes / memory 指向 Better future research 的问号。问号不能省掉。

本章已经看到，Agent 能把实机反馈转成下一版 policy 或训练程序，在固定接口内持续搜索。ENPIRE 还把一个任务的经验整理成 recipes，影响下一项研究。两部分合在一起，确实开始接近 self-improving Agent 的方向。

这里把 RSI 展开为 Recursive Self-Improvement，强调的不只是产物变好，而是改进后的系统是否更擅长做下一轮改进。改进对象不一定是 LLM weights，也可能是 memory、tools、workflow 或研究代码。不能因为基础模型 frozen 就排除所有 RSI，也不能因为有循环就宣布 RSI 已成立。

最近的 RoboRSI 报告也讨论把交互沉淀成可复用 skill 和 policy；更早的 Darwin Gödel Machine 则在 coding 任务中修改 Agent 自身代码。它们帮助说明这个概念，但这里不展开另一套结果，更不把 coding benchmark 当成机器人实证。

我想留下的 open question 是：积累的经验，能否在 held-out tasks 和相同研究预算下，让 Agent 更快找到更好的策略，同时不损害旧能力？ENPIRE 提供了可运行的物理反馈循环，也给出经验复用的起点；开放世界、持续可验证的 recursive improvement 仍需要下一步实验。

### 参考来源

- [ENPIRE §3.4 and Appendix B.1 · written experience transfer from pin to GPU insertion](https://arxiv.org/html/2606.19980v1#S3.SS4)
- [RoboRSI · Noematrix research report (Sep 2026)](https://lab.noematrix.ai/blog/2-roborsi/)
- [Darwin Gödel Machine · self-modifying coding agent, not a robotics evaluation](https://sakana.ai/dgm/)

## 35. Takeaways

建议 1 分钟（含读图、视频及停顿）。

> 读图提示：从 Agent 分别沿三条支路看 Role、Artifact 和 Evidence。三章是不同工作位置，不是一条已打通的端到端流水线。

最后只留三个对应关系。Control 产出 Action，要看执行是否可靠。Data 产出候选 assets 和 rollouts，要分别验证 physics 与 downstream training value。Improvement 产出下一版 Policy 或程序，要看 held-out gain 和总成本。

更强模型让这些分工值得重测，但新 demo 不能替代相应的验证。我们真正要问的是：在自己的机器人工作中，哪些信息、判断和执行责任，现在可以重新分配给 Agent？

### 参考来源

- [Technical report · GPT 6 Astra as an Embodied Policy (result images captured 15 Sep 2026)](https://anonymous-report-421.github.io/public-website/?lang=en&view=1)
- [ENPIRE, arXiv:2606.19980v1 (Jun 2026)](https://arxiv.org/html/2606.19980v1)
- [Awesome-Astra-Embodied-AI · curated discovery list, not an evaluation](https://github.com/zjwzcx/Awesome-Astra-Embodied-AI)

## 36. Thank You

建议 0.5 分钟（含读图、视频及停顿）。

谢谢大家。欢迎讨论，也欢迎结合你们自己的机器人系统，说说最想让 Agent 接手哪一部分，以及需要什么实验才能放心交给它。

