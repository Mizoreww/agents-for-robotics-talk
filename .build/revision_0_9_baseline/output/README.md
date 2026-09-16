# Agents for Robotics

## 当前本地版本：0.8 · 2026-09-14

- **Agents_for_Robotics_Self_Contained.html**：28 页英文 slides、18 段视频、原图和完整中文讲稿，约 131.8 MB。只需移动这个文件。
- **Speaker_Script_Revised.md**：中文逐页讲稿，专有名词 English；含读图、播放和过渡提示，与内嵌稿一致。
- **Chapter_Spine.md**：三章的问题、方法、结果与总结。

Control（4–13）从原总框图和 Hi Robot / Figure，经过 Claude 实验与 RPent，转入 Astra 新能力与接口比较。Simulation（14–19）围绕 Agentic Real2Sim，Improvement（20–26）围绕 ENPIRE；Astra demos 分布在每章中。27–28 为结构设计与全场总结。

## 操作

- Previous / Next 或左右键翻页；页码菜单直接跳转。
- Play videos / Pause / Restart 控制本页视频，也可用每段视频自己的控件；双 demo 页建议一次播放一段。
- Speaker script / N 显示讲稿；Full script 查看完整稿。
- 点击原图放大，Esc / Close figure 关闭。第 5、12、23 页建议放大讲解；视频用自身 fullscreen 按钮。
- Fullscreen / F 打开演讲视图；浏览器不允许全屏时保留专注视图。Space 播放/暂停。

建议桌面 Chrome / Edge；手机文件预览器可能无法处理约 132 MB HTML 或 H.264。App 内使用本机 loopback 预览，交付 HTML 本身不请求外部资源。60 分钟是建议安排，不是实测时长。

## 边界与历史

数字来自各自的公开实验，不能跨论文排名。Asim budgets 不齐；Direct/Hybrid 同时改变 prior/interface/horizon；Real2Sim 是 replay acceptance；ENPIRE 含 conditional retries。社区 demos 有加速、selected trials 和未通过的 gate；hand 不是物理测试。

旧 PPTX、PDF、ZIP、英文 Speaker_Notes.md 不对应当前页序。本次未发布新 Release。验证状态以项目 `.build/standalone_delivery_audit.json` 和 `.build/standalone_visual_audit.json` 的匹配 hash 为准。

HTML SHA-256：`01505a9c7b51801eb5593b8113fcd3a3b21ca05053e2c79122977d08b9b3b868`。
