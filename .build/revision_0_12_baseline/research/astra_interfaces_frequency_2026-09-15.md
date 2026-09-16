# Astra 实际接口与推理频率核查

核查日期：**2026-09-15**。基于已有一手快照继续核查，并重新验证 Asim pinned HTML；只读公开资料，没有运行机器人项目、调用模型或访问任何 Anthropic 服务。本文支持 v0.11 Control 章节，不新增论文深讲。

## 结论

**现在并不是“所有 Astra 案例都直接输出全身关节角”，也不是“都在调用原子技能”。已公开的链路至少包含 numeric joint chunks、EEF / ΔEEF、生成 waypoint 程序，以及 learned-prior 审核/委托。** 软件中出现 tool call，不等于把动作决策交给了 learned skill：`move_to` 和 `run_joint_chunk` 本身可以只是把模型决定的数值目标交给执行器。

**目前没有一个可统一引用的“Astra 控制频率”。** 可核验的 Asim 同模型记录中，三种接口的平均查询耗时约 **26–42 秒/次**；这是一个具体 medium-reasoning harness 的结果，不是 Astra 在所有部署下的速度。20 / 25 / 50 Hz 通常指下游动作执行；模拟器能在 LLM 思考时暂停，视频也常删除等待。不能据此宣布模型实现了实时高频反馈控制。

章节总结宜写为：**已展示的优势：语义理解、有限范围内的空间迁移；尚未可靠解决：实时高频反馈控制、跨接触/动力学条件的物理泛化。** “尚未可靠解决”不等于任何精细操作都做不到，更不是永久能力上限。

## 1. 谁输出什么，谁负责执行

| 一手案例 | Astra 实际输出 | 下游与边界 | 推理速率证据 |
|---|---|---|---|
| **GPT Dog Eval / Go1** [D1–D3] | `run_joint_chunk` 中的 **12D normalized joint-position residual** keyframes；也可 `hold` / `give_up` | `q_target = q_nominal + 0.5 a` rad；插值、限幅后交给 PD。12个是四足机器人的全部驱动关节，**不是人形机器人的全身关节，也不是 torque** | 控制50 Hz、physics250 Hz；**推理期间sim暂停**。未公布可直接复算的逐query wall-clock表 |
| **RoboCurve YAM** [R1] | 每臂绝对 EEF `move_to(x,y,z,yaw,pitch,roll,gripper)` | 机器人 IK 转关节目标；三路相机 + proprio，medium、20-call预算、25%速度上限；不是 VLA 接手 pick | 报告/所检 transcript 有整回合 duration，**没有可复算的逐调用耗时序列**；duration/calls混入执行时间，不当纯 inference Hz |
| **Asim / Panda** [A1] | ①20个7D **OSC_POSE ΔEEF** action；②1–4个EEF waypoint；③`plan(scene)`返回至多12个waypoint | ΔEEF 经 OSC；waypoint 经 P tracking + OSC；code生成航点，不是任意实时闭环policy。**delta不等于joint q** | 公开逐query秒数；20 Hz是动作执行率，详见下一节 |
| **匿名 Direct / Hybrid 报告** [H1–H3] | Direct：双臂EEF position/quaternion/gripper；Hybrid：审核 π0.5 candidate、接受或给EEF correction | candidate是 π0.5 生成的 **50×14 joint-space trajectory**，不是Astra自身直接输出q。Direct/correction执行1–5步；接受candidate执行1–15步。local DLS IK执行EEF | native25 Hz（每控制步0.04s）**不是LLM25 Hz**；未披露可统一推算的wall-clock query rate |

### Go1 的“直接关节控制”如何准确讲

- `[FR, FL, RR, RL] × [hip, thigh, calf]` 共12维；`a ∈ [-1,1]` 是相对 nominal pose 的归一化位置偏移，**不是对上一时刻q继续累加的增量**。[D2]
- 每chunk最多4个keyframes、15个control steps，即最多300 ms模拟时间；执行器从实际 `last_applied_action` 线性插值，拒绝超过0.1/20 ms的动作变化。它保留真实执行反馈，并非只离线写一个gait程序。[D1–D2]
- 报告中的5.8–9.4 Hz按运动/hold chunk数除以**模拟时长**计算；排除了tool validation失败和give_up stop。因为思考时sim暂停，**不能称为Astra每秒推理5.8–9.4次**。[D3]
- 4场景、每场一次的v3探索不是系统benchmark；Astra+spec在该批四场return均低于Zero和原生ONNX，forward提前give_up。它可作“直接q路径存在但控制质量未解决”的例证，不能外推到所有q接口或证明某种数据训练无效。[D3]

### 原子技能 / learned policy 的披露边界

