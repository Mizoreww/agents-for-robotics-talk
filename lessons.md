# Project Lessons

## 2026-09-10 — 复用参考 talk 的问题驱动叙事，而不只是视觉模板

**Context**: 为机器人 Agent survey 组织深入技术分享，参考此前的 Steerable VLA talk。

**Mistake**: 首版主要按能力分类和作品谱系组织，更多复用了参考的视觉语言，没有充分复用其从目标、现有方案与瓶颈推导研究问题，再由方法和实验回答问题的叙事结构。

**Rule**: 本 talk 按“背景 → 问题 → 方法 → 实验与局限 → 总结”组织。先读取参考 talk 的实际页序与讲稿；基石工作用于解释现有方案及其缺口，不单设论文时间线章。每条方法路线从明确问题出发，按 Big Picture、关键机制、证据、局限展开。

## 2026-09-10 — 字体、动态媒体与综合框图都要忠实落实

**Context**: 继续英文机器人 Agent survey PPT；用户再次强调沿用上一场 talk 的字体，尽量加入视频/GIF，并把综合理解画成框图。

**Mistake**: 初版虽然在 PPTX 中声明了参考字体，但渲染器回退为无衬线字体，尚未证明实际交付画面与参考一致；部分综合关系仍只用文字或表格表达。

**Rule**: 从参考 HTML 的实际 CSS 核对标题与正文字体，检查最终渲染而不只检查字体声明；优先嵌入可离线播放的视频；将跨论文综合理解画为可编辑框图，标明为 synthesis，并逐条验证箭头方向和反馈关系。

## 2026-09-10 — 收敛标杆，以原图和动态展示为主

**Context**: 用户审阅机器人 Agent survey 后认为内容过多，并要求增加论文/项目原图、视频/GIF，以及推特/小红书上的应用 demo。

**Mistake**: 按 36 页覆盖大量工作，易形成逐篇罗列；即使有综合框图，也不能替代直观的原始媒体。

**Rule**: 正文只细讲最多 3 个最重要的标杆工作，其余缩到背景、对照或附录；主要用论文原图和项目视频/GIF承载讲解，综合框图只补充机制理解。单设应用 demo 展示，明确标注其展示性质，不把社媒演示当成定量验证。

## 2026-09-10 — 单文件内嵌 HTML 与章节内小结

**Context**: 用户要求回到此前的 HTML 交付方式，并在每一章保留简短总结和综合框图。

**Mistake**: 上版以 PPTX 和依赖 slides/media 目录的离线 HTML 压缩包交付；综合框图集中在结尾，章节内缺少收束。

**Rule**: 当前主交付必须是可独立移动的单个 HTML，图片、视频、字体、讲稿和运行脚本全部内嵌；在三个标杆章节内分别加入机制框图、已证实贡献和未解决问题。全稿审查要检查问题与证据的对应、章节过渡和最终结论，不能只核对单页事实。

## 2026-09-10 — 幻灯片语言与讲稿语言分开处理

**Context**: 用户要求重新审核整场演讲并补充讲稿，随后明确讲稿用中文、专有名词用英文。

**Mistake**: 从英文幻灯片推定讲稿也应使用英文，生成了英文逐字稿。

**Rule**: 本 talk 保持英文幻灯片，但当前逐页讲稿、过渡、读图及播放提示使用自然中文，论文名、模型名和技术术语保留英文；HTML 内嵌讲稿与独立讲稿文件必须同步更新。

## 2026-09-10 — 章节流程图先于案例展开

**Context**: 用户要求将每个章节的流程图放到章节最前。

**Mistake**: 三章机制流程图放在章末作为总结，观众在看案例前缺少整体结构。

**Rule**: Execution、World building 和 Improvement 三章均以对应流程图开场，再展开标杆工作与应用 demo；流程图讲稿改成章节导读，章末保留简短收束。移动后同步页码、时间表、媒体归属和中文讲稿，不增加重复流程图页。

## 2026-09-10 — Execution 用工具集合解释，其他应用单列第四章

**Context**: 用户要求第一章画成 Agent 调用多种 Agent Tools（IK、VLA、WAM 等），说明接口优势，并把机械手 demo 放进结构设计及其他应用章节。

**Mistake**: 将执行框图简化成 Agent → 单一 Controller → Robot，遮蔽了工具选择和不同接口的作用；把设计与调试放在结尾附带展示，没有明确分类。

**Rule**: 第一章使用 Agent 向多种 Agent Tools 分支的结构，结合 Claude Plays Robotics 区分各接口的优势、代价和已测证据；IK、WAM 等扩展例子不得伪装成该报告的测试项目。新增第四章 Other Applications，明确机械手为结构设计应用、尚未验证的 design artifact；保留三篇标杆细讲，不把应用展示扩成新的论文综述。

