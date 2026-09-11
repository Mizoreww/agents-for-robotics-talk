# 机器人 Agent 技术分享：图片与视频分镜

## 视觉原则

沿用参考演示的 16:9 白底、青绿色强调、深色标题与大幅内容区。媒体承担解释或证据功能：**这段视频/这张图帮助听众理解哪一步？** 无法回答的素材不进入正文。

- 每页一幅主图或一个主要短片。方法复杂时按步骤揭示，不把多篇论文截图塞成九宫格。
- 表格统一用“输入 / 输出 / 反馈 / 持久化 / 验证范围”；展示事实而非用装饰性框图替代解释。
- 同一素材不重复使用。开场与深讲使用不同运行片段，或由演示切换到方法图。
- 成功与关键失败并置；原图保留分母、坐标、图例与不利结果。
- 所有视频标注原作者、日期、速度/剪辑方式和人工介入。原帖观点与论文实验使用不同文字说明，避免混成同等证据。
- 教学使用保留署名与链接。公开发布或大范围分发前，逐项核查原作者许可；可公开访问不等于拥有再分发授权。

## 七段候选短片

以下是**计划长度而非已经完成的剪辑**，总预算 185 秒，计入 60 分钟正文。时间码、完整运行与速度信息尚需在制作阶段逐片核验。若原视频无法合法获得，使用有出处的静帧与原帖链接替代。

