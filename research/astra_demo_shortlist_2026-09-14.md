# Astra 工作流变化：新增 demo 候选

核查日：2026-09-14。只做公开来源/媒体检查，**没有改 slides、讲稿或生产素材**，没有调用模型、运行来源项目或登录社媒。主张与视频应分开：demo展示某种产物/行为，不自动验证作者宣称的整个开发过程、泛化率或因果。

## 选择结论

**最值得新增两条：Office scan → simulation，以及Quadruped CAD + RL development。** 一个说明Agent改变环境构建工作流，另一个说明Agent参与设计—训练—修错；均不再展开为第四/第五个论文案例。第三候选可用Keyboard反馈学习，但当前已有physical ICL，优先避免重复。

- Simulation页：既有Lingxiao real2sim + **Office/Newton场景运行结果**。
- Improvement页：**Quadruped九宫格开发预览** + 简洁流程图即可，不必为了凑双视频再混一个in-context learning。
- 页面固定轻标签：`Author-reported demo · Simulation/Real · speed/cuts`；正式研究结果另页讲，不把本列表与论文成功率混表。

## A. 首选：Office scan → Blender / USD → Newton / G1

**作者** Jiarui Xu，@Jiarui_X；2026-09-11。[原帖](https://x.com/Jiarui_X/status/2098439950991806804) · [原MP4，1080p](https://video.twimg.com/amplify_video/2098439638574870528/vid/avc1/1920x1080/aM02cJ2Fu0It7w4P.mp4?tag=29) · [已播放的720p版本](https://video.twimg.com/amplify_video/2098439638574870528/vid/avc1/1280x720/jtX8iCLebZux4cuq.mp4?tag=29)。

- **明确归属**：原帖直接写GPT-6 Astra；X官方oEmbed也返回同一正文，保存为 `office_oembed.json`。
- **作者所述工作流**：给office scan的几张render → Astra重建Blender场景 → export USD → 放进Newton，让G1在场景中行走。**G1 locomotion policy是否新训练、来自何处没有在原帖披露**，不能说Astra训练了该行走策略。
- **媒体实际内容**：303.733s，1920×1080原版；本次检查1s、约152s、302s的画面，都是重建办公室与G1运行的simulation结果。不是已核验的完整scan-to-Blender编辑录屏。
- **不能当作实测数字**：50 desks / 62 chairs / within2cm是作者陈述，未找到匹配/误差定义及独立评测；建议slides不放这些数字，尤其不写“验证2cm物理精度”。
- **剪辑建议**：从前段选20–30s场景内行走/转弯，配一张全景帧。`0–25s`可作初剪候选，正式制作前应连续检查动作是否完整；本次只抽样看帧，没有宣称逐秒审完全片。原帖未披露倍速，标注 `speed not specified`，不拿片长当建设耗时。
- **页面一句话**：`From a scene reference to a runnable simulation asset.` 讲稿强调“工程流水线产物”，不宣称数字孪生动力学已准确。

## B. 首选：Quadruped CAD + RL development preview

**作者** Akira Sasaki，@gclue_akira；2026-09-11。[原帖](https://x.com/gclue_akira/status/2098300921658868185) · [原MP4，1440×1200](https://video.twimg.com/amplify_video/2098297480752607232/vid/avc1/1440x1200/fDFQ9O6Z9JvGebZx.mp4?tag=29) · [已播放的720p版本](https://video.twimg.com/amplify_video/2098297480752607232/vid/avc1/864x720/LTAoxHmb9RVDh6HW.mp4?tag=29)。

- **明确归属**：原帖直接写GPT-6 Astra；X官方oEmbed交叉确认前半正文，完整长文由公开帖子镜像获取。
- **作者所述工作流**：Astra在Fusion360设计机器人、输出STL；用RL迭代并修复每轮问题。作者报5天25loops、九种motions。这些是开发记录描述，不是固定协议benchmark。
- **必须保留的反证边界**：视频标题明确 **`Trial 25 | 3×3 14-second preview | Wave and Sit: partial first cycles (CUT)`**；画面同时有 **`FULL EVAL PASS` 与 `FULL EVAL NOT MET`**（Forward、MoveLeft等可见NOT MET）。因此**不能写“已学会并验证九种技能”**。安全表述是“九种行为的训练/开发预览，部分尚未达标”。
- **媒体角色**：14s仿真九宫格，展示Forward、Backward、MoveLeft、MoveRight、TurnLeft、TurnRight、LieDown、Wave、Sit。画面标注 `4 separate experts`，不能包装成一个统一policy；标注 `50 fps real time`，但Wave/Sit只保留partial first cycles。
- **真实硬件尚未完成**：原帖说第30轮后计划实机调试，下一步尺寸调整与部署需要人类执行；不写sim-to-real成功、无人类干预或已部署实物。
- **剪辑建议**：保留完整14s九宫格，**不要裁掉顶部评测状态**；旁边配 `CAD → train → inspect failures → revise` 小流程图。CAD设计过程本身未在该14s素材中呈现，只能标为作者描述。
- **页面一句话**：`The agent participates in the engineering loop—not every skill is solved.`

## C. 第三候选：Keyboard feedback learning（真实机器人）

Kaifeng Zhang / @kaiwynd，2026-09-12。[原帖](https://x.com/kaiwynd/status/2098823484474348008) · [原MP4](https://video.twimg.com/amplify_video/2098821014465519616/vid/avc1/1920x1080/IP4sVHPj3QwCbR61.mp4?tag=29)。作者原文直接称Astra（未给完整模型snapshot），描述40分钟、误长按、backspace后学会打字；**20× playback明确披露**。本次看过开头、约67s及结尾：真实Franka触键、画面文字“Astra uses Backspace to clear the input”、最终文本。

这展示视觉反馈下行为调整，不证明weight update、RL或可复用skill已持久化；没有trial分母。134.534s源片，可选错误→退格→重新输入的20–30s片段，但需制作时连续确认所选段落。适合Control demo，不要放进post-training作为训练效果。

## 其他五条：可播放，但只作备选

| 候选/原帖 | 可用视频 | 能说明什么 | 不能声称什么 |
|---|---|---|---|
| [G1 cola / Flood Sung](https://x.com/RotekSong/status/2099104628562608371)，09-13 | [27.52s，960×600](https://video.twimg.com/amplify_video/2099104580219117569/vid/avc1/960x600/Odva_XeSxXrVDMF6.mp4?tag=29) | 原帖GPT-6 Codex；simulation画面明确`AGENT → OFFICIAL SONIC PLANNER → SONIC 50Hz → ISAAC G1`，说明现有planner/controller可被Agent组织 | 不是GPT逐关节控制，更不是没有System1；原帖未给trial分母；不把overlay的时序当独立测量 |
| [Mobile ICL / Axel](https://x.com/ax_pey/status/2098216469012283681)，09-11 | [20.7s，1080p](https://video.twimg.com/amplify_video/2098212559770013696/vid/avc1/1920x1080/BC4m4aPH1EDY6cor.mp4?tag=29) | 原帖GPT-6 Astra；真实mobile manipulator，作者称video-context迁移环境/视角/layout，并自主选择EEF或joint space | 没有受控interface ablation、试验分母；“no text prompt”是任务输入描述，不等于无system prompt；倍速未披露 |
| [DexGPT / Xiao Hu](https://x.com/huxiao93612565/status/2097815230105399402)，09-09 | [20.2s，794×720](https://video.twimg.com/amplify_video/2097815161298141184/vid/avc1/794x720/Bz63pAwAG782zssb.mp4?tag=14) | 原帖GPT-6 Astra生成tracking/IK/refinement代码；[开源README](https://github.com/Hu-xiao-max/dexgpt)确有source/kinematic/contact三联视频与记录 | README明确**physical validation criteria not met**：有penetration/force/未标定参数等限制。不能称已获得真实有效机器人训练数据；不是硬件部署 |
| [Vitrus / Lucas Cassiano](https://x.com/lucascassiano/status/2097830777438486557)，09-09 | [70.4s，1080p](https://video.twimg.com/amplify_video/2097828478884429825/vid/avc1/1920x1080/7BMccxFYEHHOqjBx.mp4?tag=29) | 原帖明确GPT-6 Astra、Vitrus OS、simulation pipeline及“新embodiment”主张 | 本次35s抽样画面明确是**Vitrus simulation platform，30× speed**，故不能仅因Awesome归入Real就把视频称纯真机展示；zeroVLA/unseen与部署范围仍是作者声明，不优先选 |
| [Wuji retarget / Lingxiao](https://x.com/Lingxiao234/status/2097717020540481630)，09-09 | [33.9s，1080p](https://video.twimg.com/amplify_video/2097716973899780096/vid/avc1/1920x1080/gsFWFgb-G3egibZw.mp4?tag=16) | 原帖GPT-6、两video输入无states/actions；画面区分source、replay overlay与underlying sim。可说明视频到retarget工程流程 | `physical rollouts`不能翻译成真机rollouts；物理参数/接触有效性与训练效用未独立验证；和现有Lingxiao real2sim内容接近，优先去重 |

## 未纳入：Rednote Duck RL / Isaac-PPO

Awesome链接的 `6aa347e2000000000b036667`（duck）和 `6aa29087000000002600bb2e`（Isaac-PPO）本次HTTP返回网页shell，但嵌入错误为401/缺登录，**没有可核对的正文或媒体URL**。没有绕过、登录或补猜视频地址。仅有聚合仓库描述，不适合在提纲中承诺原视频。

## 来源与播放审计

- 本轮重新抓取[Awesome README](https://github.com/zjwzcx/Awesome-Astra-Embodied-AI)，Git HEAD为 **`61baafd5fc94ae2db32da8da57704310033a6210`**。API限流后使用只读Git ref查询确认，没有clone/安装。
- 全部原帖正文和媒体定位来自公开X帖子镜像API；Office和Quadruped额外用**X官方oEmbed**交叉核对。镜像是传输途径，主张归作者原帖，不把镜像自身当实验作者。
- 上述8条源视频均在Chrome实际加载并播放，currentTime推进、error=null；Office/Quadruped/Keyboard采3帧，其余各1帧。**播放通过不等于已完整审阅、验证任务成功或拥有独立原始实验日志。**
- 记录在 `research/sources/astra_demo_shortlist_20260914/playback_checks.json`；原MP4未下载，只保存公开文本、浏览器画面截图和manifest。源分辨率与实际测试版本可能不同，精确URL在JSON中。
- [三条首选检查帧](sources/astra_demo_shortlist_20260914/top_three_contact_sheet.jpg)；[备选检查帧](sources/astra_demo_shortlist_20260914/backup_contact_sheet.jpg)；[Quadruped不可裁掉的声明](sources/astra_demo_shortlist_20260914/quadruped_header.png)。