- **优先使用匿名Hybrid作为已核验第四路径**，称为“learned-prior review / correction”，不要硬改成 `pick(object)` 原子技能调用。
- G1 cola作者原视频画面明确标注 `AGENT → OFFICIAL SONIC PLANNER → SONIC 50Hz → ISAAC G1`，因此至少这个人形demo不是Astra直接输出全身q。画面另标 `Agent command=1.0Hz`，但未给出LLM请求的wall-clock计时定义，**只作为作者overlay，不用作Astra实测速率**。[C1]
- Mobile ICL作者称模型能选择 EEF 或 joint space，展示不同环境、视角、layout；这是一级作者声明，缺schema、执行器代码和试验分母，不能据此指定其q维数或可靠泛化率。[C2]
- Awesome的FluxVLA条目可作为检索入口；本次未获得足以独立核验的一级接口代码/评测，**不纳入硬证据表**。RPent支持某接口不等于Astra已在统一协议下验证其优势。
- GPT-Policy-Eval公开tree当前只有README/媒体；作者明确selected individual trials、code release未来发布。**No VLA**不能推导出具体API、servo频率或没有底层控制器。[P1]

## 2. 可复核的查询耗时：Asim

固定来源为 `astra-control-dashboard@1e7952c26e0a8783e4eca48514b3a1cc03e2c5df/index.html`，与2026-09-15取得的live页面逐字节一致，SHA-256：`50af836616bef6dfaed22e142702d37da7e5884c85954e9cb9ae3e7d685d4851`。[A1]

选择 **prompt-v3 / proprio / gpt-6-astra / medium**；Lift、Can、Square × 3 interfaces ×20 episodes = **180 episodes**。不含历史5回合、不含`none`或`privileged`。从每一episode的逐query耗时重算，不用四舍五入的episode均值；总计 **731 queries**。

| Interface | Episodes | Queries | Mean s/query | Median s/query | 1 / mean（queries/s） |
|---|---:|---:|---:|---:|---:|
| ΔEEF chunks | 60 | 414 | 30.7473 | 29.370 | 0.03252 |
| EEF waypoints | 60 | 241 | 26.0816 | 25.718 | 0.03834 |
| Code → waypoints | 60 | 76 | 41.9847 | 41.016 | 0.02382 |

**推荐投影片主显示秒/次，不把倒数写成“control Hz”。** 倒数仅是上述平均记录耗时的算术倒数，不含环境执行/渲染/反馈开销，不是完整闭环反馈率，也不是模型服务端pure-generation benchmark。不同接口的query内容、输出长度、action horizon和query budget不同；这个表说明时间尺度，不是公平的接口性能排名。

控制链路的时间尺度：ΔEEF每次输出20步，每步20 Hz，即**1秒模拟动作 / 一次查询**；waypoint每次1–4点，单点最多80控制步，然后gripper保持10步；code一次至多12点，之后可根据结果改写。不能用这段模拟动作时长除以展示视频帧数，替代真实模型等待。

**可复现审计**：`derive_asim_query_times.py` 绑定源hash、commit和准确9-run/180-episode identity；`verify_asim_query_times.py` 用独立HTMLParser核对370总展示回合、180被选回合、731 queries、连续query编号和全部12条task/ALL汇总，已执行通过。源码入口`asimfish/robocore`本次仍404，故只称核验了**公开prompt、schema、日志与报告**，不称独立审计了隐藏执行器源码。

## 3. 第一章的能力结论应如何落地

- **Semantic understanding**：在指定观测、任务说明和预算下，能做对象/目标理解与步骤选择；RoboCurve bowl为19/20，不能推广为所有操作可靠。[R1]
- **Spatial generalization / retargeting**：可从视觉与proprio确定动作目标；community demo展示环境/视角/layout迁移。它与跨质量、摩擦、接触几何的物理泛化不是同一个问题，当前证据强度也不同。[A1, C2]
- **High-frequency feedback control**：上述Asim查询为数十秒级；Go1依赖暂停sim，控制器可以高频执行但模型并非实时高频重新观察。不能把“输出一串高频动作”误写为“高频闭环推理”。[A1, D1–D3]
- **Physical generalization**：跨接触/动力学条件的可靠性未确立。RoboCurve puzzle insertion仅2/20；Go1某轨迹的恢复失败提供局限，但精选plug-insertion demo也说明不能声称一切接触操作都不可能。保留 **“not reliable / not established yet”**，而非 **“cannot ever”**。[R1, D3, P1]
- 保留开放问题：foundation model能力变化后旧结论要重测；Astra的具体机器人预训练配方与因果消融未公开，不把“加入海量机器人数据所以提升”写成已证事实。

## 4. 推荐一页紧凑图（英文页面、中文讲解）

标题：**What Does Astra Actually Output?**

左侧4行：`Joint chunks → interpolation + PD`；`EEF / ΔEEF → IK / OSC`；`Code → waypoint controller`；`Hybrid → prior accept / EEF correction`。每行只贴一个短来源标签。右侧3行：Asim **30.75 / 26.08 / 41.98 s/query**，小字`medium · 180 episodes · 731 queries`。

