# Agents for Robotics：中文讲稿

对应新版 24 页 HTML。幻灯片为英文，讲稿为中文，论文名、模型名和技术术语保留英文。正文可直接讲；“播放与指图提示”不念出。建议总时长约 60 分钟，包含视频、读图和短互动；并非要求将正文逐字匀速读满 60 分钟。正式演讲前建议按自己的语速彩排一次。


## 建议时间安排

| Slide | Title | Minutes | Start |
|---:|---|---:|---:|
| 01 | Agents for Robotics | 0.5 | 00:00 |
| 02 | Demo: A Robot Paints with Feedback | 2.5 | 00:30 |
| 03 | Our Ultimate Goal | 2.5 | 03:00 |
| 04 | Three Questions, Three Case Studies | 1 | 05:30 |
| 05 | Execution: Reasoning Through an Interface | 2 | 06:30 |
| 06 | Claude Plays Robotics | 2.5 | 08:30 |
| 07 | Direct Control Meets Physical Constraints | 3 | 11:00 |
| 08 | A Supervisor Can Disrupt a Capable VLA | 3 | 14:00 |
| 09 | Demo: Placement and Fine Insertion | 2.5 | 17:00 |
| 10 | Demo: Wiping a Table | 1.5 | 19:30 |
| 11 | World Building: Replay and Prediction | 2 | 21:00 |
| 12 | Agentic Real2Sim: A Real Episode and Its Twin | 3 | 23:00 |
| 13 | Agentic Real2Sim: The Conversion Pipeline | 4 | 26:00 |
| 14 | Replay Acceptance on DROID-100 | 3.5 | 30:00 |
| 15 | Demo: Real2Sim and a Disclosed Failure | 2.5 | 33:30 |
| 16 | Improvement: A Repeatable Real Experiment | 2 | 36:00 |
| 17 | ENPIRE: Real Experiments Inside the Loop | 3 | 38:00 |
| 18 | ENPIRE: Environment and Improvement | 4.5 | 41:00 |
| 19 | ENPIRE: Reset and Verification | 3.5 | 45:30 |
| 20 | ENPIRE: Improvement on Pin Insertion | 3.5 | 49:00 |
| 21 | Faster Research, Higher Token Use | 2.5 | 52:30 |
| 22 | Demo: Designing a Tendon-Driven Hand | 1.5 | 55:00 |
| 23 | Demo: Inspecting and Repairing an Execution | 2 | 56:30 |
| 24 | Conclusion | 1.5 | 58:30 |

## 01. Agents for Robotics

建议 0.5 分钟（含读图、视频及停顿）。

大家好。今天想讨论一个很具体的问题：general-purpose Agent 到底能在 robotics 中承担什么工作？我们又怎样判断，这些工作真的带来了可靠的能力？

我会围绕三个标杆展开：Claude Plays Robotics、Agentic Real2Sim 和 ENPIRE。它们分别对应执行、构建仿真世界，以及利用真实实验改进策略。中间会穿插一些应用 demo。希望看完之后，我们既能理解这些展示为什么令人兴奋，也能说清楚，它们离可靠的机器人系统还差哪一步。


## 02. Demo: A Robot Paints with Feedback

建议 2.5 分钟（含读图、视频及停顿）。

> 播放与指图提示：播放约 68 秒的 painting 视频。先提出问题，再让观众看画面的变化；部分解释可以与视频同时进行。

我们先看一个画画的例子。这里，Agent 需要把视觉目标转成一连串物理动作，观察画布上实际出现了什么，再调整接下来的计划。

大家看的时候可以想一个问题：如果最后画得比一开始好了，到底是什么东西变好了？是模型学会了一个新技能，还是计划、标定和指令变得更合适了？

原作者提到了 anchor points、calibration，以及多轮过程中来自人的反馈，有时执行期间也会有人介入。这些信息很重要，因为它们解释了系统如何把图像里的位置和真实画布上的位置联系起来。

结果改善，可能来自更好的动作顺序，也可能只是坐标校准得更准了。我们不能仅凭这段视频，就断言 foundation model 的 weights 在执行过程中发生了更新。经过剪辑的视频，也不能直接告诉我们实际的推理延迟。

但它仍然展示了一个很有价值的工作方式：Agent 可以把观察、规划、执行和修改串起来，围绕一个物理目标持续工作。接下来更值得追问的是：这一轮结束以后，有什么能力真正留下来了？这会是贯穿整场演讲的主线。

### 参考来源

