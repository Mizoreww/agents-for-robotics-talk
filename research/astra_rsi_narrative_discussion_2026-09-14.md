# Astra、直接控制与 Robot RSI：主线讨论稿

日期：2026-09-14。用途：讨论演讲主线，不是新讲稿；未修改 slides、讲稿或生成 HTML。

## 结论先行

- 应调整叙事重心：从“通用模型控制不好，所以需要调用工具”改为“通用模型正在获得直接行动能力；哪些决策留在模型里、哪些交给外部技能，是随模型、任务与成本变化的设计问题”。
- 不应把 Claude Plays Robotics 的具体实验宣布为错误。该报告明确研究代际改进和 interface 条件；过度外推发生在我们把这些条件性结果串成长期能力分工的时候。
- 新 demo 足以促使我们重新提问，也可反驳绝对的“不可能”；它们本身不足以证明可靠性、普遍优于专用 policy，或确定能力增长的训练原因。
- “Astra 使用海量机器人数据预训练，因此直接控制进步”目前保留为待查证的因果假设；本轮可访问资料未给出足以核实的数据规模和训练消融。不要反向声称它没有使用机器人数据。

## 1. 核对的是哪一版

完整阅读 `output/Speaker_Script_Revised.md` 的 28 页正文，并核对 `.build/script_revised.md` 页标题与当前产物身份。

- 当前 HTML SHA-256：`1f42a44b6f8875fab7fa800096a9bd94a9a999f539ccdef1c9c8b7ca986b5b5b`，与项目记录一致。
- 独立讲稿 SHA-256：`eecaf4b44f6f0e932945e6edcdb244e5964e0cf0e9a95e6a854c1143e9319d1e`。
- `.build/script_revised.md` SHA-256：`96f74e773c09ff5de67f33f7308c06aabd079cd7d11372e5319d31a5709f4526`。
- 本轮未重新执行 UI/media audits；这里仅核对内容和身份，不声称新增验收。

### 目前叙事的偏向

| 位置 | 现有讲法 | 应讨论的变化 |
|---|---|---|
| 01、03 | 开场即强调 general-purpose Agent 和现有工具合作；核心问题是接哪些工具 | 将“模型本身能决定多少动作”放到同等甚至更靠前的位置，不能预设答案是外包 |
| 06–08 | 先讲旧 direct-control 失败，再展示 interface / VLA 提供能力 | 保留为历史条件和实验设计，不作为所有当前模型的能力上限 |
| 10 | 将新真机 demo 总结为规划工具组合，且称“接触要求不高” | 新增插入等案例已使这句概括过窄；逐例写明接口和证据，不从几个案例概括整类模型 |
| 12–13 | “Show-Harness 与 RPent 是同一条路线的两种实现” | 它们都重视 interface，但 Show-Harness 让 VLM 选择细粒度动作；RPent 可委托完整 learned/code skills。这一差别恰好是研究问题 |
| 14 | 借旧模型 0.2–0.4 Hz 解释 Astra demo 的延迟；泛称 generative policy 更适合精细操作 | 不把旧调用频率当作 Astra 实测频率，不把加速视频当作精确 latency decomposition；所有优劣限定到匹配的模型/任务/预算 |
| 26 | Robot RSI 只在 ASPIRE 页提一句社媒概括 | 若采用 RSI 主线，应在第三章开场解释改进循环，再用 ENPIRE、ASPIRE、RoboRSI 分别说明实现与证据 |
| 28 | 最终仍收束为调用哪些工具、产生什么结果 | 增加“哪些能力已在 foundation model 中、哪些通过经验保留下来”，不只问工具组合 |

这些是待讨论的编辑建议，没有执行改稿。

## 2. “Direct”不能按是否出现 API 来划分

本讨论采用“谁决定任务相关动作”而不是“软件调用了几个函数”的区分。这是本报告的分析框架，不是新的公认 taxonomy。

| 路径 | 模型主要决定什么 | 下游主要承担什么 |
|---|---|---|
| Numeric action：q / EEF Pose / delta action | 下一步机器人目标或动作 | servo、IK/OSC、限幅和执行映射 |
| Semantic micro-actions | 每一步方向、步长选择或夹爪开合 | 将动作单元确定性映射为局部运动；Show-Harness 属此类 |
| Generated controller code | 在开发/交互过程中生成控制程序 | 程序在后续执行时处理反馈、输出动作；不等于 LLM 每一 servo tick 推理 |
| Learned / scripted skill delegation | 选择目标、子任务或技能 | VLA 或封装 skill 决定一段复杂行为；RPent 可以组织此类调用 |