底部一句：**LLM query time ≠ Controller Hz.** 小字保留`One harness; not end-to-end feedback rate; budgets differ.` 下一页总结用两组框：`Demonstrated: Semantics / Spatial retargeting`与`Remaining gaps: Fast feedback / Contact & dynamics generalization`，不额外展开Go1深讲。

## 一手来源 / 可追溯快照

本轮素材根目录：`research/sources/astra_interfaces_frequency_20260915/`。`manifest.json`记录URL、bytes、SHA及继承来源；来源内容与本地derive/audit脚本分别标识。搜索结果、Awesome分类和作者demo不当作benchmark测量。

- **[A1] Asim**：[pinned index](https://github.com/asimfish/astra-control-dashboard/blob/1e7952c26e0a8783e4eca48514b3a1cc03e2c5df/index.html)；[配置/三种I/O](https://asimfish.github.io/astra-control-dashboard/#sec2)；[逐query记录](https://asimfish.github.io/astra-control-dashboard/#sec4)。本地`asim_index.html`、`asim_index_pinned.html`、`asim_query_times_derived.json`。
- **[D1] Go1接口与暂停条件**：[README@04ef36d](https://github.com/guajun/gpt-dog-eval/blob/04ef36d8120545341f6f1e77a464327c801e03aa/README.md)。本地`dog_readme.md`。
- **[D2] Go1动作映射与编译**：[constants.py@04ef36d](https://github.com/guajun/gpt-dog-eval/blob/04ef36d8120545341f6f1e77a464327c801e03aa/src/gpt_dog_eval/constants.py#L9-L76)，[agent.py@04ef36d](https://github.com/guajun/gpt-dog-eval/blob/04ef36d8120545341f6f1e77a464327c801e03aa/src/gpt_dog_eval/agent.py#L24-L44)及`_compile_joint_chunk`。本地`dog_constants.py`、`dog_agent.py`、`dog_inference.py`；代码只读。
- **[D3] Go1原始报告**：[v3 robot-spec results@04ef36d](https://github.com/guajun/gpt-dog-eval/blob/04ef36d8120545341f6f1e77a464327c801e03aa/docs/v3-robot-spec-results.md)。本地`dog_results.md`；特别参见“后续policy复查”的反馈频率定义。没有把历史单次探索包装为新benchmark。
- **[R1] RoboCurve**：[GPT-6 Astra一手报告](https://openai.robocurve.org/gpt-6-astra/)，[检查的Astra transcript](https://openai.robocurve.org/gpt-6-astra/runs/transcripts/rig-1_6b47f3c6)。本地`robocurve.html`、`robocurve_transcript_sample.html`。没有访问其另一个模型服务。
- **[H1] 匿名动作schema**：[schema.py@79f8be5](https://github.com/anonymous-report-421/eval-of-gpt-6-astra-as-policy/blob/79f8be5905102d6b16000c0f02a9c2195b51bb61/hybrid_rollout/robodojo/skill/schema.py)。本地`anonymous_schema.py`。
- **[H2] 匿名执行合同**：[eef_control.md@79f8be5](https://github.com/anonymous-report-421/eval-of-gpt-6-astra-as-policy/blob/79f8be5905102d6b16000c0f02a9c2195b51bb61/hybrid_rollout/robodojo/skill/context/eef_control.md)。本地`anonymous_eef.md`；第38–47行区分DLS IK、25 Hz control observation与chunk-boundary decision。
- **[H3] 匿名报告**：[GPT 6 Astra as an Embodied Policy](https://anonymous-report-421.github.io/public-website/?lang=en&view=1)。本轮`anonymous_data.json`；系统架构的既有一手extract与源码核验见`research/anonymous_report_421_integration_2026-09-14.md`。不公开/推测作者身份。
- **[C1] G1 / SONIC作者视频**：[Flood原帖](https://x.com/RotekSong/status/2099104628562608371)。本地`g1_cola_post.json`、`g1_cola_frame.png`（2026-09-14浏览器播放截图，本轮重新视觉检查其overlay）。数字overlay不是独立timing日志。
- **[C2] Mobile ICL作者声明**：[Axel Peytavin原帖](https://x.com/ax_pey/status/2098216469012283681)。本地`mobile_icl_post.json`；正文称“chooses when to use end-effector or joint space”。
- **[P1] GPT-Policy-Eval**：[README@43929f0](https://github.com/cheng-haha/GPT-Policy-Eval/blob/43929f0ee3673da67393fcbe85d43c58eb15db59/README.md)。本地`policy_eval_readme.md`、`policy_eval_tree.json`；不从所选视频推测未披露的action API。

核查范围有限：截至核查日公开的这些来源，没有覆盖全部私有demo、未索引社媒或未公开部署；因此不提供各接口在“所有Astra用户”中的百分比分布。
