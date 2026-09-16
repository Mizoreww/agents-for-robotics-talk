# Control 能力诊断：暂定讨论笔记

日期：**2026-09-14**（本机时钟确认）。范围：独立研究笔记；**没有修改 slides、builder 或中文讲稿**。

## 0. 原文章状态：未核验，不能冒充文章总结

用户指定：[微信链接](https://mp.weixin.qq.com/s/kxZrh-ihP4HN20w1RdieWA)。直接请求只得到环境验证页，没有文章标题、作者或正文；随后主线程浏览器对精确 URL 报告 site-safety block，并要求停止取得该文章及其镜像/间接副本。已停止相关获取，不绕过验证或安全限制。

因此，目前**不能确定文章的实际分类、分类定义或文内链接**。下文的 Semantic intent / Spatial grounding / Physical interaction 是根据用户提及的三个方向及现有一手证据，**由我们自行提出的 operational framing**，不是该微信文章的 taxonomy，也不是对其正文的重建。待用户提供可阅读正文后，才可逐项核对文章的观点与链接。

访问状态及材料排除记录：`research/sources/wechat_control_20260914/access_status.json`。前期公开索引结果没有用于认定文章身份或恢复正文；不能把那些搜索结果写作文章依据。

## 1. 建议把三个概念变成诊断问题，而不是三档能力等级

| 我们自拟的角度 | 可操作定义 | 该问什么 | 不能直接推断什么 |
|---|---|---|---|
| **Semantic intent** | 从指令、任务上下文及反馈中确定目标、目标对象、约束和下一步子目标 | “应该操作什么？要达到什么状态？哪些东西不能动？” | 目标说对了，不代表知道精确位姿，更不代表能完成接触 |
| **Spatial grounding** | 把目标对应到当前场景和机器人状态，包括位置/朝向、坐标系、自身位姿、可达关系，以及跨时刻状态记录 | “目标在哪里？相对哪个 frame？手现在在哪里？接下来怎样对齐？” | 看懂一张图或说对方位，不等于拥有稳定的 metric localization / state tracking |
| **Physical interaction** | 在执行中建立、维持和释放所需接触，并处理动力学、约束、时序、误差与恢复 | “接触以后会怎样？该用多大/多快的动作？怎样防滑、避碰或完成插入？” | 某个成功动作不证明通用的 physics understanding；失败也不能只归因于物理知识不足 |

这三个角度**互相耦合，不是互斥任务类别，也不是 System 2 / 1 / 0 的一一映射**。例如，插入失败可能来自目标 orientation 估计错误，也可能来自接触策略、缺少反馈或执行预算；仅看失败视频无法唯一归因。更稳妥的措辞是“哪一个环节限制了这个系统”，而不是“这个模型没有物理理解”。

System 2 / 1 / 0 描述的是一种**系统分工与时间尺度**；三种诊断角度描述的是**任务所需的信息与能力**。一个 learned VLA 可能同时承担语义、空间和局部交互，LLM 也可能直接承担动作生成。不能把 Semantic 固定给 LLM，把 Physical 永久固定给独立小模型。

## 2. 现有第一章证据怎样放进这个框架

下表只引用已核验的一手来源，**不声称它们在该微信文章中出现**。

| 来源与设置 | 与诊断角度的对应 | Action interface / 支持证据 | 解释边界 |
|---|---|---|---|
| **Hi Robot**：三种 real-world task domains；20 trials / task / method | 直接测了 Semantic intent 与任务进度，而非只看演示 | 高层 VLM 输出 language subtask，π0 执行。官方显示的平均 IA：Flat VLA 36%，GPT-4o high-level 30%，Hi Robot 76%；TP 分别44 / 64 / 81%。[官方图](https://www.pi.website/research/hirobot)，[v2 Fig.5、§5.2](https://arxiv.org/html/2502.19417v2#S5.F5) | IA 是单 trial 内正确指令比例，TP 是对象放置进度，均非 episode SR；主表也改变了训练数据。支持该训练方案的效果，不支持“LLM 永远必须调用 VLA” |
| **Claude Plays Robotics**：LIBERO visual-tool ablation，10 tasks × 5 seeds | Spatial grounding / action alignment 是可干预的瓶颈之一 | Cursor tool 下 Mythos Preview success **6% → 32%**（N=50 / condition）。报告还比较 direct、programmatic、policy、RL 四类接口。[报告 “Tools to aid perception” 及 Appendix](https://www.anthropic.com/research/claude-plays-robotics) | 这是特定模型、子集和工具条件；不能说所有物理失败都可被一个坐标提示修好。报告不同视觉工具、模型与任务的结果并非单调一致 |
| **RPent / Harness VLA**：LIBERO-Pro few-shot，8 cells × 100 episodes | Semantic retargeting 与 Spatial re-binding 不必全部压在同一个 frozen motor policy 上 | 同一 frozen π0.5-SFT：direct π_RLinf **50.0%**，Harness Codex **72.1%**、CC **82.4%**。T=instruction redirection，S=position swap。Analytic primitives 负责 staging，VLA_ACT 承担局部 learned interaction。[v4 Table 3](https://arxiv.org/html/2607.08448v4#S3.T3) | 加了 planner、memory、analytic control、retries，非等预算纯接口消融；seed 0 用于探索，1–10 评测。T / S 是扰动轴，不是对模型“语义智力/空间智力”的无混杂测量 |
| **Robocurve Astra**：真实双臂，两任务各20次 | 宽容 pick-and-place 与精细 insertion 不能合并成一个“已会操控”的标签 | 同类 absolute EEF + IK interface：bowl **19/20**，round puzzle insertion **2/20**。[一手报告](https://openai.robocurve.org/gpt-6-astra/) | 两任务并非严格只差 contact difficulty 的消融；不能排除 pose、sensing、controller、budget 等因素。跨模型 bowl 比较还跨 rig。它揭示剩余困难，不定位唯一原因 |
| **Asim Astra dashboard**：同 Astra、proprio 档、每格20 episodes | Interface 决定把哪部分空间几何、闭环 tracking、动作时序交给系统 | ΔEEF chunks / absolute waypoints / code→waypoints：Can **18/20 · 17/20 · 7/20**；Square **1/20 · 18/20 · 16/20**。[矩阵及 schema](https://asimfish.github.io/astra-control-dashboard/#sec3) | ΔEEF 不是 joint q。观测辅助、控制器、最大 steps / query budgets 不完全等同；Square waypoint 平均256.6 steps 超过 ΔEEF 的200步上限。不能把差值全部归因于表示法 |
| **匿名 Direct/Hybrid report**：RoboDojo paired 10 tasks × 5 cases；RoboLab retained slots | 分工可能随任务需求与动作先验适配性改变 | RoboDojo Direct EEF **13/50**，π0.5 candidate + Astra review/correction **24/50**。RoboLab final slots 为 **49/50、46/50**。[原报告](https://anonymous-report-421.github.io/public-website/?lang=en&view=1) | RoboDojo 同时改变 prior、action branch、segment length；RoboLab 有历史记录、retry 与不等预算。不能据此宣布 Direct 胜过 Hybrid，也不能用两个 suite 的绝对分数证明其能力类别高低 |

**Figure Helix / Helix 02** 可以继续作为 language → latent → joint target 的架构实例，但所查官方发布页没有给出带 trial 分母的系统成功率。不要让其视频承担这里的能力排序证据。

## 3. 候选新结论：四条均须带边界

### 结论 A：问题不是“LLM 是否调用工具”，而是“哪个环节的 grounding / execution 还需要被外部系统承担”

**证据依据：** Hi Robot 的 language subtask interface 改善指令遵循；Claude 的 cursor tool 能显著改变同一模型的 manipulation 表现；RPent 不更新 frozen VLA 也能扩展其任务适应范围。它们改变的是**信息和责任如何分配**，不只是有没有一个名为 tool 的函数。

**可说：** “Tool use is a design choice about information and responsibility.”

**不可说：** “工具证明 LLM 缺乏物理智能”，或“LLM 能输出 action 证明不再需要控制系统”。Direct EEF 后仍有 IK / OSC / tracking / servo；这里 Direct 通常是“不调用独立 learned action policy”，不是取消底层执行器。

### 结论 B：模型变强，会移动合适的分工边界；不会让 interface 成为无关变量

**证据依据：** Astra 已有直接 EEF 的真实任务成功记录；但 Asim 的同模型结果随 task / interface 改变，匿名 RoboDojo 仍显示 Hybrid 的潜在价值。因而更值得比较 **model × task × observation × interface × feedback/budget**，而不是预设 permanent S2→S1 边界或 Direct 必胜。

**可说：** “Better models move the control boundary; the best interface remains conditional.”

**不可说：** “Astra 因海量机器人预训练必然获得了这些能力”。目前已核官方 announcement / system card 未公开该机器人数据配方或 causal ablation；表现跃升与训练原因是两个不同命题。

### 结论 C：成功理解目标、找对位置与完成接触，是需要分别验证的三件事

**证据依据：** Hi Robot 本来就分别测 IA 与 TP；Robocurve 的 bowl 与 puzzle 差距说明一个成功 demo 不能认证完整 dexterity；Claude 报告也区分 touch / grasp / final success，并展示 spatial aids 的作用。

**可说：** “Correct intent ≠ accurate grounding ≠ reliable interaction.”

这不是宣称三个能力是严格串联、彼此独立的神经模块，而是建议把结果诊断做细：目标是否正确、坐标/姿态是否正确、是否稳定接触、是否最终完成。**端到端成功率可判断系统能否用，却通常不能单独解释失败来自哪里。**

### 结论 D：此前证据需要重新测试，但不应把此前论文改写成它们没有声称的“永久结论”

**证据依据：** Hi Robot v2 §6 明说模型层面的角色分离 **“is not fundamental”**，并提出未来可合并为单模型、在 inference 时区分 System 1 / 2。[论文 Discussion](https://arxiv.org/html/2502.19417v2#S6)。Claude Plays Robotics 也把 model、embodiment、interface 的共同依赖写成结论，而不是证明所有未来模型都不能直接控制。

**可说：** “A stronger foundation model changes the empirical question—not the rules of evidence.”

该重测的是旧 model / interface 条件下的瓶颈和最佳分工；不是用不配对的新 demo 否定所有旧实验，也不是用更新模型的名称替代 robot-data 或 interface 的因果分析。

## 4. 建议的一章收束方式（仅讨论，尚未实施）

保留现有章首 Agent → direct action / Agent Tools 总框图。章末不再收成“工具越来越强”或“Direct 已替代 VLA”，而问：

> **Which capability is limiting this control loop?**
>
> Intent → Grounding → Interaction
>
> Model capability changes the boundary. Interfaces determine what the system must solve.

其中箭头只表示任务检查顺序，不声称 neural architecture。讲稿可用一句中文解释：

“我们现在不急着给 Direct 或 Tools 判胜负。先看这个任务卡在哪里：目标没理解对，空间没对齐，还是接触没执行好；再看更强模型、更多反馈或合适的动作先验，分别把哪一段补上了。”

若用户更重视简洁，只保留结论 A–C；结论 D 放口头过渡与 source note，用于避免把历史论文讲成稻草人。

## 5. 如果要验证这套诊断，而不只是重新命名

这是**我们建议的新实验设计**，不是已完成的实验证据：

- 固定 model / task / reset / camera / compute，分别增加 **明确目标/约束**、**metric pose / frame / proprio 辅助**、**contact policy 或 force/tactile feedback**；观察哪类增益改变失败阶段。
- 单独比较 action interface 时，约束 control-step horizon、query 次数和可用 feedback；报告 native success、失败阶段、wall-clock / cost，而不只报告精选视频长度。
- 使用按 task 预定义的需求 profile，不凭观察到的胜负事后把任务称为“语义型”或“物理型”。

这能检验“瓶颈是否转移”的假说；当前素材本身还不足以完成这样的 causal attribution。

## 6. 一手来源与现有核验记录

- Hi Robot / RPent / Figure：[background 研究记录](control_background_results_2026-09-14.md)，含原图、精确字段、分母与 repository pin。
- Asim / Robocurve / anonymous：[action interface 研究记录](control_action_interfaces_2026-09-14.md)；anonymous 的 retry / pairing 边界见 [专项记录](anonymous_report_421_integration_2026-09-14.md)。这些记录中的旧布局建议不代表当前 talk 页序。
- 本次复用的已核一手 HTML：`research/sources/control_results_20260914/control/{claude,robocurve}_current.html`；仅读取，未修改。相关正文提取与哈希见 `research/sources/wechat_control_20260914/reused_primary_sources.json`。
- 微信文章身份、正文、taxonomy 和文内链接仍未验证；上述来源清单**不是**声称来自该文章的链接清单。

