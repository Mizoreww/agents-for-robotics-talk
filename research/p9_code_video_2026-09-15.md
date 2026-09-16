# P9 Code → waypoints 视频核实（2026-09-15）

## 结论
已找到 **同一 GPT-6 Astra / Square / proprio / prompt v3 / 2026-09-08 矩阵** 的真实 Code → waypoints 视频，不需要使用其他接口视频替代。

- [原始 dashboard](https://asimfish.github.io/astra-control-dashboard/#sec4)
- [固定版本原始 HTML](https://github.com/asimfish/astra-control-dashboard/blob/1e7952c26e0a8783e4eca48514b3a1cc03e2c5df/index.html)
- [原视频](https://asimfish.github.io/astra-control-dashboard/media/Square__code__proprio__codex-gpt-6-astra__s0__20260908T142029Z/ep00.mp4)

## 身份与实验口径
固定 HTML 在“程序接口（code）”处明确：模型返回 Python `plan(scene)`，在受限命名空间执行成 waypoint sequence；失败后向模型反馈执行结果以修改程序。展示输入为 `Square__code__proprio__codex-gpt-6-astra__s0__20260908T142029Z` 的 ep00 第1次查询。

同一 HTML 的视频条目紧接以下分组标题：
`code · 写 plan(scene) 程序，按反馈修改 × proprio · 图像 + 本体状态 + 相机标定 — gpt-6-astra：16/20`，机器 bjxy_5090（2×RTX 5090），seed 0，prompt v3。

视频对应 episode 00：作者标记成功，125 environment steps，1 query，9442 tokens，episode time 42.42 s；该次 query 41.339 s。最近距离 0.0066 m、最大抬高0.2267 m、终点离目标0.5 cm，均为来源自报。

这是 MuJoCo / robosuite / robomimic Square 的模拟机器人，并非真实机器人录像。proprio 并非纯 RGB（还有本体状态和相机标定；现有项目证据亦指出 visual markers / fixed references）。同模型不代表不同接口具有完全相同的控制步数或查询预算。

## 资产与验证
- 视频：`.build/assets/v0_13_code/asim_square_code_proprio_ep00.mp4`
- 采集与 ffprobe 元数据：`.build/assets/v0_13_code/capture.json`
- 本地下载为源 URL 原字节，无剪辑、转码、变速。
- SHA-256：`beff2d66b6b6454652c19e9229c35183eff75e026671b06749bdbaaf57d981ef`
- 129722 bytes；H.264 High / yuv420p；256 × 256；10 fps；64 frames；6.4 s；无音轨。
- 全文件 ffmpeg decode 成功，并检查3秒帧为机器人夹持 square nut 的场景。
- **6.4 s 是视频播放时长，不是42.42 s 的 episode wall-clock，也不是41.339 s 的模型 query latency。**
- 固定 HTML 本地 SHA：`50af836616bef6dfaed22e142702d37da7e5884c85954e9cb9ae3e7d685d4851`。

## 页面建议
P9 第三张卡可用该视频替代静态 Code → waypoints 图示，保持同一模型/interface exploration 的叙述。灰色小注可写 `Python plan(scene) → waypoints`。不把播放速度当作实时推理频率；小样例成功也不代表该接口整体最优（该来源分组为16/20）。

未修改任何幻灯片生成器、数据 pin 或主 manifest。
