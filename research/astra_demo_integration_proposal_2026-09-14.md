# Astra demo 增补：用展示说明工作流程如何变化

2026-09-14。回应用户“多放一点 Awesome-Astra-Embodied-AI 的 demo，因为 GPT-6 出来后很多流程不一样了”。本文件为新的内容安排提案，补充同日 Control 与 Data / Improvement 提纲；未修改生成 HTML、讲稿或版本审计。

## 原则

**论文负责讲清机制与可检验结果；Astra community demos 负责展示正在扩展的工作范围。** 不把社区 demo 只堆在结尾，也不为每段视频新增一篇论文介绍。

保留各章原定主线和代表工作，在每章增加一页简短 Astra demo interlude，每页两段视频、一句问题。与既有开场 painting 和结尾 hand design 合计 8 个 community demo 位置；formal report 的实验视频另算。

这些案例支持重新讨论分工与流程边界，不足以单独证明所有流程已被替代，或确认某种未披露的机器人预训练因果。

## 1. Control：从意图 / 示范到可执行行为

安排在 Astra 能力转折之后、同模型 interface 比较之前。新增一页，不插入 Claude / RPent 的旧模型论证内部。

| Demo | 要让观众看到什么 | 必须保留的边界 |
|---|---|---|
| [GPT-Policy-Eval plug insertion](https://github.com/cheng-haha/GPT-Policy-Eval) | 示范 + 在线视觉反馈 → 真实机器人插头操作；展示不依赖独立 VLA 的一条实际路径 | selected trials，没有系统 trial denominator；原视频 12×，不是实时速度或普遍精细操作成功率。 |
| [Keyboard feedback learning](https://x.com/kaiwynd/status/2098823484474348008) | 真实机器人触键、发现输入问题、退格重试；用具体行为展示视觉反馈下的调整 | 作者称 Astra，未给完整模型 snapshot；20× playback，无试验分母，不能当权重更新、RL 或持久化技能的证据。选择错误—退格—重新输入片段前仍需连续审核。 |

字幕只保留任务、Real robot / Simulation、播放倍率和 attribution。这里不再讲方法表与新性能曲线。[Robot hands / Rubik’s cube](https://x.com/ZeYanjie/status/2098118164626501669) 留作可替换的视觉备选：它是一组固定 10-move scramble 的 MuJoCo physics replay，learned-vs-scripted motion 未公开，不能据此称 general zero-shot dexterity 或实机能力，不为它另加页。

## 2. Simulation：从输入素材到整套建模工作

放在 Agentic Real2Sim 方法与正式结果之后、章节总结之前。先让论文的 DROID-100 分母独立成立，再看更自由的 coding-Agent 工作流，不能将两者结果混池。

| Demo | 要让观众看到什么 | 必须保留的边界 |
|---|---|---|
| [Lingxiao / multi-view Real2Sim](https://x.com/Lingxiao234/status/2096992059731443923) | 作者给出 multi-view RGB + robot actions，报告 Astra 组织 camera calibration、assets、system-ID、MuJoCo、Blender；已有 real/sim 对照视频可复用 | 作者报告的工作链，未独立验证物理预测。输入包含 actions，不写“只有视频”；不用 microphone 的 kinematic replay 冒充成功 dynamics。 |
| [Office scan → Newton / G1](https://x.com/Jiarui_X/status/2098439950991806804) | 作者描述 office scan → Blender reconstruction → USD → Newton / G1，视频展示最终场景中的 G1 | 流程来自作者说明，视频不是逐步编辑过程录屏；不能仅看到 humanoid 行走就宣布已经训练了新的 locomotion policy，也不是重建精度验证。 |

这一页的讨论问题是：**Agent 是否正在从执行预先编好的 pipeline，扩展到编写、连接和修补 pipeline 本身？** 作为从案例提出的问题，不声称已有同条件实验量化这一转变。

## 3. Improvement：训练改进与 in-context adaptation 分开看

放在 ENPIRE 正式方法、idea tree 和 learning-curve 论证之后、章节总结之前。两视频不是一个系统的前后对照，而是“经验如何变成行为”两种路径。

| Demo | 要让观众看到什么 | 必须保留的边界 |
|---|---|---|
| [Astra quadruped design + RL](https://x.com/gclue_akira/status/2098300921658868185) | 作者报告 Astra 做 Fusion360 / STL、仿真与 RL 迭代；视频展示 9 种行为的开发预览，而不只是调用现成 policy | 原视频为 Trial 25 的 3×3、14 s preview，明确有部分动作 CUT，以及 FULL EVAL NOT MET；不能说 9 种行为都已通过验证。5 天 / 25 loops 是作者报告，实机部署仍是后续人工计划，不当受控效率评测。 |
| [Physical in-context learning](https://x.com/_wenlixiao/status/2097801944119349455) | 人类示范 → context → robot action，展示不必每次先训练独立 task policy 的探索方向 | 作者报告，已有 motion-planning tools 执行；8× playback、无试验分母。它是 in-context adaptation demo，不能冒称权重训练、跨 rollout 持续 policy improvement 或 ENPIRE 论文的新定量结果。 |

这里的讲解应明确：**训练出新的 policy、修改 controller code、把示范放进 context，都可能改变行为，但不是同一种 post-training。** 把这一区分接回 ENPIRE 的“留下什么产物”问题。

## 4. 开场与 Beyond 保留

- [Painting with feedback](https://x.com/cdngdev/status/2097339677128982873)：维持开场；语义目标 → 机器人笔触 → 人与相机反馈，原作者 timelapse，不称全程无人工介入。
- [Tendon-hand design](https://x.com/earthtojake/status/2097789988670709821)：维持结尾 Beyond；工程设计 / animation，而非已经制造验证的机械手。
- 不再额外展开一个方法章节；应用范围通过视频体现。

## 画面与播放安排

- 新增最多 3 个 demo 页：Control / Simulation / Improvement 各 1 页，每页两段。此前 9 / 5 / 6 页提纲相应变成 10 / 6 / 7；这只是页序提案，尚未计时彩排。
- 保留原章首框图、三张合并的 hierarchy 原图、每章问题/方法/实验/总结。Demo 页不能替代正式架构或结果页。
- 每段原则上选 15–30 秒以内的有意义片段；源视频更短则完整保留。Office 原视频约 5 分钟，本次抽查开头、中间和结尾均为最终 simulation scene 中 G1 的运行；实施时连续核查并选择场景与机器人清晰的一段，不整段塞入讲解，不伪装成已审核的完整构建过程。
- 四足原视频是 3×3 网格，优先全宽/放大播放以保留每格状态标记，不裁掉 FULL EVAL NOT MET 等限制。标题写 RL development preview，不写 nine validated skills。
- 一次主要播放一段，避免两路声音或运动争夺注意；可点击放大。字体、按钮风格、离线内嵌和中文讲稿要求不变。
- 图注区分 Real robot / Simulation / CAD，注明作者、来源、原播放倍率或时延剪除。没有公开倍率就不推断；“我们没再加速”不等于“源视频实时”。
- 原始示范不带完整 model waiting，不能用播放速度推论 LLM latency。

## 现有资产与新源

可直接复用且此次重新核对文件 hash / codec / duration 的本地资产：

- `.build/clips/policy_plug.mp4`：28.17 s，H.264。
- `.build/clips/ze_rubik.mp4`：23.11 s，H.264。
- `.build/clips/astra_real2sim.mp4`：16.77 s，H.264。
- `.build/clips/wenli_icl.mp4`：11.20 s，H.264。
- `.build/clips/painting.mp4`：68.12 s，H.264，后续需要选择讲述片段。
- `.build/clips/hand.mp4`：28.83 s，H.264。

本轮没有改这些 clips。清单见 `research/sources/astra_demo_integration_20260914/existing_asset_inventory.json`。这次 metadata/hash 复核不是新的完整浏览器播放验收；已有 decode/audit 来源仍保留。

新增 office / quadruped / keyboard 的一手 post / media 可用性核查见 [demo shortlist](astra_demo_shortlist_2026-09-14.md)，原视频均已实际加载播放，抽样检查了画面；不是逐秒完整审阅或实验复现。尚未将远端视频嵌入生产 HTML；正式交付前仍需合法来源获取、原倍速确认、剪辑、离线播放与布局检查。

小红书 image-to-duck RL 与 Isaac-PPO 候选当前公开入口需要登录，未取得可核对正文/视频，不为凑数量以二手摘要代替核验，也不绕过访问限制。

## 对三章总结的影响

- Control：旧接口实验是起点；新的直接行为 demo 让 S2 / S1 边界重新成为问题，同模型对照仍决定结论强度。
- Simulation：除了固定工具流程，还出现由 Agent 搭建工程链的展示；验证对象仍须区分 scene/replay 与 predictive simulation。
- Improvement：不仅比较训练算法，也要看 Agent 能否组织实验，以及新模型如何利用 context；training、code revision 和 in-context adaptation 分开表述。

最终想传达的不是“老论文都失效了”，而是 **foundation-model 能力变化后，过去被固定在 pipeline、interface 和训练环节里的分工，都值得重新检验。**
