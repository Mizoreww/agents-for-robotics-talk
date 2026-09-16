# RSI 与 Agent-for-post-training：讨论备忘

日期：2026-09-14。范围：只读研究，**尚未改动讲稿或演示文稿**。对照的是最新 28 页讲稿第 20–26 页；现稿已经包含 ENPIRE、ASPIRE 和 Robot RSI，不能把它们再当作全新发现。

## 1. 先给结论

值得改的不是“把 RSI 塞进第三章”，而是**把第三章的问题提升为：机器人一次交互得到的经验，如何成为下一次可以复用的能力？** 这里的可复用能力可以是 policy weights、可执行 code，也可以是经过验证的 repair knowledge / skill library。三者都可能变好，但不是同一种 post-training。

建议只用三个候选解释这个问题：**ENPIRE（真实实验→policy/训练程序）、ASPIRE（失败诊断→可迁移修复知识）、RoboRSI（在线探索→技能固化与策略训练）**。仍可只深入 ENPIRE，另外两者各承担一个机制对照，不增加三篇同等深度的综述。

RSI 若指 **Recursive Self-Improvement**，应在演讲里明确约定，而不要说这是三项工作的共同官方方法名。本次核查的 ENPIRE/ASPIRE 论文并未以 RSI 定义统一范式；RoboRSI 官方报告使用 robot self-evolution / self-improvement，但没有展开 RSI 的三个词。RoboRISE 的仓库标题确实写了 “recursive self-improvement”，不过目前只有两行 README，没有论文、方法或结果，不能作为实证标杆。[S1–S5]

更强意义的 recursive improvement 是“改进后的系统又更擅长改进自己”。上述机器人研究更充分证明的是有限任务/环境中的持续策略或技能改进，**尚不足以证明持续加速、自主提升研究能力或开放世界无限自进化**。可以把 RSI 作为研究愿景，具体证据仍按更新对象和验证协议讲。

## 2. 三个候选分别改变什么

| 工作 | Agent 从什么得到反馈 | 跨 rollout 留下什么 | 不是在证明什么 |
|---|---|---|---|
| ENPIRE | 真实 trial 的 reward、trajectory、video、log | heuristic policy code；BC/RL 等训练程序；训练得到的 neural policy；经验文档 | 不是 general LLM 自身 weight update；不是任意环境中无人搭建基础设施 |
| ASPIRE | perception/planning/control primitive 的细粒度 multimodal trace | task program + 验证过的 repair knowledge（失败特征、适用条件、修复策略、可选 code sketch）；后续以 in-context guidance 使用 | 不是梯度训练 foundation model；不是只改一段代码；不是已解决 real-world lifelong learning |
| RoboRSI | 分层 task/skill 执行链、log/video、simulator verdict | 新增/修改的 base/atomic/compound skill code；技能/任务知识；可选训练得到的 learning policy | 不是 95/120 frozen-policy SR；不是已验证的 GPT-6 native vs code vs learned policy 全面对照 |

## 3. ENPIRE：从“会执行”到“会组织真实试验”

**机制（paper-stated + code-confirmed contract）**：human-assisted environment construction 先建立 safety、reset、verification；之后固定 environment contract，Agent 提出可证伪 hypothesis，修改 policy 或 training code，执行真实 trial，分析证据，再保留通过 success/regression gate 的版本。Policy Improvement 可以是 heuristic、BC、online/offline RL，并非限定某一种学习算法。[S1, §2; C1]

**可用结果**：pin insertion 的目标包含 50 consecutive successful rollouts；从 1 到 8 个 agent-robot pairs，达到近乎完美 success 的 research wall-clock 由超过 1.5 h 减到约 40 min。每个 rollout 有固定的 8 次 retry，后续尝试可以依赖之前失败信息。因此不能说 99% one-shot precision，不能用独立 best-of-8 反推单次成功率。[S1, §3.2–3.3]

**边界**：部分 reset 从最难子阶段开始；初始环境搭建有人参与；更多机器人换来更快发现策略，但 token 成本增长更快、per-robot utilization 下降。跨任务经验迁移（pin→GPU insertion）是把总结加入下一任务指令，不是 general LLM weights 改了。[S1, §3.4, §4]

