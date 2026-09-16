# GPT-6 Astra：action interface 比较证据

检索/核查：2026-09-14。用途：仅供 Control 章提纲讨论；**未改 slides 或讲稿**。公开网页、README、schema 与记录只读核查，没有安装项目、运行机器人/模型或调用 Claude/Anthropic 服务。核心问题是“是否仍需独立 learned System 1”，不是能否取消伺服、IK、动作限幅等底层执行器。

## 可以直接用的结论

> **Astra 已能直接生成可执行动作；但同一模型的最佳 action interface 仍依任务、观测和执行预算而变。现有比较不足以宣布 numeric action、code 或 learned policy 在所有任务上胜出。**

新找到一个很贴题的同模型接口矩阵：**asimfish 的 Astra control dashboard**。它比泛泛社媒 demo 更接近用户问的“不同 action 输出”，但仍不是严格等预算消融。没有找到同时控制模型、任务、观测、预算，并覆盖 **joint q / EEF / program / semantic micro-actions / VLA supervision** 的完整比较。

## 1. Astra control dashboard：最直接回答 action 输出问题

- [公开面板](https://asimfish.github.io/astra-control-dashboard/#sec0)；[输入/输出原文](https://asimfish.github.io/astra-control-dashboard/#sec2)；[完整结果表](https://asimfish.github.io/astra-control-dashboard/#sec3)；[逐回合视频/推理](https://asimfish.github.io/astra-control-dashboard/#sec4)。作者的一手实验面板，**不是同行评审论文**。
- [仓库](https://github.com/asimfish/astra-control-dashboard)，revision **`1e7952c26e0a8783e4eca48514b3a1cc03e2c5df`**，2026-09-10。现网页与该 revision 的 [index.html](https://github.com/asimfish/astra-control-dashboard/blob/1e7952c26e0a8783e4eca48514b3a1cc03e2c5df/index.html) byte-identical。
- **模型/任务**：`gpt-6-astra`, medium reasoning；Franka Panda，robosuite 1.5 / MuJoCo 3.3.x，Lift / Can / Square。主表为 prompt v3、每个条件 **20 episodes**；早期5回合保留在历史表，不能混池。作者声明回合 i 跨条件使用相同 reset 物体位姿，未获得独立原始 simulator-state hash 来证明。
- **delta ≠ joint q**：每次生成20个 **7D OSC_POSE ΔEEF 动作** `[dx,dy,dz,droll,dpitch,dyaw,gripper]`，开环执行后重新看图；底层OSC仍执行动作。不能把这项写成“直接输出关节角”。
- **waypoint**：每次1–4个绝对末端位置、yaw、gripper；P controller跟踪，位置容差约1cm，随后保持10步gripper命令。没有 learned policy。
- **code**：生成 `plan(scene)` Python程序，返回至多12个Waypoint，经同一waypoint controller执行；执行反馈后可改写程序。**不是一个任意高频闭环controller**；proprio条件下不能读目标物体真值坐标。
- **proprio不是只加本体状态**：图像 + EEF/gripper状态 + EEF像素标记 + 相机尺度/轴向 + 固定地标坐标；privileged还加目标物体真值与grasp state。因此不能把proprio/none差异全归因于本体状态。

### 核心数字：只选相同 proprio 档位，不放杂乱大排行榜

| Task | ΔEEF action chunks | EEF waypoints | Code → waypoints |
|---|---:|---:|---:|
| Lift | 20/20 | 20/20 | 20/20 |
| Can | 18/20 | 17/20 | 7/20 |
| Square | 1/20 | 18/20 | 16/20 |

核验：从公开HTML的逐episode success badge重数上述180条，与原表9格完全一致；全部视频卡共370条，与面板声明相同。这是对**公开记录一致性**的核验，不是重跑实验或独立判视频成功。

**最大混杂必须同页出现**：delta最多200 control steps / 10 queries；Square waypoint最多500 steps / 16 queries；code最多500 steps / 3轮程序。控制器执行长度、feedback cadence、动作生成形式一起改变，**不是 matched-budget interface ablation**。Square waypoint平均256.6步，已高于delta的200步上限，尤其不能把18/20对1/20全部归因于表达方式。Can部分条件还跨机器；新旧prompt的差异不用于归因。

**一页推荐**：同一Square初态的两个小视频 + 三个结果数字 **1/20 · 18/20 · 16/20**，下一行明确 unequal control/query budgets；口头再用Can的排序变化说明“没有统一最优接口”。若空间不足，只用两视频+简短结论，不复制整个矩阵。

### 原表与真实媒体，已经确认可用

- 原来源是 **HTML table**，没有独立作者PNG；本次截图：[完整原表展开截图](sources/control_action_interfaces_20260914/asim_matrix_expanded_capture.png)。仅解除网页layout/max-width以完整展示横向表格；没有改数字、文字、bar。`asim_matrix_original.png` 是初次被overflow截断的截图，**不要用于slides**。
- 原文快照：`sources/control_action_interfaces_20260914/asim_index_pinned.html`；结构化抄取：`asim_tables.json`；全部episode记录：`asim_episodes_parsed.json`。不能把本次JSON说成作者原始实验输出。
- [Lift ΔEEF，ep00，成功，1.8s](https://asimfish.github.io/astra-control-dashboard/media/Lift__delta__proprio__codex-gpt-6-astra__s0__20260908T125956Z/ep00.mp4)。
- [Square ΔEEF，ep00，失败，10.2s](https://asimfish.github.io/astra-control-dashboard/media/Square__delta__proprio__codex-gpt-6-astra__s0__20260908T131857Z/ep00.mp4)。
- [Square waypoint，ep00，成功，17.3s](https://asimfish.github.io/astra-control-dashboard/media/Square__waypoint__proprio__codex-gpt-6-astra__s0__20260908T132052Z/ep00.mp4)。
- 这三条已在Chrome实际播放，均 **256×256、currentTime推进、error=null**；核验记录 `video_playback_check.json`。素材是低分辨率agentview simulation replay，不是实时包含模型等待的录屏。作者说明10fps≈仿真实时，不能当LLM真实反应速度；视频没有下载到生产素材目录。
- **代码边界**：面板所链接的 `asimfish/robocore`、`docs/VLM_CONTROL.md`，本次公开访问均404；因此仅能核查面板、原prompt/schema和推理记录，不能声称已审执行器源码。

## 2. 匿名 Direct / Hybrid 报告：同 Astra，加不加 learned prior

- [报告](https://anonymous-report-421.github.io/public-website/?lang=en&view=1)；源码revision **`79f8be5905102d6b16000c0f02a9c2195b51bb61`**；website revision **`9ac494dce8fcd7333eb2ea685fee5b4cddf19eb1`**。保持匿名，正式标题 *GPT 6 Astra as an Embodied Policy*。
- **Direct**：双臂EEF position/quaternion/gripper，每次1–5 control steps，本地DLS IK执行；不调用π0.5。
- **Hybrid**：π0.5提供50×14 joint-space候选及双臂FK轨迹，Astra审核并接受1–15步，或给1–5步EEF correction。这里joint q来自π0.5，**不是Astra q vs EEF消融**。
- RoboDojo selected **10 tasks × 5 paired cases**：Direct **13/50**，Hybrid **24/50**；两者`gpt-6-astra/xhigh`。本次从fresh `data.json`独立重数一致；Hybrid修正6,174 / 42,750 control steps =14.4%，不是Astra只调用14.4%。
- 先验、动作分支、segment length一起改变；任务偏向π0.5较弱区间，不能推及全部manipulation。RoboLab retained final slots有重试/不等预算，不把49/50对46/50当controlled胜负。
- 原Direct/Hybrid架构在现talk已有 `.build/assets/v0_7/report_architecture_original.png`；它是**系统执行架构**，不是Astra内部网络。
- [Direct分类视频](https://anonymous-report-421.github.io/public-website/media/rollouts/gpt__classify_objects__standard__g0__l3.mp4)；[Hybrid packing片段](https://anonymous-report-421.github.io/public-website/media/clips/clip__615a6ef1b93ea9da852f24c9__0.mp4)。来自不同任务，不能伪装为paired视频；均省略模型等待。
- fresh schema、EEF contract保存为 `anonymous_schema.py`、`anonymous_eef.md`，只读确认Direct仅EEF 1–5步及Hybrid student/edit/eef/stop分支。完整既有证据见 [此前核查](anonymous_report_421_integration_2026-09-14.md)。

## 3. Robocurve：直接 EEF 已很强，但精细接触不是已解决问题

- [一手报告，2026-09-04](https://openai.robocurve.org/gpt-6-astra/)；[Inspect Robots](https://github.com/robocurve/inspect-robots) v0.58.0。
- YAM双臂，三路相机 + proprio；绝对EEF `move_to(x,y,z,yaw,pitch,roll,gripper)`，IK转关节角，20 LLM-call budget、medium、25% speed cap。
- **Astra bowl 19/20；round puzzle insertion 2/20**。同接口的Fable5.1分别8/20、2/20；不是Astra内部接口消融。这里旧模型研究只引用公开实验，不调用用户Anthropic资源。
- bowl跨rig（Astra rig1 / Fable rig3），不同日期非interleaved、手动reset、模型已知的人工评分；因此不能把差值全部归因于model。puzzle是同rig但仍非paired随机试验。
- [原比较视频](https://openai.robocurve.org/gpt-6-astra/video/bowl-astra-vs-fable51-cost.mp4)与网页内原SVG结果图可引用；视频挑各模型最好完成episode，并去掉thinking pauses，不是代表性实时执行。
- **用于转折一句话**：没有独立VLA，Astra也能把简单真实操作做得很可靠；但同一套系统的精细插入仍只2/20，不能从一个contact-rich精选demo断言general dexterity已解决。

## 4. 其他线索只作边界，不再扩成主讲案例

- [GPT-Policy-Eval](https://github.com/cheng-haha/GPT-Policy-Eval/tree/43929f0ee3673da67393fcbe85d43c58eb15db59)：one-video demonstration + live feedback，plug insertion的真实机器人展示；[12×视频](https://github.com/cheng-haha/GPT-Policy-Eval/raw/refs/heads/main/assets/plug-insertion-top-and-right-wrist.mp4)。作者明确是selected individual trials，systematic evaluation/code release仍future work，**无trial denominator，无interface ablation**。
- [Show-Harness](https://arxiv.org/html/2609.10522)：有semantic micro-actions，但fresh paper/project/README未发现Astra实验；不能拿其他backbone的结果填入Astra比较表。
- [GPT Dog Eval](https://github.com/guajun/gpt-dog-eval/tree/04ef36d8120545341f6f1e77a464327c801e03aa)：真实joint-target residual路径，Go1、12D `q_nominal+0.5a`、chunk/PD。公开journal仅每scene一次的Astra探索，反馈修复与静态robot-spec对比，不是q/EEF/code对照；有失败与return/termination问题，**不推荐再塞进主讲**，也说明不要把EEF结果外推为所有q控制。
- [RPent](https://github.com/RLinf/RPent)：可用[官方framework原图](https://github.com/RLinf/misc/raw/main/pic/rpent_framework.png)说明服务组合；本次README未见GPT-6 q/EEF/code同协议比较，不能把toolkit支持某接口当作该接口优势的实验。

## 5. “因为预训练加入海量机器人数据”：目前不能写成 Astra 已证事实

核查 [OpenAI Astra announcement](https://openai.com/index/gpt-6-astra/)、[官方system card](https://deploymentsafety.openai.com/gpt-6-astra)及既有官方model doc。公告提pre-training/RL/alignment进展，但未披露机器人数据配方、规模或机器人控制因果消融。system card已保存直接HTML与正文快照；公告直接抓取403，使用相同官方URL的公开文本镜像读取。**这些已检查的一手来源未提供“海量机器人数据预训练导致Astra控制跃升”的证据**；不等于证明未使用机器人数据。

建议讲稿措辞：**“随着foundation model能力变化，过去在某些模型和接口上得到的结论需要重新检验；若训练进一步吸收机器人数据，分工边界更可能移动。Astra的公开直接控制结果已经让这个问题值得重问，但其具体训练原因尚未披露。”**

## 检索覆盖与材料清单

线索入口：fresh [Awesome Astra](https://github.com/zjwzcx/Awesome-Astra-Embodied-AI/tree/61baafd5fc94ae2db32da8da57704310033a6210)、[Awesome Robot Use Agent](https://github.com/kairunwen/Awesome-Robot-Use-Agent/tree/2324c525a122b129505fd757744fb35f36a366c8)，后续均追到作者网站/仓库。搜索词含 `GPT-6 Astra robot action interface comparison 2026`、`GPT-6 robot joint pose 2026`、`Astra robot control ablation September 2026`；另GitHub repository search检查Astra+joint/pose/interface/action。DDG出现human challenge，未绕过；Bing/Google相关性差，主发现来自GitHub搜索和一手交叉链。**这是截至今天的有界检索，不声称穷尽全部未索引报告。**

所有本轮源快照/表格抄取/截图/验证均在 `research/sources/control_action_interfaces_20260914/`。原网页中的运行命令不被执行；所有项目都只读。
