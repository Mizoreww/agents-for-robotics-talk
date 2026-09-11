# Media Storyboard：28 页 HTML 版

所有素材内嵌到主 HTML；无需 assets/media 文件夹或联网加载。原始 URL 仅用作主动点击的引用。

| 页码 | 片段 | 原素材区间 | 时长 | 来源 |
|---:|---|---|---:|---|
| 2 | painting | 0–68.1167s | 68.12s | [original](https://x.com/cdngdev/status/2097339677128982873) |
| 6 | claude_humanoid | 0–5.58333s | 5.58s | [original](https://www.anthropic.com/research/claude-plays-robotics) |
| 6 | claude_manip | 0–4.08333s | 4.08s | [original](https://www.anthropic.com/research/claude-plays-robotics) |
| 9 | astra_bowl | 0–14.3s | 14.30s | [original](https://openai.robocurve.org/gpt-6-astra/) |
| 9 | astra_insertion | 0–13.8s | 13.80s | [original](https://openai.robocurve.org/gpt-6-astra/) |
| 10 | wenli_icl | 0–11.2s（作者 8 倍速） | 11.20s | [original](https://x.com/_wenlixiao/status/2097801944119349455) |
| 10 | arx_knob | 0–15.33s（作者 16 倍速） | 15.33s | [original](https://x.com/ARXrobotics/status/2096328304794210604) |
| 11 | ze_rubik | 0–23.1s（MuJoCo replay） | 23.11s | [original](https://x.com/ZeYanjie/status/2098118164626501669) |
| 11 | juggle | 0–5.27s（MuJoCo 1×） | 5.27s | [original](https://x.com/thermalpastor/status/2097496200631210136) |
| 12 | show_harness | 39–72s | 33.00s | [original](https://x.com/ZechenBai/status/2097879130356498603) |
| 14 | xhs_piper | 0–41.4s（作者 70 倍速） | 41.43s | [original](https://www.xiaohongshu.com/explore/6a9bd4c80000000028037f67) |
| 16 | ar2s_real | 0–10.0833s | 10.08s | [original](https://agentic-real2sim.github.io/) |
| 16 | ar2s_sim | 0–10.0833s | 10.08s | [original](https://agentic-real2sim.github.io/) |
| 19 | astra_real2sim | 0–16.7667s | 16.77s | [original](https://x.com/Lingxiao234/status/2096992059731443923) |
| 19 | astra_microphone | 35–60s | 25.00s | [original](https://x.com/Lingxiao234/status/2096992132527702382) |
| 21 | enpire_task | 300–330s | 30.00s | [original](https://research.nvidia.com/labs/gear/enpire/) |
| 23 | enpire_reset | 0–61.92s | 61.92s | [original](https://research.nvidia.com/labs/gear/enpire/) |
| 23 | enpire_verify | 0–11.1333s | 11.13s | [original](https://research.nvidia.com/labs/gear/enpire/) |
| 26 | aspire_trace | 0–30s | 30.00s | [original](https://research.nvidia.com/labs/gear/aspire/) |
| 27 | hand | 0–28.8333s | 28.83s | [original](https://x.com/earthtojake/status/2097789988670709821) |

20 段 H.264/yuv420p 视频，合计约 459 秒。14 段沿用上一版 clip bytes（SHA-256 与 `output/offline_player/media_credits.json` 一致）；6 段为 2026-09-11 新增社区视频（`.build/clip_manifest_v2.json`），全部静音，未额外加速；作者原视频自带的倍速在页面标注。上一版的 wiping 片段已移除。

社区视频均为作者自述 demo：无 trial 统计，不作为定量证据。Yanjie Ze 魔方为 MuJoCo physics replay；抛接为 MuJoCo 1×；小红书 Piper 视频含三次抓取失败后的重试。Show-Harness 片段取项目视频 39–72 秒（"One VLM agent · zero-shot or fine-tuned" 至 "Out of the lab"）。

Real2Sim 两段配对视频仅用于展示，不代表本演讲做过同步数值误差分析。ENPIRE task video 是 300–330 秒 excerpt。Pin reset 和 zip-tie verifier 来自不同任务。

三个部分均以原生 HTML/SVG 流程图开场（第 5、15、20 页）。图片点击可放大；影片按当前页按需解码，离页暂停并释放播放资源。RPent 原始框架图位于第 13 页，来源为 [官方仓库](https://github.com/RLinf/RPent)。