## 2026-09-11 — 从直接动作叙述 Execution，最后用 RPent 收束

**Context**: 用户要求第一章先讲 Agent 直接控制，最后收束到 RPent，并在章首框图补上直接输出 q / EEF Pose 的分支。

**Mistake**: 将 RPent 工具包页紧接在框图后，先讲系统封装再讲执行问题；框图只列 Agent Tools，遗漏直接动作输出，章末也没有明确综合语义/长程能力与连续接触控制的差距。

**Rule**: 保留章首框图，但按“直接动作 → 接口如何提供支持 → 能力与局限 → RPent 工具组织”展开第一章。框图区分直接 q / EEF Pose 命令与可调用的控制/生成式工具，并说明底层伺服仍存在。章末同时总结 foundation-model 能力与 interface 设计的作用；语义、泛化、长程规划的优势和连续性、接触、精细操作的限制须限定在已有证据范围，不把趋势写成所有模型或任务上的严格单调定律。

## 2026-09-14 — 将直接控制与工具调用保留为随模型能力变化的开放问题

**Context**: 用户要求结合 Awesome-Astra-Embodied-AI 与最新机器人预训练证据，重新讨论第一章，并研究 RSI 后再决定是否改稿。

**Mistake**: 旧主线容易把特定模型/任务下的接口优势外推为“LLM 必须调用工具”，并把当时直接控制的不足当作长期能力上限。

**Rule**: 对照最新版讲稿与当前一手证据，区分模型训练带来的能力、直接 action 输出、低层 controller 与高层 tool orchestration；不预设工具必需，也不凭 demo 断言全面替代。机器人数据规模及因果解释必须有明确披露或对照实验支持。先讨论 Astra 和 RSI 的证据及新主线，不在用户确认前改动讲稿或演示文稿。

## 2026-09-14 — 每章只围绕一个代表工作形成完整论证

**Context**: 用户指出新版每章仍混入过多 supporting works，导致叙事混乱、信息失真，并要求补充 Direct/Hybrid 报告的具体架构，重新梳理各章的问题、方法、实验结果。

**Mistake**: 将“最多三个深讲标杆”理解为还可在各章穿插多个半展开案例；匿名报告只给 demo 和结果，没有把 joint-space candidate、Astra review、EEF correction 与执行步数的实际机制讲完整，跨论文综合先于单篇事实。

**Rule**: 正文每章只选一个代表工作，按“问题 → 原始方法/架构 → 实验设置与结果 → 局限/章节总结”讲完整；其他论文退出正文论证，仅留参考或独立 demo montage，不用它们补齐主工作的缺口。第一章以用户指定的匿名 Direct/Hybrid 报告为代表，保留原架构及 1–15 vs 1–5 control-step 差异；明确 foundation model 内部网络未披露，不把执行架构冒称网络结构。先核查同一工作的事实，再作有限综合，不跨工作拼接结果或推广因果。

## 2026-09-14 — Control 允许一页历史背景，但不能把训练原因写成已证事实

**Context**: 用户补充希望 Control 简述此前工作和架构，并说明机器人数据训练改变了旧结论的适用范围。

**Rule**: Control 可用一页对照 direct action、controller code、learned policy 的旧架构，再集中讲唯一代表报告；不恢复多篇案例轮播。表达为“模型接受机器人数据训练、能力前提变化后，旧设置结论需重新检验”，不宣布旧实验作废，不把 Astra 未披露的机器人数据规模/训练因果写成事实。

## 2026-09-14 — 保留 Control 总框图，按分层范式到新能力重组

**Context**: 用户指出 Control 最开始的综合框图不能丢，并指定新的背景与证据顺序。

**Mistake**: v0.7 用匿名报告的局部架构替代了原始 Agent 控制总框图，并把 Claude Plays Robotics 的具体实验压缩得过度。

**Rule**: 保留原始 Control 总框图（含直接 q / EEF action 与 Agent Tools 分支）；随后以此前 talk 的 Hi Robot 与 Figure 共三张原架构图解释常见 System 2 / 1 / 0 分层，再具体讲 Claude Plays Robotics 的实验与结果、用一张 RPent 图说明工具组织，最后引入 Astra Direct / 不同 action interface 的新证据与开放问题。先检索、核实、给提纲，用户确认前不改 HTML 或讲稿。不能把常见架构说成无争议定律，也不能把未披露的 Astra 机器人预训练因果当成已证事实。

## 2026-09-14 — 精简叙事不能省掉各来源的实验结果