## 4. ASPIRE：现稿“修好的 skill 代码”说得偏窄

**确切依据**：§2.2 明确说 skill 是 compact in-context guidance，包含 failure signature、when-to-apply condition、repair strategy，必要时加 representative code sketch。对象涵盖 localization heuristic、perception prompt、grasp constraint、navigation recovery、motion primitive、scene understanding 和 debugging workflow。§2.3 搜索的直接对象是可执行 program，但被沉淀到共享 library 的是可迁移修复模式；两者不要混为一谈。[S2]

**代码确认**：官方 pinned workflow 在 LIBERO-90 按任务块收集 `findings.md`，由 coordinator 更新 `.claude/libero/skills/*.md`，commit/tag 成为 skill-library snapshot；独立 transfer eval 从 frozen library 生成一个 program，不能修改 skill，也没有额外 debug loop。[C2] 这支持“learned external knowledge + executable artifacts”，不支持“所有学习都是 weights”。

**最有说服力的积累实验**：library 从 0/25/50/90 个 LIBERO-90 source tasks 增长，然后在 held-out LIBERO-Pro Long 生成 program。每个 target task 不再 debug/retry/update library；满库在 Pos/Task 两轴分别 23%/38%，论文约写为 31%。每轴 10 tasks × 50 held-out seeds，macro-average。比 headline 最大增幅更适合支撑“过去经验帮助新任务”。[S2, §3.5, Fig.5, App.C]

**真机只算初步 transfer**：三种 Franka-sim 学到的 skill，给不同 embodiment 的 bimanual YAM 作为 guidance；真机仍须 debug/adapt，并非直接部署 simulation policy。bowl 20/20→20/20（total tokens 8.65M→5.11M）；can 13/20→19/20（61.94M→6.58M）；drawer 无 skill 的 budget 耗尽、未得到成功 eval program，表列 0/20，对照有 skill 为 11/20（334.917M→81.67M）。tokens 测到首次成功 program 或 budget 耗尽，不能当部署 action latency。[S2, §3.6, Table 1]

**局限是作者自己写的**：frozen frontier LLM、固定 perception/planning/control API、memory stale/redundant 问题、昂贵 debug/search，且未形成 fully autonomous real-world lifelong learner。[S2, §5]

**讨论用替代句，不是已改稿**：ASPIRE 把失败中的修复经验整理成可迁移的 skill knowledge，再用这些经验指导下一次 program synthesis；真正留下来的既有可执行程序，也有如何判断和修复问题的知识。

## 5. RoboRSI：最适合把第一章和第三章接起来的新例子

官方是 **Noematrix Team 的 September 2026 research blog / open-source project**，不是本次已核验的同行评审论文。`research-preview` 链接现在转到正式报告地址。[S3]

**作者流程**：

```text
Task + observation + released skills
               ↓
Manager → Planner → Engineer → Reviewer
               ↓
层级 skill 执行 → trace / video / outcome
               ↓
诊断责任节点 + 提炼成功路径
               ↓
       validation / no-regression gate
          ↙                    ↘
parameterized code skill     rollout data → learning policy
          ↘                    ↙
       发布为下一轮可调用的能力
               ↖───────────────┘
```

这不是必须依次走“direct action→code→policy”的单一路线，而是**把有效交互压缩成更便宜、可复用的执行形式**：重复流程可固化 code，连续控制可训练 policy，陌生情况/失败再回到在线 reasoning。这里的“压缩/可塑性与效率”是本备忘的机制综合，不是作者已经证明的通用定律。

**代码确认的实现边界**：`compound_proposal.py` 从成功历史鼓励 Planner 提交 `SKILL.md + policy.py`，排入 review；已固化 compound 用 public base-skill dispatcher，不能任意引入未暴露能力。`pi0_finetune/policy.py` 是真正的 `lerobot-train` subprocess wrapper，可配置 ACT / diffusion / pi0-family；仅有 wrapper 不证明所有类型均已完成实验。`docs/skill-taxonomy.md` 描述训练后 eval 达阈值才切 active executor（示例 0.70）。[C3]

