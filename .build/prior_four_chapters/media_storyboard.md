# Media Storyboard：26 页 HTML 版

所有素材内嵌到主 HTML；无需 assets/media 文件夹或联网加载。原始 URL 仅用作主动点击的引用。

| 新页码 | 片段 | 原素材区间 | 时长 | 来源 |
|---:|---|---|---:|---|
| 2 | painting | 0–68.1167s | 68.12s | [original](https://x.com/cdngdev/status/2097339677128982873) |
| 6 | claude_humanoid | 0–5.58333s | 5.58s | [original](https://www.anthropic.com/research/claude-plays-robotics) |
| 6 | claude_manip | 0–4.08333s | 4.08s | [original](https://www.anthropic.com/research/claude-plays-robotics) |
| 9 | astra_bowl | 0–14.3s | 14.30s | [original](https://openai.robocurve.org/gpt-6-astra/) |
| 9 | astra_insertion | 0–13.8s | 13.80s | [original](https://openai.robocurve.org/gpt-6-astra/) |
| 10 | wiping | 0–47.2s | 47.20s | [original](https://x.com/k7agar/status/2096593654320341027) |
| 13 | ar2s_real | 0–10.0833s | 10.08s | [original](https://agentic-real2sim.github.io/) |
| 13 | ar2s_sim | 0–10.0833s | 10.08s | [original](https://agentic-real2sim.github.io/) |
| 16 | astra_real2sim | 0–16.7667s | 16.77s | [original](https://x.com/Lingxiao234/status/2096992059731443923) |
| 16 | astra_microphone | 35–60s | 25.00s | [original](https://x.com/Lingxiao234/status/2096992132527702382) |
| 18 | enpire_task | 300–330s | 30.00s | [original](https://research.nvidia.com/labs/gear/enpire/) |
| 20 | enpire_reset | 0–61.92s | 61.92s | [original](https://research.nvidia.com/labs/gear/enpire/) |
| 20 | enpire_verify | 0–11.1333s | 11.13s | [original](https://research.nvidia.com/labs/gear/enpire/) |
| 24 | hand | 0–28.8333s | 28.83s | [original](https://x.com/earthtojake/status/2097789988670709821) |
| 25 | aspire_trace | 0–30s | 30.00s | [original](https://research.nvidia.com/labs/gear/aspire/) |

15 段 H.264/yuv420p 视频全部保持已有 clip bytes，与原下载剪辑 SHA-256 一致，未额外加速，静音以便现场讲解。源视频自身可能经过剪辑或加速。

Real2Sim 两段配对视频仅用于展示，不代表本演讲做过同步数值误差分析。ENPIRE task video 是 300–330 秒 excerpt。Pin reset 和 zip-tie verifier 来自不同任务。

四个章节均以原生 HTML/SVG 流程图开场（第 5、12、17、23 页），章末讲稿保留简短总结。图片点击可放大；影片按当前页按需解码，离页暂停并释放播放资源。

RPent 原始框架图位于第 11 页，来源为 [官方仓库](https://github.com/RLinf/RPent)。它是简短的工具生态例子；没有新增或伪造 RPent 实验视频。

第 6 页先讲右侧 direct manipulation，再用左侧 controller-code 动画引出接口分工。第 10 页保留 wiping 视频，右侧改为优势与执行缺口；第 11 页以 RPent 收束 Execution。视频内容与速度未改。