| ID | 页 | 计划秒数 | 素材与来源 | 画面要解释的内容 | 必须保留的说明 |
|---|---:|---:|---|---|---|
| V01 | 2 | 20 | [Robocurve Astra 对照视频](https://openai.robocurve.org/gpt-6-astra/video/bowl-astra-vs-fable51-cost.mp4) | 通用模型经工具接口完成实体操作 | 原页为精选完成运行；等待/加速处理按原页说明，不能据此推断延迟 |
| V02 | 2 | 20 | [Agentic Real2Sim teaser](https://agentic-real2sim.github.io/static/videos/ar2s_teaser.mp4?v=d6a9655b) | 工作产物可以是仿真，而不是当前动作 | teaser 是定性示例，不等于全部输入转换成功 |
| V03 | 2 | 25 | [ENPIRE pin insertion](https://research.nvidia.com/labs/gear/enpire/videos/pin-success.mp4) | 机器人能力可以由研发循环得到改进 | 此片是成果演示；训练过程与重试预算在后文解释 |
| V04 | 17 | 30 | [Robocurve 全部运行目录所在页](https://openai.robocurve.org/gpt-6-astra/)中的 puzzle 失败片段 | 接近正确目标与完成精确插入的差别 | 需按任务/阶段/运行 ID 选片，不凭最好看选取；具体片段待定 |
| V05 | 18 | 35 | [thijs 的 SO-101 绘画原帖](https://x.com/cdngdev/status/2097339677128982873) | 规划、执行、观测与校准 | 同屏注明一分钟动作规划、初始锚点与人工反馈；不标“零人工” |
| V06 | 21 | 30 | [Lingxiao Guo Real2Sim 原线程](https://x.com/Lingxiao234/status/2096992059731443923)及[失败披露](https://x.com/Lingxiao234/status/2096992132527702382) | 同一类重建中，视觉一致与物理正确会分离 | microphone 为 kinematic replay；取片必须能对应披露的具体示例 |
| V07 | 29 | 25 | [ASPIRE 方法短片](https://research.nvidia.com/labs/gear/aspire/assets/videos/method/how_aspire_works.mp4?v=20260629b) | 执行证据如何进入程序修复与技能积累 | 解释技能持久化，不暗示模型权重被自动更新 |

可选替换：用 [Astra 擦桌](https://x.com/k7agar/status/2096593654320341027)的静帧或极短片补充第 18 页，不额外延长章节。它没有足够公开协议来证明稳定力控。机械手 [CAD/动画演示](https://x.com/earthtojake/status/2097789988670709821)只进入附录，并配[作者不可现实运行说明](https://x.com/earthtojake/status/2097801101890207893)。

## 各页主视觉安排

| 页 | 主视觉 | 说明与来源 |
|---:|---|---|
| 1 | 极简标题 | 保留模板留白，不放 Logo 墙 |
| 2 | V01–V03 顺序播放 | 一个画面对应执行、建世界或策略改进；不三屏同时播放 |
| 3 | 两条流程的对齐说明 | “输入—Agent—工具/执行—反馈—产物”；用相同术语逐项对比，避免交叉箭头 |
| 4 | 真实观测与动作接口实例 | 优先选 Robocurve 的相机/位姿说明；不虚构内部传感器 |
| 5 | 动作接口层级表 | 子任务、程序、末端轨迹、关节/力矩分别列出；不要把它们画成必经的四个串行 Agent |
| 6 | 持久化位置比较 | 上下文、技能库、世界参数、权重的简洁可编辑表格 |
| 7 | 证据类型与协议表 | 单次演示、固定预算、未见条件、系统闭环；标注各自不支持的外推 |
| 8 | SayCan 与 Inner Monologue 原始方法局部 | 优先突出 affordance 与反馈两种机制；完整原图置附录 |
| 9 | Code as Policies 的程序与执行实例 | [原项目](https://code-as-policies.github.io/)、[说明视频](https://code-as-policies.github.io/videos/3_min_explainer.mp4)中选择静帧 |
| 10 | VoxPoser value-map 与真实机器人对照 | [原项目](https://voxposer.github.io/)、[teaser](https://voxposer.github.io/media/videos/teaser.mp4)中选空间约束清晰的一例 |
| 11 | Eureka / DrEureka 的训练流程 | [Eureka](https://eureka-research.github.io/)、[DrEureka concept](https://eureka-research.github.io/dr-eureka/videos/concept.mp4)；重点保留 RL 训练与反馈 |
| 12 | RoboGen 与 AutoRT 的工作对象对比 | [RoboGen pipeline](https://robogen-ai.github.io/videos/pipeline_cropped.mp4)静帧与 [AutoRT 原图](https://auto-rt.github.io/static/images/Auto-RT.png)；分别标注仿真与真实数据 |
| 13 | Claude 按接口的原始结果图 | 使用本地 `claude_interfaces.png`；同图保留四种 interface 图例 |
| 14 | Claude VLA supervision 原始结果图 | 使用本地 `claude_vla.png`；保留 VLA-alone 水平参照，口头解释延迟实验 |
| 15 | 当前产业接口比较 | Google 当前页面、π0.7、GR00T N1、MolmoAct2；用版本明确的小表，而不是并排成功率 |
| 16 | Robocurve 的工具与执行协议 | 相机输入、move_to、IK、控制器、限速；引用原页，不猜代码未确认的实现 |
| 17 | 两任务结果与 V04 | 表格列 19/20 与 2/20；附对照与小样本限制；不能只留下 95% |
| 18 | V05 + 方法说明 | 画面占主要空间；原作者 follow-up 摘要紧邻画面 |
| 19 | Claude 与 Astra 协议差异 | 在同一表格中列实验类型、动作接口、预算、等待/人工；不合并算总分 |
| 20 | 四层 Real2Sim 验证表 | 外观、重放、物理交互、未见干预/策略效用；各配一个短定义 |
| 21 | V06 成功路径与失败披露 | microphone 失败必须明确标为运动学重放，不使用“数字孪生已解决”标题 |
| 22 | Agentic Real2Sim 原始流程 | [论文 §3](https://arxiv.org/html/2607.19190v3#S3)及项目 teaser 静帧；分别标出 Agent 与专用视觉/数值工具 |
| 23 | Agentic Real2Sim Fig. 3 | 本地 `agentic_replay_results.png`；保留三类结果与 logarithmic cost axis |
| 24 | SceneMosaic 原始 pipeline | 本地 `scenemosaic_pipeline.webp`；分步讲局部修复和组合，不一次朗读整个图 |
| 25 | ENPIRE 原始系统框架 | 本地 `enpire_framework.png`；先讲环境构建，再讲固定接口后的策略改进 |
| 26 | 单 rollout 的条件重试示例 | 引用论文 §3 的度量定义；步骤编号不能暗示独立采样 |
| 27 | ENPIRE 扩展实验原图/表 | [论文 §3.3、§3.6](https://arxiv.org/html/2606.19980v1#S3.SS3)；截图待获取，需一起呈现时间、成本与利用率 |
| 28 | CaP-X 接口展开与训练结果 | 本地 `capx_interface.png`用于机制；[Table 4](https://arxiv.org/html/2603.22435v2#S5.T4)用于结果，两者不能混称同一性能图 |
| 29 | V07 与持久化技能实例 | ASPIRE 方法动画或[技能库原图](https://arxiv.org/html/2607.00272v1/skill_library_update.png)；避免同时播放和展示密集表格 |
| 30 | RATs 探索与下游测试流程 | [原始方法图](https://Playful-RATs.github.io/assets/images/rats-method.png)；重点标出测试时技能库冻结 |
| 31 | 持久化比较表 | 对齐 Astra / Real2Sim / CaP-RL / ASPIRE / ENPIRE 的产物 |
| 32 | 能力地图 | 分类表而非不可比数值排名；一页只保留重点工作 |
| 33 | 四类瓶颈与对应证据 | 用前文案例的文字索引，不重复媒体；接触、反馈、辨识性、验证/成本 |
| 34 | 研究问题 | 简洁列出机制问题与验证方式；标为综合分析 |
| 35 | 实验报告标准 | reset、retry、人类介入、延迟、独立验证、未见干预 |
| 36 | 三项结论 | 纯文字收束，保留模板留白 |

## 已保存并检查的原图

以下六项已保存本地并检查图面内容；这不等于完成整套 PPT 的排版验证。

| 文件 | 内容 | 制作时注意 |
|---|---|---|
| [claude_interfaces.png](/home/limx/Desktop/agent_for_robotics/research/assets/claude_interfaces.png) | 按模型/接口的 composite score | 原图每接口权重和总分定义不可裁掉 |
| [claude_vla.png](/home/limx/Desktop/agent_for_robotics/research/assets/claude_vla.png) | LIBERO-40 的 VLA+LLM 结果 | 保留独立 VLA 基线、误差线、模型名称 |
| [agentic_replay_results.png](/home/limx/Desktop/agent_for_robotics/research/assets/agentic_replay_results.png) | DROID-100 接受结果与模型费用 | 图中的百分比与计数在 N=100 下相同，但需注明分母；费用为模型调用 |
| [enpire_framework.png](/home/limx/Desktop/agent_for_robotics/research/assets/enpire_framework.png) | 环境构建、Agent 改进、真实任务 | 图很高，正文需分区域讲解；完整图保留在附录 |
| [capx_interface.png](/home/limx/Desktop/agent_for_robotics/research/assets/capx_interface.png) | 高/低层代码接口展开 | 字小，正文只聚焦与感知/几何有关的部分，不将其误标为实验结果图 |
| [scenemosaic_pipeline.webp](/home/limx/Desktop/agent_for_robotics/research/assets/scenemosaic_pipeline.webp) | 重建、物理稳定、局部演化、组合 | 内容多，分阶段揭示；不把所有模块当作 LLM 直接计算 |

原始 URL 与 SHA-256 保存在 [图片清单](/home/limx/Desktop/agent_for_robotics/research/assets/manifest.json)。Agentic Real2Sim 的另一张 qualitative 图获取超时，未计为可用素材；已有 Fig. 3 不受影响。

## 媒体制作检查单

1. 每段先完整观看，再选择时间码；记录运行/episode ID、原始时长、是否包含人类提示。
2. 不用暂停仿真或删去等待的片段证明实时性；不把手工 kinematic replay 标成 physics simulation。
3. 不修改图中的模型、基线、数字、误差线或坐标；如为可读性重绘，保存结构化数据与原图，确保含义一致。
4. 若图中多小图只有一部分用于正文，裁剪边界必须保留该结果的图例、任务、坐标与定义；完整版本进附录。
5. 视频优先本地嵌入，避免讲台网络依赖；无法再分发的素材只使用静帧与链接，明确媒体未嵌入。
6. PPTX、中文讲稿与媒体文件统一编号；导出后逐页检查布局，并实际测试视频播放与备用静帧。
