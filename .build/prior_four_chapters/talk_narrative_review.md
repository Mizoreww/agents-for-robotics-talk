# 演讲逻辑与证据审核

审核对象：26 页 HTML 与同步中文讲稿。2026-09-11。

## 主线与章节职责

总问题是“Agent 调用什么工具，产生什么结果，用什么证据判断它有用”。再追问哪些产物能够保留并帮助后续工作。不是按模型发布时间或论文数量串联，也不要求每个例子都更新模型权重。

| 部分 | 提出的问题 | 对应证据 | 收束与过渡 |
|---|---|---|---|
| 开场 1–4 | Agent 与现有 robotics tools 如何合作？ | Painting demo 提供直觉，但不作为 weight update 证据 | 三个核心角色与更广应用，明确不是强制流水线 |
| Execution 5–11 | 哪些接口让 Agent 复用既有能力，各自代价是什么？ | Direct/code control → Claude model/interface 图 → familiar LIBERO-40 → 真实 demo 与局限 → RPent 原图和工具例子 | 第 5 页直接动作/多工具分支图导读；第 10 页 strengths/gaps，第 11 页 RPent 收束，再引出 simulator |
| World building 12–16 | 重建一段交互能支持哪些用途？ | 原流程图、DROID-100 全分母与 acceptance rule、独立失败 demo | 第 12 页流程图导读；第 16 页收束 replay 与 prediction 的区别，过渡到真实反馈 |
| Improvement 17–22 | 真实实验能否支持 policy improvement？ | Environment、reset/verifier、pin 曲线、token/time scaling | 第 17 页固定 API 反馈图导读；第 22 页总结，保留 reset/retry 边界 |
| Other applications 23–25 | Agent 还能参与哪些工程工作？ | Hand structural design、ASPIRE trace demo | 第 23 页 artifact/validation 图导读；第 25 页小结，不引入第四个细讲工作 |
| Conclusion 26 | 如何评价这些不同产物？ | 回看四章，不添加新实验或主张 | 回扣工具、结果、证据与可保留成果 |

## 修正点

- 四章流程图均位于章节第一张（第 5、12、17、23 页），先明确角色和反馈，再讲案例；章末由简短讲稿收束。
- 第一章不再简化为 Agent → 单个 Controller。直接 q / EEF Pose 分支仍接到底层 servo/controller；Action tools 分为 IK / motion planner、controller code、VLA / learned policy、WAM；perception/state tools 位于 observation 反馈路径。工具可选择、可组合，不是强制串行。
- 先解释接口优势，再看具体证据和限制；IK / WAM 是扩展例子，不伪装成 Claude Plays Robotics 的评测组。VLA proposal 先经 Agent accept/edit/replace，再到 robot。
- RPent 放到本章最后，仅用一页原图与示意工具序列解释封装方式；ROSA / ROS-MCP 点到为止，不增加论文清单。
- 明确“execution 难题 → 模拟试验动机”与“replay 无法自动证明预测 → 直接真实反馈路线”两次过渡。
- Hand / ASPIRE 单列第四章 Other Applications，分别对应结构设计与程序调试；分类可以交叠，并非前三章之外的互斥集合。
- 补充 Claude 总图的读法：按 model 排列，颜色分 interface，纵轴为汇总 embodiment score，不能当作单一任务成功率。
- 资源页标题改为 Faster Research, Higher Token Use，避免把 token consumption 扩大成未测量的总成本结论。
- 讲稿使用自然中文，专有名词保留英文；区分正文与播放/指图提示。
- 流程图讲稿改为章节导读，删去“接下来用图收束”的旧过渡；case、视频、原图和时间预算随页序同步移动，共 26 页、60 分钟。

## 关键证据口径

- Claude direct manipulation 的 0–5.5% 为完整任务成功；部分 locomotion 暂停 simulation，不是实时物理控制证据。VLA 图仅为 familiar LIBERO-40。可能的 harmful-intervention 原因标为解释，非逐项因果实验证明。
- Robocurve 是独立来源。Astra 的 19/20 与 2/20 不与 LIBERO 分母混用。小样本、rig 差别、人工 reset、非盲法与非交错实验限制均保留。
- DROID-100：48 accepted / 8 partial / 44 failed。最多五个 candidate、三个 judges、任一 judge 的最佳分数 ≥8/10 即通过。不是 majority voting；cost 仅 model usage。
- ENPIRE：human-assisted setup 后固定环境 API。最多八次 conditional retry，不等于 one-shot precision 或 i.i.d. best-of-eight；部分 reset 从 hard subphase 开始。Research time 与 policy latency 分开。
- Microphone 明确为 dynamics failure 后 kinematic replay；hand 明确为不能直接物理工作的 design artifact；painting 没有 model-weight update 证据。
- RPent 代表可组合的工具框架，不是新的 VLA backbone。`pi0_pick` / `move_to` / `rotate_wrist` / `view_env_state` 是固定代码版本中的接口；`move_to` 是 OSC。示例不是新执行的实验。原图中的 DreamZero/WAM 与硬件范围不等于已确认集成，memory 文件更新不等于 foundation-model weight update。

## 复核来源

复用项目内完整原始来源快照，不依赖新检索摘要：
- `research/sources/claude_robotics.txt`：low-level control、VLA supervision、evaluation protocol。
- `research/sources/agentic_real2sim_paper.txt`：§4.1 acceptance、§4.2 DROID-100、§4.3 backend/cost。
- `research/sources/enpire_paper.txt`：§2 environment/API、§3 retry/scaling、§4 resource discussion。
- `research/sources/x_*_snapshot.txt` 与已有 media metadata：作者披露与 demo 归属。
- `research/interface_application_revision.md`：RPent 固定版本、具体工具与架构支持边界；DreamZero、ROSA 和 ROS-MCP 的官方来源。

## 演讲节奏

26 页的分配合计 60 分钟，包含约 6.3 分钟原始剪辑、读图和短互动。新增工具生态与第四章导读后，缩短部分既有读图停顿，不增加总时长。播放可与解释部分重叠。时长是彩排目标，不宣称单纯朗读正文恰好需要 60 分钟。若需要压缩，优先缩短 demo 后的互动和读图停顿，而不是删除关键实验条件。


## 本次叙事边界

- 先具体看 direct action 的局部进步、完整任务失败与 timing，再讨论同一个模型怎样通过不同 interface 得到支持；避免一开始就变成工具包介绍。
- 第 7 页明确 foundation model 与 interface 是两条改进轴。原报告低层能力的代际进步不均匀，不能写成“更强模型在每项直接控制任务上必胜”。Cursor / compass 是改善同模型效果的例子；更多输入和更多工具并不自动更好。
- 第 10 页把语义目标、任务拆解、工具复用与连续接触执行分开。Long-horizon planning potential 不等于长程机器人执行已可靠；熟悉任务上的 VLA 优势也不推广为所有生成式模型上的定理。
- Contact-state estimation / correction 是对瓶颈的合理分析，不伪称报告完成了独立的“接触理解”因果测量。
- 第 11 页 RPent 提供工程组织方式，不宣称已解决这些限制。结尾再转向通过 simulator 降低真机试错成本。
