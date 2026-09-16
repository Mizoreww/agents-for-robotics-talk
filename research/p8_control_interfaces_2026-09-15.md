# P8 操作 demo 的控制接口核查

核查日期：2026-09-15。范围仅限 P8 两段 demo；未运行第三方机器人代码，也未调用模型服务。已加载项目 lessons，沿用“不从视频外观猜 action interface”的证据规则。

## 可直接用于页面的结论

标题建议：**Astra: More Robot Manipulation Demos**。

两段视频下方均可用浅灰小字：**Control interface: not disclosed**。

不要写成 **IK Goal / EEF target**：本次检查的一手 README 与作者正文均未披露这两段 demo 的 action schema 或执行器。这里的 not disclosed 指所核查公开资料，而非证明作者从未在任何地方披露。

## 左侧：GPT-Policy-Eval / One-Shot Plug Insertion

- [项目 README](https://github.com/cheng-haha/GPT-Policy-Eval/blob/43929f0ee3673da67393fcbe85d43c58eb15db59/README.md)说明：GPT-6 Astra 使用 one video demonstration 与 live visual feedback 指导真实机器人；作者声明 No VLA / No WAM / No RL / No DAgger。
- README 写明 plug insertion 视频为 **12× playback**，这些为 selected individual trials，broader evaluation ongoing。
- 当前 HEAD 仍为 `43929f0ee3673da67393fcbe85d43c58eb15db59`。递归 tree 只有 README（英文、中文）和 assets，**没有控制实现或 API schema**；Code release 仍列为后续事项。
- 因而不能从 No VLA 推断 IK、joint target、OSC、力控制、原子技能，或推断没有底层 Controller。
- README 链接的 [X 帖子](https://x.com/z_code68632/status/2098401554676269236)正文为 mobile manipulation 展示概述，未补充 plug insertion 的控制接口。不能将其当作接口证据。

## 右侧：Kaifeng Zhang / Keyboard

- [作者原帖](https://x.com/kaiwynd/status/2098823484474348008)正文：让 Astra 用键盘表达自己，经过 **40 minutes**、多次意外长按与 backspace；视频 **20× speed**。
- 本次通过 FxTwitter API 重取作者正文，与既有快照文字相同。正文未说明 joint / EEF / IK / primitive / code 接口，也未公布 controller 或逐 query 时间。
- 浏览器入口因 request-header policy 加载失败而不可用；**未能审查 X 回复线程**，不能把当前 finding 说成全站穷尽检索。
- 40 minutes 是作者的整体尝试时间，不是 inference latency；20× 是播放倍率，不是控制频率。

## 讲稿建议

“这一页再看两个真实机器人操作 demo：左边根据一次视频示范完成插头插入，右边尝试使用键盘。这里展示的是能力案例。两位作者在目前查到的公开说明中都没有给出明确的控制 API，因此先不把它们标成 IK Goal；具体接口仍待代码或作者说明确认。”

## 快照与复核

本轮文件：`research/sources/p8_interfaces_20260915/`。`manifest.json`记录来源 URL、时间、字节数与 SHA-256；包含 GitHub repo/tree/commit/README，以及两条作者正文的 API 镜像。公开来源的没有披露，不等于技术上不存在。
