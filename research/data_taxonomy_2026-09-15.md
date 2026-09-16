# Data: Assets, Real-to-sim Replay, and Rollout

核查日：2026-09-15。任务仅限一手来源研究；未修改 slides、讲稿或生产 assets，未运行来源项目、实验或模型服务。已加载项目 lessons。WeChat 被阻止的文章不在本次来源中。

## 1. 直接建议

第二类统一叫 **Data**，其内部是三个工作对象，而不是三个新的论文 deep dive：

1. **Assets / environments**：构建可视化、几何、关节模型、场景与机制。
2. **Real-to-sim replay**：将观测到的行为重建、retarget 并在 simulator 中回放。
3. **Data rollout**：执行 policy / controller 得到实际 simulated states、actions、contacts 等时序记录。

三者都可参与 data workflow，但**资产生成 ≠ 已执行 rollout；rollout ≠ 已通过物理验证；通过局部验证 ≠ 已证明训练收益**。不要把所有案例都称作可直接用于训练的高质量数据。

保留 Agentic Real2Sim 作为唯一细讲代表；把最后的 tendon-hand demo 移入 Data 的 **Asset / mechanism reconstruction** 位置即可。Office/Newton 保留为环境资产生成示例；不声称其 G1 locomotion policy 是 Astra 新训练的。

## 2. 用户列表的当前版本