**博客与 pinned docs 有版本差异**：博客 TSR 当前讲 Task Family / Compound Skill / Atomic Task / Base Skill 四层；pinned taxonomy 文档仍强调 base / atomic / long_horizon 三层目录。可讲“hierarchical skill tree”，不要把四层概念图和三层文件结构说成完全一致。

### 真正有结果的部分

1. **Code consolidation 对照**：120 tasks × 5 initial layouts，每组 600 episodes；相同 Base Skills，Code-off 129/600 (21.5%)，Code-on 174/600 (29.0%)，+7.5 percentage points。118-task matched efficiency panel：median tokens −29.4%，VLM calls −27.2%，wall time −17.0%。这是复用已固化 compound 的证据，**不是 GPT-6 numeric direct actions 对 code 的比较**；Code-off 本身仍在线调用 base skills。[S3, §03.C; pinned README]
2. **跨版本 adaptive coverage**：LIBERO 的 95/120 是 evolving releases 中至少成功过一次的 task coverage；LIBERO-PRO 80/120 来自 5 个 adaptive releases，43/120 的起点本身也是多个 runs 的 closure。不能当 frozen-policy score，不能与别人的单次 episode success rate 排榜。RoboTwin 9/50→36/50 也以累计任务覆盖报告。[S3; C3 Evaluation historical boundary]
3. **固定 vs adaptive 扰动修复**：840 = 7 categories × 120 instances；fixed 261/840，adaptive Pass@2 398/840。这个差值同时含额外尝试与适应，不能解释为同预算 fixed-policy robustness 提升。[S3, §03.E]
4. **Learning policy 仅一个可见闭环案例**：官网 evidence JSON 明确命名 ACT corrective transport，`libero_spatial_swap/0`、seed 3。一条 304-frame corrective trajectory，8 training sequences 共 2,432 samples，1,000-step fine-tune；图示为 `code grasp → learned transport → code place`，保留 trace 为 `code_backed_grasp → act_transport (304/304 steps) → code_backed_place → final_simulator_verdict`，同任务、同初态下成功。不是 2,432 条独立轨迹，不能用一个成功案例推出跨任务泛化或全面优于代码控制。[S3, §03.D and original training figure]
5. **真机 mobile manipulation 是可追 trace 的 demo**：floor cleanup 在场景变化前后两轮 search/navigation/grasp/transport/place；官方仍保留 necessary safety supervision / course adjustment。没有本次找到的完整真机 trial denominator；不采纳其“first deployment”或“generalizable from scratch”作为已独立证实结论。[S3, §02.B, §03.A]

### 目前未能证明的部分

- 没有核验到 **GPT-6 native q/EEF output vs code vs trained policy** 的统一模型、同任务、同预算三路对照；不能借此回答哪一路普遍更强。
- 未从一手报告中确认历史 Code-on/off 使用 GPT-6。当前 reproduction 文档的 `gpt-5.6-sol` alias 示例不等于历史结果的模型披露。
- 官网正文和原图称 learning-based policy，配套公开 evidence JSON 明确命名 **ACT corrective transport**，因此可以按作者披露说 ACT；不能改称 RL。该单一案例有 fine-tune loss/数据 lineage 和成功 trace，未提供本文独立复现，不能从它推出 RL 或任意 VLA 训练已经普遍有效。
- 框架支持 data→weights，但高质量、大规模、多任务持续训练及 held-out transfer、忘却率、真实接触安全/恢复的系统验证尚未由本次来源建立。

## 6. 建议讨论的主线（未采纳、未改稿）

第一章不要落在“LLM 必须用 tools”。它问的是 **foundation model 能直接承担多少 control responsibility？在什么任务/反馈/延迟条件下，哪个 action representation 最合适？**

第三章顺势问：**当 Agent 已经能通过交互找到做法，我们要不要让它下次还花相同 token 一步步想？能否把这次经验保存为更快的 code、更可靠的 policy 或更可迁移的 skill knowledge？** ENPIRE 用真实实验改善策略，ASPIRE 验证知识跨任务复用，RoboRSI 给出从在线探索到 code/policy consolidation 的直观框架。

