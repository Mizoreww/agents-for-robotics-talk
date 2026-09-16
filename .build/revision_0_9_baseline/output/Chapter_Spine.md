# Agents for Robotics — 章节主线

2026-09-14 · v0.8 · 28 页

**谁生成 action → 谁构建 simulator → 谁改进 policy。** 三章对应不同产物，不是一套已经端到端验证的系统。每章先看总框图，再看机制、实验及总结。Chinese script 保留 English 专有名词。

## 1. Control：分层边界是否应该重画？（4–13）

**问题**：Foundation model 应自己生成哪些 action，哪些仍值得交给工具或 learned policy？

### 背景与方法

1. **第 4 页，原总框图**：Agent 直接输出 q / EEF Pose，或调用 IK / planner、controller code、VLA、WAM；都保留低层控制和反馈。是接口全景，不是每项都经过同一个实验。
2. **第 5 页，三张原图**：[Hi Robot](https://www.pi.website/research/hirobot) 的 VLM → subtask language → π0 → action；[Helix](https://www.figure.ai/news/helix) 的 semantic latent；[Helix 02](https://www.figure.ai/news/helix-02) 明确 S2 → S1 joint targets → S0。Hi Robot 本身只描述 two-level inference，不能补造第三个网络。
3. **第 6–7 页，具体旧模型实验**：[Claude Plays Robotics](https://www.anthropic.com/research/claude-plays-robotics) 比较模型所处 interface，集中讲 manipulation，不展开所有 benchmark。
4. **第 8 页，工具组织**：[RPent](https://github.com/RLinf/RPent) 一张原 framework 图说明 memory、tools、action primitives 和统一接口；不是另一个性能排行榜。
5. **第 9–12 页，能力前提变化**：先看 Astra Direct 的真实行为和 community demos，再看同模型 interface 比较，最后看用户指定[匿名报告](https://anonymous-report-421.github.io/public-website/?lang=en&view=1)的原始 Direct/Hybrid 架构。

### 实验与边界

- **Claude / LIBERO-40**：40 tasks × 5 seeds。Opus 4.6 Direct 3.5%、MolmoAct + supervision 76%，MolmoAct alone 86%。Motor prior 帮助很大，但 Agent 干预未必改善已有 policy。两幅原图 y-axis 不同，不比柱高。
- **[Robocurve](https://openai.robocurve.org/gpt-6-astra/)**：Astra → absolute EEF → IK，无独立 VLA；bowl 19/20，precision insertion 2/20。支持部分任务直接能力强，也保留接触操作边界。
- **[Asim 同模型对比](https://asimfish.github.io/astra-control-dashboard/#sec3)**：Square 的 ΔEEF 1/20、waypoint 18/20、code 16/20。不是 joint q 对比；≤200/500/500 steps 与 10/16 queries、3 code revisions 不配平。Waypoint 平均 256.6 steps，已超过 delta 上限。不能把差距全部归因于 action representation。
- **匿名 Direct/Hybrid**：共享 3 views、14D proprio 等输入；π0.5 提出 50×14 joint candidate，Astra 接受 1–15 steps，或改为 EEF correction 1–5；Direct EEF 1–5。RoboDojo 10 selected tasks × 5 paired cases：13/50 vs 24/50。Prior、interface、horizon 同时改变，25 Hz 也不是 LLM 决策频率。

**第 10 页 demos**：plug 12×、keyboard 20×，selected trials，无整体成功率。用来讨论视觉反馈，不当 RL/weight update 证据。

**总结（13）**：常见分层有工程依据，但不是能力上限。更强的模型使 S2/S1 分工值得重测。Astra 的 robot-pretraining recipe 和 causal ablation 未披露，不能把“海量机器人预训练导致提高”写成已证事实。暂不比较 latency，也不能忽略控制/反馈预算。

**过渡**：从“已有世界里下一步怎么动”，转向“已有交互能留下什么模拟产物”。

## 2. Simulation：真实记录能变成可运行场景吗？（14–19）

代表：[Agentic Real2Sim](https://arxiv.org/html/2607.19190v3)。

**问题（14–15）**：手工建模、对齐坐标、调参数很费力。能否把同步真实交互记录转成 runnable simulation episode？Real/sim pair 先展示输入与输出。

**方法（16）**：Agent 选择对象、keyframe、mask 和 tracking repair；专门组件完成 segmentation、mesh/depth/pose 等计算。Meshed objects、scale、pose tracks、robot trajectory 和 camera metadata 进入 MuJoCo scene；后续是 deterministic sweep 或 LLM-assisted refinement。不是任意单 RGB 视频自动恢复物理世界，也不是每次修正都由 LLM 自由调参。

**实验（17）**：全部 100 DROID episodes 在分母。Gemma 4 31B 得到 **48 accepted、8 partial、44 failed**。最多 5 个 eligible candidates，3 judges；**任意 judge 的最佳分数 ≥8/10** 即通过，不是 majority vote。Model-call bill 不含所有 pipeline 成本。

**工作流 demos（18）**：Lingxiao 输入 multi-view RGB + actions，展示 real/sim replay；Office 展示 reference → Blender/USD → Newton/G1 的最终场景。两条流程来自作者说明，不能据视频声称已测物理预测或训练了新 locomotion policy。

**总结（19）**：得到的是可运行、可检查的 episode artifact。Matching replay 与改变 action/initial state 后的 predictive simulation，是两项不同验证。

**过渡**：Policy 改进也能直接使用真实实验。ENPIRE 不依赖先运行上面的 Real2Sim。

## 3. Improvement：反馈怎样变成下一版策略？（20–26）

代表：[ENPIRE](https://arxiv.org/html/2606.19980v1)。

**问题（20）**：临时纠正一次 action 不等于跨 trial 保留改进。如何让 Agent 反复修改 policy/code/training recipe 并检验结果？

**方法（21–22）**：Human-assisted environment construction 建立 safety、reset、success verification；随后固定 Gym APIs 和成功定义。Coding Agent 提出假设、修改程序、运行真实 rollout、分析反馈。Reset / verifier 两段原视频来自不同任务。

**具体修改（23）**：原 Figure 12 展示一次 team run 的 idea tree，包含无收益分支。I37 BC regularization +10.8 pp；I66 batch size 1024→512 +0.9 pp；I76 controller compensation +1.3 pp。是该 run 的 best-score 轨迹，不是独立随机消融的平均因果收益。

**实验（24）**：Pin insertion 的 1→8 agent–robot pairs 把 near-perfect success 的 research time 从 **>1.5 h 降到约 40 min**。Rollout 允许最多 8 次 conditional retries；不是 one-shot precision，也不是独立 best-of-eight。

**Astra demos（25）**：四足 CAD/RL 是 4 separate experts 的开发预览，保留 FULL EVAL NOT MET 与 Wave/Sit CUT，不说九种行为全部通过。Physical ICL 是已有 motion tools 下的 8× 定性展示，不是权重训练或持久技能验证。

**成本与总结（26）**：更多并行资源可以缩短 research time，但可能增加 tokens。固定可重复实验中的 policy self-improvement 已有具体结果；不等于改进者自身的 recursive enhancement。Setup、retry budget、verifier 可靠性和资源代价都属于结论。

## Beyond 与结束（27–28）

Tendon-hand 是 structural design / CAD animation，**不是验证过的物理手**。最后比较三种产物与各自验证，讨论新模型能力会怎样改变机器人工作的分工，不宣布旧论文作废或全部流程已被取代。

18 段 clips 合计约 6 分 47 秒。60 分钟为读图、视频和讨论的建议节奏，未彩排。完整稿见 `Speaker_Script_Revised.md`。