**Context**: 用户审核 v0.8 后要求第一章补更多结果表，明确包括 RoboDojo、RoboLab，并要求后两章也补充。
**Mistake**: 过度压缩为少量 headline numbers 和演示视频，未给出足够逐任务/逐条件结果，导致读者无法检查每个来源的完整实验结论。
**Rule**: 保留少量代表工作和原图/视频，同时为每个具有定量评测的正式来源补紧凑结果表，注明 task、condition/baseline、metric、分母和限制。RoboDojo 与 RoboLab 必须分表并保留 selected-case/final-slot 口径，不能混池；只有定性展示的来源明确写未公布系统评测，不制造数字。Simulation / Improvement 同样补足结果与对照，不靠 headline 代替实验。

## 2026-09-14 — 用诊断框图收束，并突出表内可比最优值

**Context**: 用户要求第一章总结纳入 Semantic / Spatial / Physical 诊断，合并章首 VLA / WAM / Learned policy，重排 Claude interfaces，简化 Takeaways 并增加感谢页。
**Mistake**: v0.9 的总结仍偏文字，learned action tools 分得过碎，接口图对齐不够清楚，表格没有系统突出可比最优值。
**Rule**: 第 4 页合并 learned tool 节点；第 7 页以 LLM 开始、接口居中，并明确 Controller 与 Policy 的不同路径，不画出错误的统一执行链。所有原生结果表只在同任务同指标的可比组内加粗最佳值（并列同样加粗），不得给成本、样本数或不配对的 retained slots 硬排优劣。第 18 页用能力诊断收束，第 36 页用少字框图总结全稿，另加感谢页，同步中文讲稿并做完整视觉和离线验证。

## 2026-09-15 — Data 作为第二类，并区分 Agent 推理频率与控制频率

**Context**: 用户要求第二类统一为 Data，包含 Real-to-sim Replay / Data Rollout，机械手资产设计并入；第一章需要明确 Astra 实际 action interface、推理频率与能力边界。
**Mistake**: 旧分类将第二章限定为 Simulation、把设计孤立在 Beyond，第一章概念总结未充分说明真实案例中的控制链路和速率限制。
**Rule**: 第二类采用 Data，并准确区分 replay、rollout 与设计资产；移动 hand demo 但保留未验证物理可用性的限制。逐来源记录 Astra 输出的 joint targets / EEF pose / controller code / atomic skills 与底层执行器，分别报告 LLM decision latency、action horizon 和 controller Hz。第一章突出已展示的语义理解与空间泛化，明确高频反馈控制和可靠物理泛化仍是短板；不得把控制器频率当成 LLM 推理 Hz，也不得用 demo 泛化成永久能力不可能。

## 2026-09-15 — 用职责迁移解释 Control 主线，去掉 Hi Robot 结果岔路

**Context**: 用户要求删掉第6页Hi Robot结果，画出从“System 1承载generalist能力”到“System 2承担更多动作决策、System 1提供action primitives”的变化。
**Mistake**: Control仍容易变成论文结果串讲，没有用一张图明确generalization与动作智能的责任在何处、为何值得重新分配。
**Rule**: 保留第5页原架构，删除第6页Hi Robot定量页并以职责迁移示意图替换；从steerable generalist policy的原先设想讲到部分空间/动作决策上移。System 1/action primitives只是本talk的功能性简称，不把IK/OSC冒称learned VLA；System 0仍负责servo/低层控制。泛化与“任意(o,l)→a”是设计目标，非已证能力；机器人数据训练对Astra的具体因果仍未披露。

## 2026-09-15 — 职责迁移图要用面积和箭头表达，不在图上重复讲稿

**Context**: 用户认为新画的职责迁移页字太多，要求更美观。
**Mistake**: 每个System框同时放角色、职能、解释句，再叠加迁移说明和结论条，造成阅读负担。
**Rule**: 将职责迁移页压缩为两条System 2→1→0链：保留角色与最短标签，用System 2扩大/System 1缩小、颜色和迁移箭头表达主旨。实验条件、primitive定义与训练因果限制放入同步讲稿和来源说明，图上不重复段落。

## 2026-09-15 — 职责迁移页末端直接标 Controller

**Context**: 用户要求把新职责迁移图中的sys0直接写成Controller。
**Mistake**: 在末端框同时保留System 0与Servo，使概念层级和实现名称重复。
**Rule**: 第6页两条链的末端均只标Controller，不再显示System 0或Servo；同步讲稿与当前章节文档。第5页原始论文架构图不改写。

## 2026-09-15 — Controller 上方保留 System 0 层级标签

**Context**: 用户再次明确System 0还是需要加上。
**Mistake**: 上版将层级标签完全去掉，只留下Controller。
**Rule**: 覆盖前一条命名偏好：第6页两条链末端均保留System 0作为层级标签、Controller作为功能名称，不恢复Servo；与System 2和System 1的层级排版一致。

## 2026-09-15 — Control 精简到 Astra，结果优先用报告原图