这两章共同的 open question 是：**在给定 base model 与资源预算下，能力应该放在 model weights、在线 reasoning、code/skill library，还是几者混合？** 直接控制能力增强不自动取消工具/技能的效率价值；工具有用也不意味着 foundation model 天生不能控制。

## Sources / 证据定位

- **S1 ENPIRE paper**：[arXiv 2606.19980v1](https://arxiv.org/html/2606.19980v1)，§2、§3.2–3.6、§4；复用本项目 `research/sources/enpire_paper.{html,txt}`，本次核实 current abs 仍只有 v1。
- **S2 ASPIRE paper**：[arXiv 2607.00272v1](https://arxiv.org/html/2607.00272v1)，§2.2–2.3、§3.3/3.5/3.6、§5、App.C；复用本项目全文，本次核实仍只有 v1。
- **S3 RoboRSI official report**：[Noematrix](https://lab.noematrix.ai/blog/2-roborsi/)，§02.C、§03.C–03.E；研究快照 `research/sources/rsi_20260914_roborsi_report.{html,txt}`；original training figure 快照 `rsi_20260914_roborsi_training_svg.txt`；[official evidence JSON](https://lab.noematrix.ai/assets/roborsi/evidence/simulation-showcase-v1.json) 的 `act_showcase[0]` 确认 ACT、seed、工具调用序列；`libero-task-iteration-v1.json` 明确 95 个 first-success records 来自 releases r82–r146。
- **S4 RoboRISE placeholder**：[pinned README](https://github.com/lixuan27/roborise/blob/0169b60b361e680d76456675e43dd74e67e7abba/README.md)，只有标题，明确证据缺失，不纳入标杆。
- **S5 Recursive improvement 的非机器人背景**：[Darwin Gödel Machine, §1 and §3](https://arxiv.org/html/2505.22954v1) 与 [Sakana official article](https://sakana.ai/dgm/)。这里只支持系统修改自身代码并用结果验证的概念区别，不把 coding benchmark 当机器人证据。
- **C1 ENPIRE code**：`NVlabs/ENPIRE@99ee90acf65b5b18957c8382ad580db999528be3`，[autoresearch contract](https://github.com/NVlabs/ENPIRE/blob/99ee90acf65b5b18957c8382ad580db999528be3/enpire/policy/autoresearch_instruction.md)。
- **C2 ASPIRE code**：`NVlabs/ASPIRE@f4c8939aab0af9b97690c561bd80e282940f7886`，[library build workflow](https://github.com/NVlabs/ASPIRE/blob/f4c8939aab0af9b97690c561bd80e282940f7886/aspire/sim/.claude/libero/zeroshot-transfer/main-agent-prompt.md#L178)，[frozen library eval](https://github.com/NVlabs/ASPIRE/blob/f4c8939aab0af9b97690c561bd80e282940f7886/aspire/sim/.claude/libero/library-size-scaling/main-agent-prompt.md#L32)。
- **C3 RoboRSI code**：`nssmd/RoboRSI@ae2bc840f02ff85ca18eac9766bfeeb0f0a381cf`，[frozen evaluation and historical boundary](https://github.com/nssmd/RoboRSI/blob/ae2bc840f02ff85ca18eac9766bfeeb0f0a381cf/docs/EVALUATION.md)，[compound proposal](https://github.com/nssmd/RoboRSI/blob/ae2bc840f02ff85ca18eac9766bfeeb0f0a381cf/roborsi/agents/compound_proposal.py)，[training wrapper](https://github.com/nssmd/RoboRSI/blob/ae2bc840f02ff85ca18eac9766bfeeb0f0a381cf/roborsi/embodied/skills/_lib/training/pi0_finetune/policy.py)。

完整有界检索、全部命中与错误：[search report](sources/rsi_20260914_search/allinone.md)。只读静态核查，不运行模型、simulation 或实验；public code 的存在与流程检查不等于复现通过。