Direct pose output 仍需一个执行 API，并不因此变成“VLA 帮它完成了抓取”。反过来，调用 `GRASP` 也要看实现：在 Show-Harness 中它主要对应夹爪关闭，不等于一个完整的 `pick(object)` skill。

Interface design 与直接控制不对立：更好的 observation、坐标约定、action representation 和 feedback 可以帮助模型自己做细粒度动作选择，而非把决策交出去。

## 3. Awesome-Astra 新材料具体改变什么

读取 [Awesome-Astra-Embodied-AI](https://github.com/zjwzcx/Awesome-Astra-Embodied-AI) 的固定 revision `a22a671bf68c29d05fa22e3a77b2352fc8eccd1d`。当前有 32 个条目，不等于 32 个独立研究或互不重复的实验。分类中混合了 numeric/trajectory output、code generation、SONIC 等 learned controller、policy calls 与建模/训练工作。

### A. Robocurve：有限但有完整分母的直接 EEF 控制证据

[原始评测](https://openai.robocurve.org/gpt-6-astra/) 给模型三视角和 proprioception，模型请求 absolute EEF poses，由机器人 IK 转成 joint angles。每次最多 20 次 model call，speed cap 25%。

- Bowl placement：Astra 19/20，Fable 5.1 8/20；平均每次约 2.5 vs 6.8 min。
- Puzzle insertion：两者均 2/20。
- Bowl 并非同一 rig，实验非交错，人工 reset、非盲评分；不能把差异全部归因于某种训练数据或唯一模型能力。

结论：确有直接目标控制能力的显著进展；进展不均匀。保留 insertion 失败，但不要把这个设置的失败宣布为所有接触任务的不可能。

### B. GPT-Policy-Eval：当前稿中缺少的接触任务反例

[官方仓库](https://github.com/cheng-haha/GPT-Policy-Eval)，revision `43929f0ee3673da67393fcbe85d43c58eb15db59`。

作者展示 one-video-demonstration 的真实 plug insertion，明确标为 No VLA / No WAM / No RL / No DAgger；还展示 hidden goal 与 goal-image arrangement。

但作者同时明确：selected individual trials、加速播放、broader evaluation ongoing。插入为 12×，另外两个为 8×/24×。当前 tree 只有 README 和媒体，code release 尚在计划中；因此 exact action API、controller、接触反馈、人工介入、选择过程和成功分母不能从代码核验。

应当用它打开问题：“模型能否基于视觉示范和反馈完成接触任务？”不应写成“已证明端到端无任何控制工具”“已可靠解决插入”或用它推翻另一个装置的 2/20。

### C. Show-Harness：现有素材本身支持更开放的解释

[全文](https://arxiv.org/html/2609.10522v1)，尤其 §§3.1–3.4、5.3、5.4.3–5.4.4、Appendix 7.4；[官方代码](https://github.com/showlab/Show-Harness)，revision `137d5718c3b7af0150764d8f9beeb252c9f2794a`。

- 论文直接强调 VLM remains responsible for fine-grained physical decisions；不必把它讲成“VLM 只规划，VLA 负责动作”。
- `core/action_units.py`、`core/vlm/roles.py`、`interpreters/franka_atomic_controller.py` 和 `interpreters/real_atomic_controller.py` 的只读检查确认 action-unit 输出到 Cartesian setpoint 的路径。
- §5.4.4 固定其余 harness，只改变 action representation / conventions，支持 interface 与模型能力共同决定结果。不能因此推出更高层 skill delegation 永远最好。
- §5.3.1 包含 stacking / peg insertion，以及缩小 step size 的实验；§6 仍说明尚未覆盖 dexterous/humanoid 和丰富触觉/力反馈。
- §5.3.2 的 visual in-context learning 与 §4 的 GUMI 数据采集，可连接“先会行动，再积累训练材料”。

没有运行其代码或模型；这里只核验接口实现，不是复现实验。Show-Harness 仍可保持 supporting example，无需增加第四篇深讲论文。

## 4. 训练原因与模型标签

[当前 OpenAI model documentation](https://developers.openai.com/api/docs/models/gpt-6-astra) 和 [model guide](https://developers.openai.com/api/docs/guides/latest-model) 已实际获取，未披露机器人预训练规模或相关消融。原始 announcement URL `https://openai.com/index/gpt-6-astra/` 在本次直接请求中返回 HTTP 403，未获得正文；因此不能声称已全面审计所有官方训练披露。

需要拆开三句话：

1. 多模态基础模型可以学习 action generation——有既有 VLA 文献与当前接口实验支持。
2. Astra 在某些 robot-control 条件下明显强于过去模型——有 Robocurve 及近期定性案例支持，仍受协议约束。
3. 这个增长主要由“海量机器人数据预训练”导致——本轮材料不足以确证，尚需开发者披露或受控消融。

可作概念参照的 [VLA-0](https://arxiv.org/html/2510.13054v1) 直接用 VLM native vocabulary 生成数值 action strings，通过机器人示范训练，并没有额外 generative action head。这里只用其已读摘要/方法来说明“文字生成模型”与“action policy”并非本体上互斥；不将它用作 Astra 训练来源的证据，也不把 zero architectural modification 写成 zero training。

“LLM vs generative model”也不是严格对立：LLM 本身是生成模型。实际应比较 action representation、训练数据、推理架构、闭环频率、成功率与总体成本。

## 5. RSI：新材料与第三章的实际变化

详细证据见 [RSI 讨论备忘](rsi_discussion_2026-09-14.md)，完整检索结果和连接错误见 [检索报告](sources/rsi_20260914_search/allinone.md)。

最贴近用户这次问题的新项目是 [Noematrix RoboRSI](https://lab.noematrix.ai/blog/2-roborsi/)，官方 [代码](https://github.com/nssmd/RoboRSI) 固定于 `ae2bc840f02ff85ca18eac9766bfeeb0f0a381cf`。它是 September 2026 research report / project，不能写成已同行评审的统一范式。

本次核查的 RoboRSI 报告/README 使用 robot self-evolution / self-improvement，没有明确展开 RSI 为 Recursive Self-Improvement；ENPIRE、ASPIRE 也未共同定义该缩写。若演讲使用 Recursive Self-Improvement，应明示自己的概念约定，并区分“策略/技能经反馈改进”与更强的“系统改进了自身的改进能力”。后者的持续递归增强尚未由这些证据建立。

三种改进载体：

- **ENPIRE**：真实 trial → 修改 heuristic policy / training code 或训练 neural policy。固定 API、human-assisted setup、reset/verifier 与 conditional retry 都继续保留。
- **ASPIRE**：trace → failure attribution → program repair → validated skill knowledge。现稿只讲“修好的代码”过窄；§2.2 的实际 skill 包含 failure signature、适用条件、repair strategy 和可选 code sketch，后续以 in-context guidance 使用。Foundation LLM 是 frozen；有 held-out task 的 library-transfer 评测，不能简单等同于“只在当前 session 重试”。
- **RoboRSI**：在线探索与层级 skill 执行 → 验证 → 固化 parameterized code skill，或用 rollout data 训练 learning policy → 发布并在后续任务复用。不是每个任务必须依次经历 code 再变 policy。

RoboRSI 中最有信息量的证据不是 headline coverage，而是以下三项：

1. **Code consolidation 的对照**：同 Base Skills，120 tasks × 5 layouts，每组 600 episodes。Code-on 为 174/600（29.0%），Code-off 为 129/600（21.5%）；另有 118-task efficiency panel，median tokens 减少 29.4%。这证明的是该设置中代码固化的价值，不是“GPT-6 native action vs code”的实验；Code-off 仍调用基础技能。
2. **Learning policy 个例**：官网 [evidence JSON](https://lab.noematrix.ai/assets/roborsi/evidence/simulation-showcase-v1.json) 标为 ACT corrective transport：一条 304-frame 纠正轨迹产生 2,432 samples，1,000-step fine-tune，然后 code grasp → ACT transport → code place，在相同 task/initial condition 下成功。它是单例闭环，不是 RL、多任务泛化或 VLA 普遍优越的证明。
3. **指标边界**：95/120 是 evolving releases 的累计 task coverage，不是 fixed policy 的 episode success rate。不能加入跨论文成功率排行；真机部分也未找到完整 trial denominator。

最值得拿来讨论的机制问题：**Agent 既然已能交互找到一种做法，下次是否还应该付出同样的推理和试错成本？哪些经验放进 weights，哪些放进 code，哪些以可迁移知识保留？**

## 6. 建议讨论的全场主轴

推荐：**Foundation models 正在获得行动能力；下一步是把一次交互中的成功转化为可积累、可复用的机器人能力。**

保留现有三个工作对象，但改变每章问题：

1. **Act — 模型现在能自己决定多少动作？** 先用新 direct/visual-context 案例打开问题；再用 Claude Plays Robotics 的接口实验解释不同分工，用 Show-Harness说明“界面也能帮助直接动作”，最后让 RPent 代表一种可组合选择，而非预定终点。
2. **Build experience — 怎样获得更多有效物理经验？** 保留 Agentic Real2Sim；重点是创建可实验、可产出数据的环境，同时明确 replay 还不能替代 counterfactual physical validity。
3. **Improve — 怎样让这次的探索帮助下一次？** 将 Robot RSI 作为问题框架：经验进入代码、skill memory 或 policy weights；ENPIRE 保持深讲，其他案例只说明不同积累载体与证据。

这不是声称三篇工作已经连成一条端到端 pipeline。第二章提供的是潜在经验来源，第三章也可以直接在真机获得反馈；训练改进可能作用于外部 policy/skill，不一定更新 Astra 本体。

### 第一章可用的开场问题

> 当一个通用多模态模型已经能看示范、读 robot state，并自己决定末端怎么移动时，我们还应该把它仅仅放在 planner 的位置吗？

这只是讨论用问题，不是已写入讲稿的替换文本。

章首框图继续保留，但三个分支平等：模型直接输出 action、模型生成 controller code、模型调用现有 skills。它们共享 perception/feedback 和 execution stack；不要用视觉层级暗示越靠下/工具越多越先进。

### 两条可以共同成立的判断

- 随着模型、数据和训练方法改进，更多原来依赖手写抽象的任务相关决策，可能由模型自身承担。
- 即使模型会做，也可能因为速度、稳定性、成本和复用而把成熟行为编译为代码或训练成专用 policy；这时工具不是“LLM 永远不会动作”的证明。

后一条与 RSI 的关系尤其值得讨论：**探索可以慢而灵活，积累后的执行可以更快、更稳定；遇到失败再回到探索。** 这是建议的综合视角，需要逐项用具体项目支持，而非把它宣布为已完成的通用机器人系统。

## 7. 应保持开放的三个问题

1. **Scaling 移动的是哪条边界？** 更强模型究竟改善语义目标、空间定位、action precision、接触状态估计，还是在反馈中适应新 embodiment？不要把总成功率的变化全部叫作 reasoning 增强。
2. **同样资源下，什么分工最好？** 固定模型、任务、机器人、observation 和安全约束，比较 numeric action、semantic micro-actions、generated code、learned skill；记录成功率、first-attempt/recovery、wall time、模型调用/费用、人工介入。Interface 改变 action space 或 feedback 时必须明示，不能伪装成只换 prompt。
3. **RSI 究竟留下了什么？** 清空会话、换初态或相关任务之后，是否仍受益？是复用了 task-specific script，学到了可迁移 skill，还是只在同一次长会话中找到了一次解？Adaptive coverage、best-of-search 与 frozen-policy success rate 分开报告。

对于机器人数据预训练的因果问题，最有信息的额外证据是同族模型的数据/训练消融。闭源模型之间的胜负或社媒作者猜测都不能替代它。

## 8. 范围和交付边界

- 仍建议最多三篇 deep case，不因为新材料把 talk 扩成更多论文的罗列。
- 保留原字体、章首框图、章节总结、论文原图/视频与单文件内嵌 HTML 的交付原则。
- 未修改演示文稿或讲稿；用户讨论后再决定标杆比重、具体页序和 RSI 框图。
- 来源快照和固定 revision 见 `research/sources/astra_20260914/source_manifest.json`；检索时间是 2026-09-14，未来更新不能自动继承本轮结论。
