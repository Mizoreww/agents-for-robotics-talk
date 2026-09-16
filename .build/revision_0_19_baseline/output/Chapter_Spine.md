# Agents for Robotics — 章节主线 v0.18

Zimo Huang · 2026-09-16。36页英文 slides，25段内嵌视频，中文讲稿。建议59分钟，未彩排。

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

## 3. Improvement（23–34）：实验反馈能否改善下一次研究？

**问题（23）**：不仅改下一条 action，还要改下一版 policy；先用框图看完整物理反馈循环。

**方法（24–27）**：ENPIRE 原 Figure 2，先 human-assisted environment setup，后固定 safety/reset/verifier 的 autonomous improvement。完整 reset / verification 视频解释重复实验如何成立。两张官网任务照片区分 heuristic code 与 BC/RL policy training。Figure 12 原 idea tree 展示 objective、batch size 和 controller compensation 等真实修改；保留无收益分支，不当独立因果消融。

**实验（28–30）**：Figure 3 与官方终点均值保留 Push-T normalized score、Pin success rate 的不同指标。Fleet 完整视频配原 learning/scaling 曲线，1→8 pairs 从 >1.5 h 到 ~40 min，指 research time。物理 pass@8 含 conditional retries，不是 iid sampling。RoboCasa Figure 6 与表格保持40个固定 matched episodes、每episode一次script、禁 reset/retry/oracle 的协议，不估计柱高。

**行为与迁移（31–32）**：Pin / tie / cut 三段官方完整视频，8×，替代 CAD/RL 与 physical ICL。GPU insertion 完整视频配 Pin→written recipes→GPU autoresearch 图。§3.4 / Appendix B.1 的迁移对象是经验总结，不是旧 checkpoint / raw trajectories；视频不是 transfer ablation。

**成本（33）**：Figure 7 及精确均值/std。更多机器人缩短研究时间，却提高 fleet token rate；utilization 是 active-time fraction。该图4.5/3.2/2h与40min曲线不是同一组实验。

**RSI 与总结（34）**：上方闭环说明 ENPIRE 的 policy improvement；下方 memory/recipes 指向“Better future research?”。RSI 指 Recursive Self-Improvement，改进者可以通过 tools、memory、workflow/code 改变，不局限于 LLM weight updates。是否在 held-out tasks 和 matched budgets 下更擅长改进、且不遗忘，仍是开放检验。RoboRSI 与 DGM 只在讲稿中提供概念背景，不再展开新标杆。

## Closing（35–36）

Takeaways 保留三条 Role→Artifact→Evidence 支路，再感谢与讨论。三章不是一条已经打通的端到端流水线。

证据：`research/enpire_rsi_evidence_2026-09-16.md`。中文逐页稿：`Speaker_Script_Revised.md`。
