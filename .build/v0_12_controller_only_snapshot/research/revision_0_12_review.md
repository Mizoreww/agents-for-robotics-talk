# v0.12 审核记录

日期：2026-09-15。固定对照：`.build/revision_0_12_baseline/manifest.json`，即已验证 v0.11；不是 Git HEAD。
最终 HTML SHA-256：`c6ca5f7082a5b91f10387401e2405b2fc0c707d92814b9848f0ba035308c3ba1`。

## 实际范围

第6页 Hi Robot 结果替换为稀疏职责迁移图，末端按用户最新要求只写 Controller。保持第5页原架构、38页页序、18段媒体、其余数字与证据边界。Control 中文讲稿及过渡同步，英文字体与播放器样式不变。

## Standards

0 项 findings。独立审查未发现 documented-standard 违规或值得报告的 code smell。生成源、原有视觉风格、离线媒体约束及来源校验保持一致。

## Spec

0 项 findings。独立审查确认图以两条链和单一箭头表达 Partial shift，Controller-only 命名已落实。讲稿明确 generalist 是目标、迁移是部分的、analytic tools 不等于 learned System 1、Astra 训练因果未披露。只有第6页画面变化。

## 验证

- 14 项单元测试通过，13项冻结来源的结果推导通过。
- 完整 validator 通过：38页、18视频、36图像、4种内嵌字体，中文独立稿与内嵌稿一致，无外部运行时资源。
- 38页 layout 无文字 overflow、无缺图；所有18 clips play/pause/restart通过。
- 10次原图放大检查；5段选定clips完整连续播放通过。桌面/手机按钮与讲稿检查通过。
- HTTP流式hash在浏览器运行前后相同，并独立绑定实际加载的deck-data DOM，未通过CDP搬运大文件。
- 已人工查看最终职责迁移图及桌面/手机控制条，无文字或箭头遮挡；其他静态页截图保持一致。
- 审核后的最终文档变更只关闭pending状态并附预览路径，未改变HTML或讲稿。

证据：`.build/standalone_delivery_audit.json`、`.build/standalone_visual_audit.json`、`.build/v0_12_extended_audit.json`。
本次没有新web研究、模型服务调用、实验复现、push/Release或历史PPTX/PDF/ZIP更新。60分钟为建议安排，未彩排计时。
