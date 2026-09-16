# Agents for Robotics — 三章讲解提纲

2026-09-14 · v0.7 · 21 页

三章分别讨论 **控制动作、构建模拟场景、改进 policy**。它们不是一套系统已打通的三个模块，也不共用一个成功率指标。每章先看框图，再讲问题、方法、实验与总结。

## 1. Control：Direct 还是 Hybrid？（4–8 页）

代表工作：[GPT 6 Astra as an Embodied Policy](https://anonymous-report-421.github.io/public-website/?lang=en&view=1)，匿名 technical report。

**问题**：同一个 Astra Agent，直接生成动作，与借助 learned action prior，分别能做到什么？

**简短背景（第 5 页）**：
- [Claude Plays Robotics](https://www.anthropic.com/research/claude-plays-robotics)：区分 direct action、controller code、policy supervision 等控制分工。
- [RPent](https://github.com/RLinf/RPent)：把 motion、perception、code、learned policy 等能力组织成可组合服务。
- 当模型通过机器人数据训练获得新的能力，旧设置中的结论需要重新检验；这不代表旧实验作废，也不能据此断言 Astra 使用了何种未披露的训练配方。

**方法与架构**：
- 输入：3 个 RGB views、14D proprioception、instruction；Astra 还使用 history / notes。
- **Direct**：Astra 生成双臂 EEF position / orientation / gripper targets，执行 1–5 个 control steps 后重新观察。
- **Hybrid**：task-finetuned π0.5 生成 50×14 joint-space candidate；Astra 结合 observation、history 和 FK poses 审核，选择接受候选前缀（1–15 steps），**或**给出 EEF correction（1–5 steps）。
- EEF targets 仍通过 local IK 和 controller 执行。25 Hz 是 native control rate，不是 LLM 决策频率。第 4 页保留报告原架构图，可点击放大；它不是未公开的 Astra 内部网络结构。

**实验结果**：RoboDojo 的 10 个 selected tasks × 5 paired cases，共 50 cases / arm；Direct **13/50**，Hybrid **24/50**。两个视频是不同仿真任务的成功案例，并省略 LLM 等待时间。

**局限与总结**：Hybrid 在这组条件下完成更多 cases；但 action prior、生成接口和执行段长同时改变，不是纯 prior 消融。任务选择、端到端 latency 和总预算都限制外推。既不能推出“LLM 必须委托控制”，也不能推出“Direct 普遍替代 policy”。

**过渡**：第一章研究下一步怎么行动；第二章研究已经发生的真实交互能转化为什么。

## 2. Data：真实记录能变成可用 simulator 吗？（9–13 页）

代表工作：[Agentic Real2Sim](https://arxiv.org/html/2607.19190v3)。

**问题**：给定真实机器人交互记录，能否自动得到相应的、可运行的 simulation episode？

**方法与架构**：recording → perception / geometry → scene 和参数组装 → simulator replay → 与真实记录比较并修正。Agent 组织工具和中间产物；输出首先是场景与 replay，不是已经训练好的 policy。

**实验结果**：DROID-100 的全部 100 episodes 均保留在分母。最佳 backend Gemma 4 31B 得到 **48 accepted、8 partial、44 failure**。每个 episode 最多选 5 个 eligible candidates，由 3 个 VLM judges 评分；**任意一个 judge 的最佳 candidate ≥8/10** 即可通过，不是 majority vote。

**局限与总结**：结果支持为部分真实记录构建被接受的模拟回放；不等于物理参数准确率，也未由此证明对新 action / initial state 的预测能力。论文 model-call bill 不是包含 perception、simulation、preparation 的全部成本。

**过渡**：模拟不是改进 policy 的唯一反馈来源；第三章直接把真实机器人组织成实验环境，不要求先运行 Agentic Real2Sim。

## 3. Improvement：真实实验能改进 policy 吗？（14–19 页）

代表工作：[ENPIRE](https://arxiv.org/html/2606.19980v1)。

**问题**：能否让 coding Agent 反复修改策略、运行真实实验并检查结果，而不再由研究者手动组织每一轮？

**方法与架构**：human-assisted environment construction → 固定 action / safety / reset / verification APIs → Agent 修改 policy 或 training procedure → real rollout → verifier / logs → 下一轮修改。Improvement 期间环境与成功标准保持固定；foundation LLM 不必更新 weights。

**实验结果**：pin insertion 中，1→8 个 agent–robot pairs 将达到接近完美 success rate 的 research time 从 **超过 1.5 小时缩短到约 40 分钟**。指标采用允许 conditional retries 的 rollout protocol，最多 8 次 retry；增加并行资源可缩短 research time，但消耗更多 tokens。

**局限与总结**：这不是 one-shot insertion precision，也不是独立 best-of-eight。Human setup、reset / verifier 的可靠性、retry budget 和资源成本都是结论的一部分。它是具体的 policy self-improvement 实践，不等于已证明递归增强“改进者自身”的能力。

## 开场与结尾

- 第 2 页 painting demo 引出物理交互和反馈，仅作应用展示。
- 第 20 页 tendon-hand CAD demo 展示 structural design，**不是经过物理验证的机械手**。
- 第 21 页总结：Control、reconstruction 与 policy improvement 改变的对象不同，需要的验证也不同。

完整中文逐页讲稿见 `Speaker_Script_Revised.md`。60 分钟包含读图、视频、停顿与讨论，是建议安排，尚未彩排计时。
