# Agents for Robotics

## 当前版本：单文件 HTML + 中文讲稿（0.5，2026-09-11）

- **Agents_for_Robotics_Self_Contained.html**：28 页英文幻灯片，3 个细讲标杆，20 段视频，原始论文图，3 张章首流程图（第 5、15、20 页）。图片、视频、中英文字体、样式、脚本与中文讲稿全部内嵌。文件约 132 MB。
- **Speaker_Script_Revised.md**：中文逐页讲稿；论文名、模型名及技术术语保留英文。含建议时间、读图说明、播放提示和来源。与 HTML 内嵌讲稿一致。

全场分三个部分：Agent Controls Robot（5–14）、Agent Produces Data（15–19）、Agent Post-trains Robot（20–26），每部分以流程图开场；结尾一页机械手结构设计放在三个角色之外，再总结。第一部分新增 GPT-6 Astra 发布后一周内 X 与小红书的社区 demo（Yanjie Ze 的 MuJoCo 魔方、MuJoCo 双机器人抛接、Wenli Xiao 的 human video → arm、ARX 旋钮、小红书 Piper 抓放）、Show-Harness 接口研究，以及"Gaps and Directions"一页总结当前不足与方向。仍然只细讲三个标杆。

只需移动 HTML 本身，无需 ZIP 或配套文件夹。建议用桌面 Chrome / Edge 等现代浏览器打开；手机文件管理器内置预览未必支持大 HTML 或 H.264 播放。

## 操作

- Previous / Next 或左右方向键翻页；页码菜单可直接跳转。
- Play videos 播放当前页；Pause 暂停；Restart 从头开始。也可使用单个视频自身的播放控件。
- Speaker script 显示当前页中文讲稿。Full script 切到整篇，Current slide 返回逐页。
- 点击论文图查看大图，Close figure 或 Esc 关闭。
- Fullscreen / F 打开更大的演讲视图。浏览器允许时同时请求原生全屏；内嵌预览器不支持时保留专注视图。Exit view 返回。
- N 切换讲稿，Space 播放/暂停。键盘焦点在页码菜单时，保留菜单自身的键盘行为。

60 分钟为包含视频、读图和短互动的建议安排，实际时长请以彩排为准。资料截点为 2026-09-11。社区 demo 均为作者自述、有倍速、无 trial 统计，不等于重复实验；关键分母、retry 及人工准备条件见讲稿。

## 历史版本（保留，不是当前页序）

以下文件对应旧 22 页版本，未随 28 页 HTML 版重排：
- Agents_for_Robotics_Focused.pptx
- Agents_for_Robotics_Static_Preview.pdf
- Agents_for_Robotics_Offline_Player.zip / offline_player
- Speaker_Notes.md（旧英文笔记）

本次修订说明（2026-09-11）：内容、页序、内嵌资源与中文讲稿已同步，静态检查与打印引擎渲染已完成。浏览器播放/交互/移动端复测的状态以 `.build/standalone_delivery_audit.json` 的 `browser_audits` 字段为准。播放器代码未改；沿用的 14 段视频字节未改。
