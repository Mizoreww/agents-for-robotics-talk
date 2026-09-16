# Agents for Robotics

## 当前本地版本：0.7 · 2026-09-14

- **Agents_for_Robotics_Self_Contained.html**：21 页英文 slides、9 段视频、论文/项目原图、章节框图及完整中文讲稿。约 99.9 MB；只需移动这一个 HTML，无需 ZIP 或资源目录。
- **Speaker_Script_Revised.md**：中文逐页讲稿，专有名词用 English；含播放、读图、过渡、建议时间和参考来源。与 HTML 内嵌讲稿一致。
- **Chapter_Spine.md**：三章各自的问题、方法、实验结果与局限，可用于快速复习。

Control（4–8）只细讲匿名 Direct/Hybrid 报告；第 5 页简述 Claude Plays Robotics 和 RPent。Data（9–13）只讲 Agentic Real2Sim；Improvement（14–19）只讲 ENPIRE。章节以框图开始，并各自总结。第 20 页为 structural design demo，第 21 页为全场总结。

## 操作

- Previous / Next 或左右方向键翻页；页码菜单可直接跳转。
- Play videos 播放当前页；Pause 暂停；Restart 从头开始。也可使用视频自身的控件。
- Speaker script 显示当前页中文讲稿；Full script 切换完整讲稿，Current slide 返回逐页。
- 点击论文图查看原图，Close figure 或 Esc 关闭。第 4 页原架构图建议放大讲解。
- Fullscreen / F 打开演讲视图；浏览器允许时请求原生全屏，否则保留专注视图。Exit view 返回。
- N 切换讲稿，Space 播放/暂停；页码菜单获得焦点时保留菜单自身键盘行为。

60 分钟是建议时长，尚未彩排。建议使用桌面 Chrome/Edge；手机文件预览器可能不能打开约 100 MB 的 HTML 或播放 H.264。App 内通过本机 loopback 预览，交付 HTML 本身不请求外部资源。

## 证据与历史版本

Direct/Hybrid 比较不隔离 prior 的因果作用，两个视频是不同仿真任务且省略 LLM 等待。Real2Sim 指标是 replay acceptance；ENPIRE success 含 conditional retries。Hand 不是物理验证过的机械手。详细边界见讲稿与章节提纲。

旧 22 页 PPTX、PDF、ZIP 和英文 Speaker_Notes.md 未随本次重排，不对应当前页序。本次未发布新 GitHub Release。

验证状态见项目 `.build/standalone_delivery_audit.json`。HTML SHA-256：`cccec9692b6470391539624e016cce0ee7860c3b0f4ebb8c3b0b8ac315cbd602`。