**Context**: 用户要求删除Claude Plays Robotics与RPent，职责迁移图后直接重点讲Astra；RoboDojo/RoboLab大表换成原报告结果截图并加入报告后部热力图。
**Mistake**: 历史背景仍占四页，打断职责迁移到新模型证据的主线；重制大表不如原报告图直观。
**Rule**: 当前Control删除Claude/RPent方法及结果页，并清除讲稿中的对应过渡；Astra成为直接后续。RoboDojo/RoboLab采用经来源核实的原始结果图，补报告热力图，保留实验口径与限制；同步页序、导航、讲稿、引用和验证，不只隐藏页面。


## 2026-09-16 — Data 小结收束到如何利用产物

**Context**: 用户调整第21页下游训练问题。
**Mistake**: 小结只问已有数据是否改善训练，没有引出如何利用这些产物。
**Rule**: 当前 Data 小结使用“How can we use it for downstream training?”，中文讲稿相应讨论如何把资产、replay、rollout用于训练；不把这个开放问题表述成已验证的训练收益。

## 2026-09-16 — P3/P23 删除冗余说明后重新居中
**Context**: 用户要求删除 P3 底部概括句以及 P23 的 Evidence / Still open 两块文字。
**Mistake**: 页面同时保留框图与重复说明，删去文字后若不重排会留下偏上的内容重心。
**Rule**: P3 保留三角色与问题，P23 保留章首闭环图；删除指定说明后重新居中其余正文与标题，保留统一页眉标识、页脚和字体。不恢复被删段落，不改动其他页。

## 2026-09-16 — 删除文字后的居中仅指竖直位置
**Context**: 用户纠正 P3/P23 的居中修改，没有要求水平居中。
**Mistake**: 把原本左对齐、分列的内容改成水平居中，并移动了标题。
**Rule**: 本次及同类删除说明后的重排，仅调整正文的 y 坐标以平衡竖直留白；保留所有原始 x 坐标、宽度、水平对齐、字号、分列和标题位置。若未明确要求，不把“居中”扩展成水平改版。此条覆盖上一条关于 P3/P23 标题居中的解释。

## 2026-09-16 — ENPIRE 按官网的解释顺序展开
**Context**: 用户提供官网目录截图，要求第三章叙事更有逻辑。
**Mistake**: 把方法、结果、demo 和经验迁移交错排列，没有沿官网由效果到系统再到验证的主线展开。
**Rule**: ENPIRE 按 Learned Policy → System → Environment Loop（Auto Evaluation、Auto Reset 与案例）→ Policy Improvement → Evaluate Coding Agent → Fleet Scaling → Simulation Evaluation → Limitations 的顺序讲述；保留章首图，在局限之后衔接 RSI。同步逐页中文稿和过渡，不影响前两章，也不恢复用户已经删除的说明或水平居中改动。

## 2026-09-16 — ENPIRE 引用采用学术格式，结果 demo 后置
**Context**: 用户要求 ENPIRE 灰色引用按学术风格，并把原 P24 demo 放到后面。
**Mistake**: 页脚混入大量制片和证据说明；机械沿用官网先展示效果的顺序，不符合本次先讲系统和实验的叙事。
**Rule**: ENPIRE 章页脚使用作者、论文题目、arXiv 编号、年份和 Figure/Section；官网视频写明 project website，自绘图注明 adapted schematic。细节与限制留在讲稿和来源记录。Learned-policy 四视频页移至定量结果之后、Limitations/RSI 之前（当前 P33），其余官网方法顺序保留；同步讲稿过渡及页码，不改媒体字节或页面主体。

## 2026-09-16 — Takeaways 回看关键框图并落到具体开放问题
**Context**: 用户要求重做 P36，并删除 P35 的 Open test 文案。
**Mistake**: 结尾沿用 Role / Artifact / Evidence 和抽象标语，未直接回扣 Control 的职责迁移与能力边界，也没有以用户关心的具体问题收束。
**Rule**: P36 用三条简洁路径：Control → P6/P17 缩略 → Latency? / Better interface?；Data → Sim2Real?；Improvement → Efficiency?。缩略必须对应真实页面内容，不重写为不同结论。删除指定的 Different artifacts / Re-test 标语及 P35 Open test 行；其余页面和右侧讲稿行为不变，同步中文讲稿。

## 2026-09-16 — Takeaways 用统一 SVG 语法，不拼接截图
**Context**: 用户指出 P36 太丑，要求最左侧补 Agent、纯 SVG、字号一致。
**Mistake**: P36 将两张整页截图缩到细小尺寸，并混用大号问题与不同字号角色标签，视觉层级和线条风格割裂。
**Rule**: P36 从一个 Agent 分三路；用原生 SVG 重绘 P6/P17 的关键概念，不再嵌缩略截图。正文统一字号，用同一线宽、配色、节点和对齐规范表达层次；保留 Control 的 Latency / Better interface、Data 的 Sim2Real、Improvement 的 Efficiency 问题。