- [@cdngdev, X demo and method thread (8 Sep 2026)](https://x.com/cdngdev/status/2097339677128982873)

## 03. Our Ultimate Goal

建议 2.5 分钟（含读图、视频及停顿）。

> 播放与指图提示：先沿正向箭头讲，再回到反馈箭头。在 reusable capability 处停顿，可以请观众举一个“任务结束后仍能保留的东西”。

我们的目标其实包含两个层次。第一个层次，是把当前这件事完成。第二个层次，是让这次经验帮助下一件事做得更容易。

先看第一个层次。人给出一个目标，但机器人面对的场景通常不会完全符合最初的假设。物体可能偏了一点，抓取可能滑动，接触状态也可能发生变化。系统需要根据实际观察，调整下一步动作。这是当前任务内部的反馈。

第二个层次是经验能不能留下来。假设 Agent 花了二十分钟调试一次抓取，最后成功了，但任务结束以后，所有有效修改都丢失了。那么我们解决了今天的问题，却不一定降低了明天的难度。

能留下来的东西有很多种：修好的程序、可复用的 skill、校准过的场景，或者训练后的 policy。它们也需要不同的检验。程序需要运行测试；simulator 需要预测没有用于拟合的新动作；policy 则需要在没有参与改进的条件下接受评价。

这张图是我们对目标的整理，不是某篇论文声称已经实现的统一架构。尤其要注意，执行到可复用能力的箭头，并不意味着“成功一次就自动学会了”。我们还需要保留有效变化，并证明它在什么条件下仍然有效。

所以后面每个章节，我们都问两件事：Agent 在这一轮里改了什么？又有什么证据，说明这个改动值得留下来？


## 04. Three Questions, Three Case Studies

建议 1 分钟（含读图、视频及停顿）。

第一个问题是执行：给 general model 不同的 action interface，它分别能做什么？Claude Plays Robotics 的价值，在于它测试了不同接口，而不只是挑一个成功行为展示。

第二个问题是 world building：Agent 能不能从一段真实交互中，构建一个有用的 simulator？Agentic Real2Sim 给出了具体流程，也保留了完整的实验分母。

第三个问题是 improvement：Agent 能不能通过真实机器人实验，得到更好的策略？ENPIRE 把 physical robot 放进了这个改进循环。

这三个方向是互补的角色，不是必须依次完成的流水线。比如 ENPIRE 可以直接在硬件上工作，不需要先运行 Agentic Real2Sim。它们的 success rate 统计的也不是同一种东西，因此今天不会把几个百分比放在一起做排行榜。


## 05. Execution: Reasoning Through an Interface

建议 2 分钟（含读图、视频及停顿）。

> 播放与指图提示：先从左到右讲四个框，再沿 observation 的反馈箭头返回 Agent。底部两行只作预告，具体证据留到后面的案例页。

先用这张图说明第一章要看什么。在 execution loop 里，Agent 根据目标做出决策，controller 或 skill 把它变成可执行动作；机器人产生新的 observation，再影响 Agent 的下一次决策。这是我们的简化理解，不是报告完整实现的复刻。

这一章的关键是中间的 interface。一个 move-to tool、一段生成的控制程序，以及一个 VLA，给 Agent 提供的支持并不相同。要解释模型表现，首先得分清哪些难题交给了模型，哪些由现成的 robotics stack 接管。

下面的案例会围绕三个问题展开：精细接触能不能做好？决策是否来得及？额外的 supervision 会帮助执行，还是打断本来有效的动作？图下方的 Evidence 和 Still open 是本章的结论预告，我们稍后逐项看依据。

带着这张图，先进入 Claude Plays Robotics 的原始 interface 对比，再看 direct control、VLA supervision 和几个真实机器人 demo。

### 参考来源

- [Anthropic, Claude Plays Robotics (9 Jul 2026)](https://www.anthropic.com/research/claude-plays-robotics)

## 06. Claude Plays Robotics

建议 2.5 分钟（含读图、视频及停顿）。

> 播放与指图提示：按 interface 读原图。先指出每种设置中模型到底输出什么，再解释结果。留约 20 秒让观众看图。

沿着刚才流程图里的 interface，先看第一个标杆。这里有一个容易被忽略的问题：我们说“让语言模型控制机器人”，到底给了模型什么控制权？

一种方式是 direct control。模型接收 observation，直接选择 action，再根据下一次 observation 继续选择。这样，模型需要承担很大一部分视觉到动作的对应关系，也要理解动作在物理世界里的后果。

另一种方式是 programmatic control。模型先写出一段代码，再由 runtime 执行。这段代码可以包含运行频率很高的 feedback controller。所以，生成 controller 的模型很慢，并不代表生成出来的 controller 也只能慢慢运行。这是两个不同的时间尺度。

还可以把模型放在现成执行系统的上层，比如让它监督一个 VLA。Agent 负责拆解目标、选择指令，而 VLA 提供已经具备 grounding 的动作能力。报告还测试了 reinforcement learning 等设置，我们读图时需要保留这些区别。

举个例子，如果把 direct joint command 换成一个 inverse kinematics 工具，任务变得更容易了，其中一部分原因是工具接管了难题。这可以是很好的工程设计，但我们对模型能力的归因也要随之改变。

这张图的柱子按 model 排列，颜色区分 interface，纵轴是汇总后的 embodiment score，不是某个单一任务的 success rate。不要把每一段颜色直接读成独立的机器人任务成功率。

这就是我选择这份报告的原因：它把模型和 robotics stack 的边界摆到了台面上。讨论“模型是否更懂 robotics”之前，我们先要知道，这个实验到底把哪些 robotics 问题交给了模型。

### 参考来源

- [Anthropic, Claude Plays Robotics (9 Jul 2026)](https://www.anthropic.com/research/claude-plays-robotics)

## 07. Direct Control Meets Physical Constraints

建议 3 分钟（含读图、视频及停顿）。

> 播放与指图提示：播放两个短动画。Humanoid 例子展示生成的 controller；manipulation 只是定性片段。结束前指向 0–5.5% full success 的结论。

左边的 humanoid 例子，对比了生成的 Python controller 和 zero commands。它说明 executable code 可以提供一个很有用的接口：模型花时间生成控制程序，后续较快的反馈更新由程序完成。

右边的 manipulation 例子则提醒我们，中间动作成功和整个任务成功是两回事。机器人能够接近物体、碰到物体、甚至抓住物体，都不代表它能稳定运输并完成最后的放置。某个 subgoal 的表现改善了，最终任务仍然可能很不可靠。

在报告的 direct manipulation 设置里，完整任务成功率大约是 0 到 5.5%。我们需要把动画和这个统计一起看。一条挑选出来的轨迹，无法告诉我们整个任务通常有多可靠。

还有一个直接的约束是 timing。在部分 locomotion 实验中，模型调用时 simulator 会暂停。报告讨论的控制需求大约是 83 Hz，而相关设置下的模型调用频率大约只有 0.2 到 0.4 Hz。暂停 simulation，可以暂时不让推理延迟成为主要限制，单独考察决策质量。但真实机器人通常没法让整个物理世界等它想完。

一个合理的设计，是把快速稳定和底层执行交给 controller，让 general model 处理时间尺度更合适的决策。

不过，这又产生了一个新问题：当我们把 Agent 放到一个已经很能干的 policy 上面，它一定会让结果更好吗？

### 参考来源

- [Anthropic, Claude Plays Robotics (9 Jul 2026)](https://www.anthropic.com/research/claude-plays-robotics)

## 08. A Supervisor Can Disrupt a Capable VLA

建议 3 分钟（含读图、视频及停顿）。

> 播放与指图提示：先指出 base VLA，再比较 supervised variants。这张原图只展示 familiar LIBERO-40。留时间让观众比较，不要把 novel-task 结果当成这张图的一部分。

这一页把问题从底层控制推进到 supervision。底层 policy 已经会做一部分任务，Agent 则通过任务级别的决策影响它的执行。

这里展示的是 familiar LIBERO-40。在这个设置中，额外加入 supervisor，表现可能反而低于 base VLA。报告在其他地方也测试了 novel tasks，其中 supervision 可以带来帮助。但那是另一组结果，不在这张图里。

为什么一个看上去更聪明的 supervisor 会帮倒忙？我们可以想象一个本来正在正确执行的 policy。如果 supervisor 错判了任务进度，提前改了指令，或者打断了一段有效动作，就可能制造出原本不会发生的失败。这些是对 harmful intervention 的可能解释，这张图并没有逐一分离并证明每一种机制。

另一方面，当任务目标是底层 policy 不熟悉的，拆解目标或者提供更合适的指令，又可能补上它缺少的信息。所以 supervision 的价值取决于具体情境。

由此，一个更有信息量的评价方式，是把两类情况分开：它救回了多少 base policy 原本会失败的例子？又损害了多少 base policy 原本会成功的例子？除此之外，还应记录 intervention 次数和额外 latency。

下面的小框图是我们对接口的简化理解。Agent 做任务级决策，VLA 负责动作执行，最终结果由机器人和环境决定。它不是报告完整实现的复刻。

因此，额外的 reasoning loop 本身也是一种 intervention。它可能有收益，也可能有代价。接下来我们看一个较小规模的真实机器人评测，把粗粒度动作和精细接触之间的差别具体化。

### 参考来源

- [Anthropic, Claude Plays Robotics (9 Jul 2026)](https://www.anthropic.com/research/claude-plays-robotics)

## 09. Demo: Placement and Fine Insertion

建议 2.5 分钟（含读图、视频及停顿）。

> 播放与指图提示：先播放 bowl placement，再播放公开的 failed insertion。保留两个 trial count。明确 Robocurve 是独立评测方，不是 OpenAI 官方报告。

这两个视频来自独立评测方 Robocurve。它们可以补充前面的讨论，但系统、任务和实验规模都不一样，不能直接把数字拼起来比较。

在这个设置里，模型接收三个 camera view 和 robot state，通过 move-to interface 请求 absolute end-effector pose，再由 inverse kinematics 处理关节。每次 trial 最多使用二十次 model call，并有 25% speed cap 和其他安全限制。

公开的 Astra 结果是：bowl placement 成功 19/20，fine insertion 成功 2/20。作为对照的 Fable 5.1，在 placement 上是 8/20，在 insertion 上同样是 2/20。

这个差异最有价值的地方，是提醒我们：粗粒度放置做得好，不代表最后几毫米的接触也可靠。把一个成功放置和一个失败插入放在一起，比只展示成功片段更容易看见这个边界。

但不能进一步断言，我们已经知道差异完全来自什么。样本很小，对照还包含不同的 placement rig、非交错执行的实验、人工 reset 和非盲法评分。这些条件都限制了因果解释。

真正值得带走的问题是：当最后几毫米决定成败，系统需要什么 observation 和 control interface，才能做出可靠的修正？

### 参考来源

- [Robocurve, GPT-6 Astra on robotic manipulation (4 Sep 2026)](https://openai.robocurve.org/gpt-6-astra/)

## 10. Demo: Wiping a Table

建议 1.5 分钟（含读图、视频及停顿）。

> 播放与指图提示：播放 wiping 视频，请观众指出一个需要 feedback 的量。保持短 demo 的节奏，不展开成第四篇论文。

这个擦桌子的例子，把应用范围再扩展了一点。相比一次离散的放置，wiping 需要持续地和表面发生接触。

大家可以想一下，机器人至少需要观察什么：目标区域覆盖完了吗？工具是否一直贴着表面？如果工具滑了，或者桌面高度和预期不同，下一步怎么办？

公开的 post 展示了一种行为，但没有提供足够的重复实验和控制细节，来回答这些问题。我们不能仅凭画面上看起来有接触，就推断它具备某种 force-control 能力。

它仍然很好地说明了 Agent 的潜在用途：通过现成工具，协调一个实际任务。

这一章可以收束为一句话：先看 control interface，再判断 Agent 的贡献。Claude Plays Robotics 和这些 demo 提醒我们，precise contact、timing，以及 supervision 是否持续有益，都需要各自的证据。

如果希望减少真实机器人的反复试错，一个自然的方向是先在 simulator 里检查替代动作。但它需要预测相关的物理后果，而不只是看起来逼真。下一章就从这个区别开始。

### 参考来源

- [@k7agar, X wiping demo (6 Sep 2026)](https://x.com/k7agar/status/2096593654320341027)

## 11. World Building: Replay and Prediction

建议 2 分钟（含读图、视频及停顿）。

> 播放与指图提示：分别追踪 recording 到 Agent、recording 到 comparison 的两条路径，再讲 mismatch 的返回箭头。先建立结构，不在这里展开 acceptance 的评分细则。

第二章先看这张流程图。与上一章修改机器人下一步的决策不同，这里 Agent 修改的是 scene 或 model。Agent 和工具创建 candidate，simulator 运行它，再与真实 recording 比较；两者的 mismatch 成为下一轮修正的依据。

图上方的 reference path 很关键。系统当前试图解释的是一个已经观察到的 interaction。如果评价仍然只围绕这个 interaction，我们检验的主要是 reconstruction consistency，而不是新动作下的预测能力。

这也给本章划出了两层问题：能否把 recorded episode 变成可运行、被接受的 replay？如果换一个 action，场景还能不能预测对？Agentic Real2Sim 的 48/100 回答前一层；它依赖具体的 acceptance rule，不能直接用来回答后一层。

接下来先看真实与模拟的配对视频，再沿论文原图拆解 conversion pipeline，随后读完整的评价规则，最后用一个独立作者披露的 dynamics failure 检查这个边界。

### 参考来源

- [Agentic Real2Sim, arXiv:2607.19190v3 (24 Jul 2026)](https://arxiv.org/html/2607.19190v3)

## 12. Agentic Real2Sim: A Real Episode and Its Twin

建议 3 分钟（含读图、视频及停顿）。

> 播放与指图提示：同时播放真实和模拟片段。它们来自同一个 recorded episode，但这里没有做逐帧同步的数值误差分析。

这组视频直接展示了 Agentic Real2Sim 的目标：从一段真实交互出发，构建一个相应的 simulated episode。

这件事远不止重建一个外形相似的 mesh。流程还需要把 robot、scene geometry、camera、object pose 和 trajectory 组装成 simulator 真正能运行的场景，并选择能支持该交互的表示和参数。

难点在于，一段视频通常不能唯一确定一个 physical model。Camera pose 的误差，可能看起来像 object pose 的误差；collision shape 和 friction 也可能在某一条轨迹上互相补偿。于是，不同的模型可能都生成一个相似的 replay。

比如，录制数据里机器人缓慢地从左边推了物体。重建出来的场景可能把这一次推得很像，但它是否能预测从另一侧推、或者更快地推？这是另外一个问题。

这正是章首流程图里 comparison 的边界：与 reference recording 一致，和对新动作有预测力，是两种不同的要求。

我们可以认可一个可运行、可评测的 conversion workflow 的价值，同时把 predictive validity 保留为单独需要验证的问题。下面进入它的内部流程。

### 参考来源

- [Agentic Real2Sim, arXiv:2607.19190v3 (24 Jul 2026)](https://arxiv.org/html/2607.19190v3)

## 13. Agentic Real2Sim: The Conversion Pipeline

建议 4 分钟（含读图、视频及停顿）。

> 播放与指图提示：沿原图的四个阶段讲。每经过一个阶段，都指出它交给下一阶段的 artifact。重点是数据如何流动，不必把所有工具名都念一遍。

首先是 visual processing。系统需要识别相关物体、估计几何，并跟踪 pose。SAM3、SAM3D、FoundationStereo 和 FoundationPose 等专门工具，分别提供一部分信息。

Agent 的职责主要是组织这些工具，而不是在语言模型内部直接完成所有 depth estimation 或 pose tracking。这一点决定了 pipeline 的信息来源，也决定了出了问题以后应该去哪里排查。

第二部分引入 physical priors。系统需要对物体的性质形成结构化假设。有些属性仅凭图像很难确定，因此需要先建立假设，再检验它们产生的 simulation 是否与真实观察一致。

接下来是 scene preparation。几何、pose、camera setting 和 motion trajectory，要在坐标系和 simulator 表示上保持一致。哪怕每个模块单独看都不错，只要模块之间的转换出错，整个场景仍然可能运行失败。

最后，simulator 进入 feedback loop。Pipeline 运行一个 candidate episode，把输出和 recorded interaction 比较，再更新场景。这里既有 Agent 的决策，也有 deterministic optimization 和 search。

读这张图时，可以一直追踪中间产物：perception 之后得到的是估计；assembly 之后得到的是可执行场景；simulation 之后得到的是 replay 和可用于修正的测量。产物越明确，越容易知道失败发生在哪一层。

举个例子，如果物体 geometry 本身就不对，后面的参数搜索可能一直在补偿错误的形状。此时仅仅换一个更强的语言模型，未必能解决问题。不过，这只是关于 bottleneck 的一种合理机制解释，不能把架构图本身当成组件级因果证据。

这项工作的价值，是把一个长而复杂的 robotics toolchain 组织成可检查的流程。至于这个流程究竟有多可靠，还需要看下一页的完整评价口径。

### 参考来源

- [Agentic Real2Sim, arXiv:2607.19190v3 (24 Jul 2026)](https://arxiv.org/html/2607.19190v3)

## 14. Replay Acceptance on DROID-100

建议 3.5 分钟（含读图、视频及停顿）。

> 播放与指图提示：先读左图的 success、partial、failure；再完整解释 candidate/judge 规则；最后指向右图的 logarithmic cost axis。规则讲完后停顿，确保观众理解分母与判定方式。

左图保留了抽样得到的全部一百个 DROID episode。表现最好的 backend 是 Gemma 4 31B：48 个达到 replay-success 标准，8 个是 partial，44 个失败。即使某次运行还没生成有效 replay record 就停止了，也仍然算在这一百分母里。

这个分母很有价值，因为它描述的是整批尝试，而不是只展示 pipeline 最终成功输出的漂亮视频。

但 success 到底是什么意思？Evaluator 首先筛选 reconstruction candidate，例如要求 grasp probe 有效、replay video 存在，以及 motion statistics 有限并且落在合理范围。随后，最多选五个 candidate 交给 judges。

三个 VLM judge 比较真实和模拟的关键帧。评分关注 target-object identity、final object location、action similarity 和 final gripper location。每个 judge 会选出自己评分最高的 candidate。

只要任意一个 judge 的最佳 candidate 达到 8/10 或以上，这个 episode 就可以通过。这是一种寻找可接受 candidate 的规则，不是 majority voting，也不要求三个 judge 一致，更不是把所有 candidate 的分数取平均。

因此，48/100 的准确含义是：在这套 acceptance rule 下，pipeline 为多少个 episode 找到了被接受的 replay。它并不直接等价于 friction、stiffness 等物理参数估计准确，也不等价于新动作下的预测准确。

再看右边，cost axis 是 logarithmic scale。论文统计的是 model-call bill，而不是 perception、simulation 和 preparation 的全部成本。这个结果可以支持 model usage 的成本比较，但不能直接当成完整部署成本。

其他 backend 得到的 accepted episode 数量在 37 到 45 之间。它说明这个 workflow 可以搭配不同模型工作。不过，不宜把这一次排序扩展成普遍的模型能力排行榜，尤其当不少失败可能来自 pipeline 的其他部分时。

对我们的问题来说，下一步真正有价值的实验，是改变 action 或 initial condition，再检验 simulator 的预测。下面这个 demo 会更直观地说明，为什么一个漂亮的 replay 仍然可能留下重要的物理问题。

### 参考来源

- [Agentic Real2Sim, arXiv:2607.19190v3 (24 Jul 2026)](https://arxiv.org/html/2607.19190v3)

## 15. Demo: Real2Sim and a Disclosed Failure

建议 2.5 分钟（含读图、视频及停顿）。

> 播放与指图提示：播放两个作者 demo。Microphone 使用原视频 35–60 秒的片段。先说明 dynamics failure，再解释动画。它们不是 Agentic Real2Sim 论文的新增实验。

这里是独立作者展示的 Agent-assisted Real2Sim workflow，与刚才论文的评测分开来看。

公开描述涉及 multi-view RGB、已知 robot action、camera calibration、asset construction、MuJoCo execution 和 Blender rendering。一个 coding Agent 能把这么长的工具链组织起来，本身就是很有意思的应用。

其中 microphone 的例子特别值得保留，因为作者明确披露了失败：dynamics 没有成功，展示出来的是 kinematic replay。用到的 rigid proxy 没能表达任务所需的 compliant snap-fit behavior。

这说明一种可能的 model-class 问题。如果表示本身无法表达关键的 deformation 或 contact，那么反复调整几个物理参数，也未必能得到正确预测。这个解释来自该案例披露的限制，不应推广成所有 Real2Sim 方法都存在同样失败。

工程上的进展和物理上的局限可以同时成立。Agent 确实搭起了复杂流程，也产生了直观的可视化；但我们需要的 predictive model，仍然没有因此得到证明。

回到章首的流程图，这一章的结论是：Agent 可以组织出可运行的 scene 和 replay，但 recording 之外的 predictive validity 仍需要单独检验。Replay acceptance 不等于物理模型已经被验证。

如果我们的目标是改进机器人，可以继续加强 simulator 并测试新动作，也可以直接获取真实机器人的反馈。下一章 ENPIRE 选择后一条路线：它不必先完成 Agentic Real2Sim，而是要解决如何反复运行真实实验的问题。

### 参考来源

- [@Lingxiao234, X Real2Sim and failure thread (8 Sep 2026)](https://x.com/Lingxiao234/status/2096992059731443923)

## 16. Improvement: A Repeatable Real Experiment

建议 2 分钟（含读图、视频及停顿）。

> 播放与指图提示：先点明 human-assisted setup 与 fixed API，再沿 Agent、real rollout、verifier/logs 及反馈箭头讲一遍。把 reset、verification 和 retry 留作后续读图线索。

第三章换一种获取证据的方式：直接把真实机器人实验放进改进循环。先看图中的 Agent，它修改 policy 或 training procedure；real rollout 检验这个版本，verifier 和 log 提供结果与过程信息，再帮助 Agent 决定下一次修改。

这里改的不是当前 rollout 的某个动作，而是后续实验还会使用的策略或训练程序。这是它与 execution loop 的主要区别，也让我们有机会讨论：一轮实验结束后，什么有效变化被保留下来了？

图左边的 fixed environment contract 是前提。ENPIRE 先通过 human-assisted setup 建立接口；进入 improvement 阶段后，action、reset 和 success signal 的定义保持稳定。Agent 改策略时，不能顺便把成功标准也改掉。

这一章会用 ENPIRE 展开这张图：先看真实任务和原始方法图，再看 reset 与 verification 如何支持反复试验，最后检验 policy improvement 的曲线及资源代价。看结果时要一直保留 conditional retries 和已测试环境的边界。

### 参考来源

- [ENPIRE, arXiv:2606.19980v1 (Jun 2026)](https://arxiv.org/html/2606.19980v1)

## 17. ENPIRE: Real Experiments Inside the Loop

建议 3 分钟（含读图、视频及停顿）。

> 播放与指图提示：播放原始 task video 中 300–330 秒的片段。它展示 hardware interaction，不是完整 rollout，也不是 success-rate 统计。

在 ENPIRE 里，Agent 可以提出一个策略修改，运行真实机器人实验，检查发生了什么，再决定下一次修改。

这里的 improvement 可以落在不同产物上。Agent 可能编辑 heuristic program，也可能修改 training procedure，或者通过环境接口训练 policy。这些变化并不要求 general language model 自身更新 weights。

做 robotics 的同学应该会觉得，这很像我们平常的一部分工作：改代码、跑一次、看 video 或 log、解释失败，再继续修改。但大量时间往往花在准备下一次实验，以及判断上一轮究竟算不算成功。

ENPIRE 把这些外围环节放进了方法本身。机器人需要 action interface、hard safety constraints、automatic reset 和 success verification。缺少这些组件，Agent 想要更多证据时，就不能随时启动下一次实验。

这一页的视频让我们看到物理场景。真正需要评价的，是一个可重复过程能否在清楚定义的 protocol 下产生更好的策略。接下来先看 environment 与 improvement 的分工，再看 reset 和 verification，最后读 learning curve 和资源代价。

### 参考来源

- [ENPIRE, arXiv:2606.19980v1 (Jun 2026)](https://arxiv.org/html/2606.19980v1)

## 18. ENPIRE: Environment and Improvement

建议 4.5 分钟（含读图、视频及停顿）。

> 播放与指图提示：先追踪原图中的 human-assisted environment setup，再进入 improvement loop。可以问：“你们平常的机器人实验里，哪一步最耗时间？”留一小段回应时间。

这张图把两个容易混淆的阶段分开了。第一个阶段，是 environment construction；第二个阶段，才是在这个环境里进行 autonomous improvement。

构建 environment 的时候，系统会利用 human feedback，建立控制接口和配套工具，包括 safety constraints、automatic reset 和 success verification。构建完成以后，改进过程通过 immutable Gym APIs 访问这些能力。

这个边界让后面的实验结果有稳定的含义。Agent 可以改 policy 或 training procedure，但 improvement 期间 environment contract 保持固定。否则，如果策略做不好时，系统还可以顺手重新定义 success，那么分数上升就很难解释了。

在这个固定接口里，policy improvement 提出并实现修改，real rollout 检验当前策略。Agent 可以查看 trajectory、video 和 reward signal，再决定下一次尝试。

策略的实现方式并不是唯一的。论文探索了 heuristic code，也包括 behavior cloning、reinforcement learning，以及与 VLA 的组合。这些是生成行为的不同路径，不能概括成“同一个模型把所有东西都学会了”。

这里还有两个时间尺度。较短的尺度上，policy 执行一个 trial，并可能根据当前反馈进行修正。较长的尺度上，research Agent 比较实验依据，修改 policy 或 training code，让后续 trial 使用新的版本。后者产生的产物有机会跨越当前 rollout 保留下来。

系统还支持多个 agent-robot pair 并行工作。不同 Agent 可以探索不同 hypothesis，也可以交换有效的代码改动。这样可能更快找到好策略，但总成本是否更低，需要后面的资源实验单独回答。

大家可以看到，很大一部分贡献不在某一个 optimizer 里。再聪明的下一步想法，如果机器人不能 reset、log 看不出失败原因，或者 verifier 给错 reward，也很难转化成可靠进展。Experimental interface 决定了 Agent 到底能从试验里获得什么信息。

因此 human-assisted setup 不能从结论里消失。这里证明的是：在搭建好的环境和接口内，Agent 可以进行自动改进。它不等于机器人进入一个任意实验室，就能独立建立所有 safety 和 evaluation 条件。

下一页把其中两个关键环节具体展示出来：如何让物理任务重新开始，以及如何判断结果。

### 参考来源

- [ENPIRE, arXiv:2606.19980v1 (Jun 2026)](https://arxiv.org/html/2606.19980v1)

## 19. ENPIRE: Reset and Verification

建议 3.5 分钟（含读图、视频及停顿）。

> 播放与指图提示：依次播放 pin reset 和 zip-tie verification。Reset 约 62 秒。两个视频来自不同任务，不要讲成同一个 rollout 的同步流程。

Automatic reset 让一次实验变成可以反复运行的实验。如果每次失败都需要人恢复现场，Agent 的自主工作就会停在这里。

Pin 的例子展示了系统怎样准备下一次 trial。Reset 的质量也影响实验是否可比。假如后来的 policy 总是得到更容易的 initial state，那么分数改善可能部分来自状态分布变了，而不是策略更好了。

ENPIRE 的部分 reset 从较困难的 task subphase 开始。这是研究复杂 manipulation 的合理方式，但我们必须保留这个前提。从特定 subphase 出发的成功，不应被重新描述为“任意初始状态下都能完成全任务”。

第二个例子展示 zip tie 的 verification。系统利用视觉处理，判断 strap 是否穿过 head，论文讨论了通过两个 camera view 降低 false positive。其他任务还可以结合 proprioception 或 torque 等信号。

Verifier 提供了 Agent 据以改进的结果。如果出现 false positive，系统可能奖励了错误行为；如果出现 false negative，又可能错过有效修改。

因此，要把三个问题分开：动作是否安全，reset 是否正确，success test 是否可信。它们各自承担不同职责，通过其中一个并不证明其他两个也没有问题。

有了这些前提，接下来我们再读 improvement curve，才知道曲线究竟代表了什么。

### 参考来源

- [ENPIRE, arXiv:2606.19980v1 (Jun 2026)](https://arxiv.org/html/2606.19980v1)

## 20. ENPIRE: Improvement on Pin Insertion

建议 3.5 分钟（含读图、视频及停顿）。

> 播放与指图提示：先读左侧不同 backend 的 learning curve，再读中间不同 team size 的曲线。讨论接近 99% 的结果时始终保留 retry 口径；可问观众还需要什么信息才能知道 one-shot precision。

这是论文结果图中 pin insertion 的部分，原来的 axes、legend 和任务示意都保留下来了。

左侧曲线随着 research time 推进，展示策略性能如何变化。Horizontal axis 是实验开发耗费的时间，不是最终 policy 在部署时生成 action 的 latency。

中间改变的是 agent-robot pair 的数量。更多并行实验，可以更快找到高性能策略。论文报告，在 pin insertion 上，从一个 pair 扩展到八个 pair，达到接近完美 success rate 的时间，从超过一个半小时降低到大约四十分钟。

但在解释最后的 success rate 之前，需要先说明 rollout 的定义。ENPIRE 使用固定的 retry budget，最多允许八次 retry。后续尝试可以利用之前失败带来的信息，所以这个指标同时包含初次执行的 precision 和 rollout 内部的 recovery。

因此，在这套 protocol 下接近 99%，不能直接说成 99% one-shot insertion precision。它也不是 independent best-of-eight，因为这些尝试不是相互独立的。我们不能代入独立 Bernoulli 假设，反推出一次尝试的成功概率。

这不意味着 recovery 没有价值。真实部署里，发现失败再修正，本来就是重要能力。关键是准确承认它测量了什么，同时保留 retry budget 和所需时间。

这组结果支持一个明确而有边界的结论：在定义好的 environment 内，这个 research workflow 能随着实验推进改进 policy，额外并行资源也能缩短发现高性能策略的时间。

仍然值得进一步测量的包括：first attempt 有多可靠？Recovery 增加了多少时间？留下来的策略，在新的 starting condition 或相关任务上是否仍然有效？

此外，发现好策略更快，不代表整体资源使用更少。下一页专门区分这两件事。

### 参考来源

- [ENPIRE, arXiv:2606.19980v1 (Jun 2026)](https://arxiv.org/html/2606.19980v1)

## 21. Faster Research, Higher Token Use

建议 2.5 分钟（含读图、视频及停顿）。

> 播放与指图提示：依次读 utilization、实测 token use 与 linear projection、time/cost。可以短问一句：当前更关心最低 elapsed time，还是最低 total cost？

这张图把 scaling 的几种含义拆开了。

首先是 utilization。随着 fleet 变大，GPU utilization 可以提高，但平均到每台机器人的 utilization 可能下降。增加机器人数量，并不保证每台机器人都把更多比例的时间用在执行实验上。

接下来是 token usage。图中同时给了实测曲线和 linear projection。实测曲线描述运行过程中真正发生的资源消耗；projection 则是一个简单线性增长的参照，两者不能混在一起说。

最后，图把 tokens to success 和 time to success 分开。更大的 fleet 可以更早达到目标，同时消耗显著更多 tokens。论文的结果体现的是用 token efficiency 换取更短的开发时间。

这个交换是否值得，取决于目标。如果最稀缺的是上线窗口或实验周期，缩短 elapsed time 可能值得付出更多成本；如果预算才是主要约束，最合适的配置又可能不同。

对今天的讨论，重要的是把量说清楚。Research wall-clock time、policy latency、token consumption 和 robot utilization 回答的是不同问题，不能全部压缩成一个含糊的“效率更高”。

结合前面的 learning curve，我们可以给 ENPIRE 一个具体评价：它组织起了能够改进策略的真实实验流程，同时也明确暴露了配套基础设施和资源 tradeoff 的重要性。

这也是第三章的简短总结：在固定的 environment contract 下，真实 rollout、reset 和 verification 可以支持 policy improvement；但结果仍要连同 human-assisted setup、conditional retries 和已测试条件一起解释。

现在可以把三个角色放在一起看：execution 改决策，world building 改 scene，improvement 改 policy 或 training procedure。结束前，再看两个短应用 demo，看看控制之外还能留下哪些工程产物。

### 参考来源

- [ENPIRE, arXiv:2606.19980v1 (Jun 2026)](https://arxiv.org/html/2606.19980v1)

## 22. Demo: Designing a Tendon-Driven Hand

建议 1.5 分钟（含读图、视频及停顿）。

> 播放与指图提示：播放 CAD animation，始终保留 “Not a validated physical hand”。可请观众说出一个下一步必须做的物理测试。

这个例子从“控制机器人”转到了“帮助设计机器人”。作者展示了 Agent-assisted CAD 和 visualization，包括生成的 geometry 以及 hand animation。

它的视觉复杂度很高，但作者同时明确指出，当前设计不能直接在现实里工作。我们需要保留这两个事实。因此这里展示的是 design artifact，不是一只已经制造出来、并经过验证的机械手。

下一步可能要检查 tendon routing、friction、actuator requirement 或 manufacturing tolerance，再进入 physical prototype。具体做什么测试，取决于希望成立的工程结论是什么。

这和刚才评价 replay 的原则一样：可视化很有用，但 physical validity 仍然需要与产物相匹配的证据。

### 参考来源

- [@earthtojake, X hand design and limitation thread (10 Sep 2026)](https://x.com/earthtojake/status/2097789988670709821)
- [Author limitation and follow-up](https://x.com/earthtojake/status/2097789991426335015)
- [Author limitation and follow-up](https://x.com/earthtojake/status/2097801101890207893)

## 23. Demo: Inspecting and Repairing an Execution

建议 2 分钟（含读图、视频及停顿）。

> 播放与指图提示：播放约 30 秒的 ASPIRE trace-inspection 片段，指出 observation 和 program repair 的对应关系。保持 demo 深度，不扩展成完整论文分析。

ASPIRE 展示的是另一种可以留下来的产物：修好的代码和 reusable skills。

项目记录 multimodal execution trace，用它定位失败并修复程序。视频把物理观察和代码改动之间的联系直接展示了出来。

一个经过修复的 skill library，可以让这次调试的成果跨越当前 session 留下来。这属于 external memory 和 executable code，不一定需要改变 foundation model 的 weights。

要证明它真的形成了有用积累，我们还需要测试：留下的 skills，是否让后续任务更容易？这段视频本身不足以证明 open-world continual learning，这里也不额外引入新的 benchmark 数字。

Hand design 和 debugging 两个例子共同说明，Agent 的贡献不只在于选择下一步 action，也可以是给 robotics workflow 产生可复用的工程产物。最后要回答的，是怎样知道这些产物值得依赖。

### 参考来源

- [ASPIRE, arXiv:2607.00272v1 (Jun 2026)](https://arxiv.org/html/2607.00272v1)

## 24. Conclusion

建议 1.5 分钟（含读图、视频及停顿）。

最后回到开头那个画画的机器人。令人感兴趣的，是 Agent 能围绕一个物理目标，把决策和工具组织起来。三个标杆则帮助我们更精确地检查，这种能力到底成立到什么程度。

Claude Plays Robotics 提醒我们先看 control interface 和 time scale。Agentic Real2Sim 展示了可检查的 conversion workflow，同时把 recording 之外的 predictive validity 留给单独测试。ENPIRE 则说明，在 reset、safety 和 verification 到位的条件下，真实硬件可以进入持续改进策略的循环。

那些应用 demo 扩展了产物的范围：真实行为、simulated scene、mechanical design，以及 repaired program。把每个例子实际产生的东西说清楚，它们的价值也就更容易判断。

希望大家最后带走的问题是：这一轮结束以后，什么留下来了？它是否真的让一个新任务更容易？

这个问题既保留了 demo 带来的想象力，也给了我们评价研究进展的具体标准。谢谢大家。