- [Awesome-Astra-Embodied-AI](https://github.com/zjwzcx/Awesome-Astra-Embodied-AI)
- 本次读取的 commit：[`61baafd5fc94ae2db32da8da57704310033a6210`](https://github.com/zjwzcx/Awesome-Astra-Embodied-AI/commit/61baafd5fc94ae2db32da8da57704310033a6210)，committer 时间 `2026-09-14T06:12:39Z`，message `Clarify planning stack in Flood demos`。
- [固定版本 README](https://github.com/zjwzcx/Awesome-Astra-Embodied-AI/blob/61baafd5fc94ae2db32da8da57704310033a6210/README.md#-real-to-sim-replay--data-rollout)；已对照 immutable raw bytes，一致。
- 分类为 Zero-shot Control（10 simulation / 10 real）、Agentic Policy Calls（1）、**Real-to-sim Replay / Data Rollout（6）**、RL environments and training（5）。这不是对所有公开案例的统计调查，不应外推占比。
- Replay / Data Rollout 的六例是 articulated kitchen、Dmytro rope-hand partial reconstruction、Jake tendon-hand design、Lingxiao Wuji retarget、DexGPT、Lingxiao multi-view Real2Sim。
- 列表自身说此类是 “Workflows that reconstruct or replay real-world trajectories, demonstrations, and environments in simulation.” 其命名宽泛；讲稿需要自行把资产、回放和物理 rollout 拆清。

## 3. 当前已有案例：一手证据与边界

### A. Tendon-hand：可以归入 Data 的资产层，不是验证过的 physical rollout

- [Jake 主帖](https://x.com/earthtojake/status/2097789988670709821)：`Astra designed a tendon-driven robot hand`。
- [作者方法说明](https://x.com/earthtojake/status/2097789991426335015)：约 48 小时；`190 STEP files with build123d, animated with javascript, exported to GLB and rendered in a gui`。
- [作者限制说明](https://x.com/earthtojake/status/2097801101890207893)：`Would this model work irl? Def not.`
- 本次用 X 官方 `publish.x.com/oembed` 重新读取三条原文，均成功；不是引用第三方改写。日期为 2026-09-09（UTC 页面日期）。
- **适合页内标签**：`Mechanism / CAD asset`；`Author-reported design; not hardware-validated.`
- **不要沿用列表的强解释**：列表将其描述为 cable-actuated motion reconstruction；原始方法能确认 STEP / JavaScript / GLB 的设计可视化，不能确认经过 tendon-transmission dynamics 验证。
- 保留已有视频即可，无需下载新的 CAD 集合或重新制作视频。

### B. Office scan → Blender / USD → Newton

- [Jiarui Xu 原帖](https://x.com/Jiarui_X/status/2098439950991806804)，X 官方 oEmbed 重新核验。
- 原帖：几张 office scan renders → Blender rebuild → USD → Newton，G1 在其中行走。
- 50 desks、62 chairs、within 2 cm 都是作者声明；没有误差定义、验证协议或 trial denominator。建议不把它们新增为结果表。
- 原帖没有披露 G1 policy 的训练过程或来源，不能把 “humanoid gym” 写成 “Astra 已训练新 humanoid policy”。
- **适合页内标签**：`Scene asset → runnable simulator`；`Training utility not evaluated.`
- 现有视频可继续使用；[原 720p MP4](https://video.twimg.com/amplify_video/2098439638574870528/vid/avc1/1280x720/jtX8iCLebZux4cuq.mp4?tag=29)。本轮只给已记录的媒体 URL，不重新播放或下载。

### C. Multi-view Real2Sim：replay 不等于物理正确

- [Lingxiao 主帖](https://x.com/Lingxiao234/status/2096992059731443923)：输入 multi-view RGB **and robot actions**；camera calibration、assets、physics system-ID、MuJoCo、Blender。
- [microphone 原帖](https://x.com/Lingxiao234/status/2096992132527702382)：`no run retained all three mics`；`kinematic replay, not validated dynamics`；snap-fit clips 需要 compliant contact，rigid proxies 无法表达。
- 两条官方 oEmbed 本次重新核验。不能把该输入说成仅视频，也不能把 microphone replay 作为成功恢复 dynamics 的样例。
- **适合总结短句**：`Visual replay ≠ validated dynamics.`
- 既有 Agentic Real2Sim 正式论文的四 backend 表保留现有审计，不新增实验数值：其 DROID-100 的 accepted 是 replay judging，不是 unseen-action predictive validity，更不是下游 learning benefit。见本项目 `research/data_improvement_results_2026-09-14.md`。

## 4. Data Rollout 最适合的补充：DexGPT（有数据、有明确负面审计）

若需要一个新的、真正能说明 `rollout data` 含义的小例子，优先 **DexGPT**，而不是仅按列表名称认定某个短片已经产生训练数据。它可替换/补充 montage 的一小格，不扩成新 deep dive。

- [X 原帖](https://x.com/huxiao93612565/status/2097815230105399402)：Astra 写 hand tracking、IK retargeting、grasp refinement pipeline；本次 X 官方 oEmbed 核验。
- [项目](https://github.com/Hu-xiao-max/dexgpt)，当前 commit `03ba8a26eaef9dfd272ac1a22c0fd06ccb9b2e5b`，时间 `2026-09-09T22:55:35Z`。
- [固定 README](https://github.com/Hu-xiao-max/dexgpt/blob/03ba8a26eaef9dfd272ac1a22c0fd06ccb9b2e5b/README.md)：monocular GIF → 两只 22-DOF Sharpa Wave hands → MuJoCo passive object hinge。
- 三联视频：**source / kinematic reference with imposed hinge / contact physics with passive hinge**。只有右栏是接触驱动的物体运动；中栏不是物理验证。
- [原比较 MP4](https://raw.githubusercontent.com/Hu-xiao-max/dexgpt/03ba8a26eaef9dfd272ac1a22c0fd06ccb9b2e5b/outputs/comparison.mp4)（README 20.3 s）与[原预览图片](https://raw.githubusercontent.com/Hu-xiao-max/dexgpt/03ba8a26eaef9dfd272ac1a22c0fd06ccb9b2e5b/outputs/comparison_preview.jpg)。本轮未下载或播放，不能称媒体已做最终嵌入 QA。
- README 明确 `physics_rollout.npz` 包含 actual `qpos`, `qvel`, controls、hinge angle、contacts、forces；`retargeted.npz` 是 targets / wrist poses，不能混淆 reference 与实际状态。
- [rollout.py](https://github.com/Hu-xiao-max/dexgpt/blob/03ba8a26eaef9dfd272ac1a22c0fd06ccb9b2e5b/dexgpt/simulation/rollout.py#L66-L85) 用 `mujoco.mj_step` 积分并保存状态；[L120 起](https://github.com/Hu-xiao-max/dexgpt/blob/03ba8a26eaef9dfd272ac1a22c0fd06ccb9b2e5b/dexgpt/simulation/rollout.py#L120) 写 NPZ。只读代码，没有重跑。
- README 的 0.001 s physics step（1000 Hz）和 0.1 s logging（10 Hz）**均不是 Astra inference frequency**。

**必须展示的边界：** README 顶部就是 `EXPERIMENTAL — physical validation criteria not met`。原 [physics_report.json](https://github.com/Hu-xiao-max/dexgpt/blob/03ba8a26eaef9dfd272ac1a22c0fd06ccb9b2e5b/outputs/physics_report.json) 给 `task_success: false`；5.62 mm penetration 超过其 `<5 mm` criterion。203 states 是一条已记录轨迹，不是 203 trials。没有 downstream policy training / transfer benefit。

不推荐把 99.5% contact frames 单独做 headline；它可以同时伴随穿透和大力。比较视频若使用，轻标签至少为 `Contact rollout data; physical validation not met.`

### 备选：Lingxiao Wuji hand-object rollout

- [原帖](https://x.com/Lingxiao234/status/2097717020540481630) 官方 oEmbed 本轮重读：两视频、无 states/actions，要求 Real2Sim + physical retarget to Wuji hands；作者称 `successful physical rollouts`。
- [原 MP4](https://video.twimg.com/amplify_video/2097716973899780096/vid/avc1/1920x1080/gsFWFgb-G3egibZw.mp4?tag=16) 是已有候选记录；本轮未重新下载/播放。
- 公开主帖未给 trial counts、对象动力学一致性或下游训练收益。可讲 author-reported physical replay/retarget；不可据此宣称高质量 dataset 或从视频获得已验证 manipulation policy。
- 若 deck 已经足够拥挤，**不新增**，只用现有案例说明 Data 的更宽覆盖范围即可。

## 5. 稀疏章节框图及总结文案

章首可保留原代表工作的主链，在左/右侧标明 Data 的输入输出，避免画成所有分支都自动成功：

```text
Videos / scans / specifications
                ↓
       Agent + engineering tools
          ↙          ↓          ↘
  Assets / scenes   Replay   Rollout records
          \          |          /
             Validation gate
                    ↓
      Candidate data for training / evaluation
```

`Candidate` 不能省去。箭头表示可组成的工作流，不是所有现有 demo 已走完，也不是当前论文证明的训练收益。

**章末英文三行：**

- `Build assets. Reconstruct behavior. Record rollouts.`
- `Replay quality ≠ physical validity.`
- `Training value still needs downstream tests.`

**中文讲稿建议：**“这里统一叫 Data，因为 Agent 不只是搭一个 simulator。它可以先造场景和机器人资产，再把真实演示变成 replay，或者组织 controller 跑出 states 和 actions。但这三步产物不能混为一谈。机械手 CAD 是资产，视频对齐是 replay，真正积分得到的轨迹才是 rollout；最后还要检查物理可行性，并通过下游训练或评测判断数据有没有用。”

## 6. 本次来源保存

`research/sources/data_taxonomy_20260915/` 保存 16 份只读来源快照及 `manifest.json`（大小、SHA-256）。包括两 repo README / commit、DexGPT tree / physical report / audit / rollout.py、八条 X 官方 oEmbed。仅这些文件与本文属于本子任务；未修改现有来源注册或生产文件。
