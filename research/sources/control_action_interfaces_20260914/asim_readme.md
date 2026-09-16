# GPT-6 Astra 直接控制机械臂 · 测试面板

静态面板：https://asimfish.github.io/astra-control-dashboard/

内容：实验配置、GPT-6 Astra 收到的图像 / prompt 与返回的 JSON 原文、结果矩阵（脚本上界 / 随机下界 / 三种控制接口 × 三档观测）、每回合回放视频与模型推理轨迹、与 RoboCurve 等外部结果的对照。

由 [asimfish/robocore](https://github.com/asimfish/robocore) 的 `scripts/build_vlm_dashboard.py` 从 `experiments/` 生成：

```bash
cd robocore && python3 scripts/build_vlm_dashboard.py --out ../astra-control-dashboard && cd ../astra-control-dashboard && git add -A && git commit -m "Refresh dashboard" && git push
```

方法与设计见 [robocore/docs/VLM_CONTROL.md](https://github.com/asimfish/robocore/blob/main/docs/VLM_CONTROL.md)。
