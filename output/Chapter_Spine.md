# Agents for Robotics — 章节主线 v0.20

Zimo Huang · 2026-09-16。37页英文 slides，28段内嵌视频，中文讲稿。建议60分钟，未彩排。

## 1. Control（4–17）：动作决策应该放在哪一层？

- **4–6 导图与问题**：Agent 直接 q / EEF 命令及工具分支；Hi Robot / Helix / Helix 02 原架构；泛化责任从 generalist VLA / WAM 部分上移到 System 2 的功能示意。System 0 / Controller 保留。
- **7–9 新能力展示**：Robocurve 两任务完成数；plug/keyboard 真机 demo；新增 Rubik’s Cube 与 Claw 仿真 puzzle。Cube 的 action API 未披露。Claw 是预抓取、理想刚性 grasp 下的 IK/joint path，参考 object-space 解来自既有工作，不能称为已验证的接触动力学或任意初态 online policy。
- **10–11 接口探索**：同一 Astra 的 ΔEEF、waypoint、code 对比及三任务结果。控制和查询预算不齐。Waypoint proprio 的整列强调不是所有任务上的统一最优。
- **12–15 Direct/Hybrid**：原始执行架构，RoboDojo/RoboLab 原结果图及热力图。历史基线、retained slots、retries 与不同 horizon 保留各自口径，不混池。
- **16–17 瓶颈与总结**：平均 query 数十秒，不能承担高频反馈；语义理解和部分空间迁移已有展示，可靠物理泛化仍是问题。研究方向是降低 latency 和设计更连贯、更稳定的 action primitives。

## 2. Data（18–22）：怎样利用这些产物帮助训练？

- **18 导图**：Assets / scenes、Real-to-sim Replay、Data Rollout。
- **19 场景**：Office / Newton 与 articulated kitchen 原视频；kitchen 仍在 adding simulation。
- **20 手部资产**：CAD 与 rope-hand reconstruction，后者采用 simplified mechanics / illustrative cable deformation。
- **21 行为与数据**：multi-view replay 与 DexGPT contact rollout。记录了状态/动作/接触不意味着 physical validation 通过。
- **22 总结**：检验资产可用性、replay matching 和 physics，问“How can we use it for downstream training?”。

保持原五页紧凑组织，不恢复 Agentic Real2Sim 论文深讲。

## 3. Improvement（23–35）：按官网顺序理解 ENPIRE

- **23 导图**：保留已删减的章节闭环图，不恢复 Chapter overview、Evidence 或 Still open 文本。
- **24 ENPIRE System**：原 Figure 2，先构造环境，再在固定接口下改进 policy。
- **25 Auto Evaluation**：two-view detector 视频配 detection / segmentation → per-view geometry → AND reward 框图；判定标准固定。
- **26 Auto Reset**：按官网 Case 1–4 看 Push-T、Pin、Zip-tie、GPU；完整 reset case，与 learned-policy rollout 分开。
- **27–28 Policy Improvement**：heuristic code 与 BC/RL 训练两条路，再看原 idea tree 中成功和无收益的修改。
- **29 Evaluate Coding Agent**：原曲线和精确数据；Push-T normalized score 与 Pin success rate 不混池。
- **30–31 Fleet Scaling**：并行研究曲线与视频，接成本和 utilization，区分 Figure 3/7 口径。
- **32 Simulation Evaluation**：RoboCasa 原图，40 个固定 matched episodes、每回合一次 script，禁 reset/retry/oracle，不估柱高。
- **33 Learned Policy**：在系统和定量结果之后集中展示 Pin、GPU、Tie/Cut zip-tie 四段官方 demo，8×，不是新的成功率统计。
- **34 Limitations**：单独讲资源闲置与 token 成本，不混入未来方向。
- **35 Toward Recursive Self-Improvement**：保留 policy improvement 闭环，再以 Pin→Markdown summary→GPU 的经验复用引出“能否让 improver 自己变好”的 open question，不宣称无限递归能力。

## Closing（36–37）

Takeaways 保留三条 Role→Artifact→Evidence 支路，再感谢与讨论。三章不是一条已经打通的端到端流水线。

证据：`research/enpire_rsi_evidence_2026-09-16.md`。中文逐页稿：`Speaker_Script_Revised.md`。
