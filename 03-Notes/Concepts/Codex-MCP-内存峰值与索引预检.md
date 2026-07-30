---
type: concept
title: Codex MCP 内存峰值与索引预检
created: 2026-07-30
updated: 2026-07-30
status: active
tags: [codex, mcp, performance, obsidian, incident-review]
last-verified: 2026-07-30
review-after: 2026-10-30
---

# Codex MCP 内存峰值与索引预检

## 结论

Codex 卡顿不一定来自主进程泄漏。全仓索引、子 Agent、每会话 MCP 服务会叠加内存；Obsidian 插件中的打包 JavaScript 会放大索引成本。

## 2026-07-30 现场数据

- 机器内存：16 GiB。
- Codex 核心进程 RSS：约 1.7 GiB。
- MCP 与工具进程 RSS：约 0.8 GiB。
- 合计：约 2.5 GiB。
- Swap 已用：约 5.76 GiB。
- 索引峰值时 `codebase-memory-mcp` RSS：约 727 MiB。
- Codex Renderer 同期 CPU：约 40%。
- `.obsidian/plugins/obsidian-excalidraw-plugin/main.js`：约 8 MiB 打包文件。
- Appium、Figma、code review、PPT 等 MCP 出现重复实例。

权限确认界面只是卡顿发生位置。主要负载来自索引、Renderer 和重复 MCP。

## 根因

1. 对 Markdown 为主的 vault 执行 moderate 全仓代码图谱索引。
2. 索引范围包含 `.obsidian/plugins/**` 第三方打包代码。
3. 后台研究 Agent 启动独立工具上下文，复制 MCP 服务。
4. Renderer 同时承载长对话和大段工具输出。
5. macOS 压缩内存与 Swap 让索引结束后的卡顿继续存在一段时间。

## 防复发规则

### 索引

- Markdown、YAML、模板、MOC：优先 Obsidian、Dataview、`rg`。
- 只有分析自有代码定义、调用链、数据流时使用代码图谱。
- 索引前排除：
  - `.obsidian/plugins/`
  - `.git/`
  - `.venv/`
  - `99-Archive/`
  - `node_modules/`
  - 生成物、vendor、压缩包、大型单文件 bundle

### 并行 Agent

- 先判断子任务是否真正独立、是否节省总时间。
- 启动前检查 MCP 是否按 Agent 复制。
- 内存紧张或任务轻量时保持单 Agent。
- 子任务完成后检查重复服务是否退出。

### 诊断安全

- 不输出完整进程命令行。
- 只保留 PID、CPU、RSS、短进程名。
- 对 token、API key、URL 参数、环境变量统一脱敏。
- 凭证出现在进程参数或仓库后，执行删除、配置改造、轮换。

## 执行前检查表

- [ ] 目标是代码关系分析，不是 Markdown 内容检索
- [ ] 已检查目录总体积和最大文件
- [ ] 已定义索引包含范围
- [ ] 已排除第三方插件、归档、生成物
- [ ] 已检查系统内存压力和 Swap
- [ ] 已检查正在运行的 Agent 与 MCP 数量
- [ ] 进程诊断不会输出凭证
- [ ] 已定义任务结束后的资源回收检查

## 处理顺序

出现明显卡顿时：

1. 停止新增索引和并行任务。
2. 等待当前索引退出，观察 RSS 是否下降。
3. 结束不需要的子 Agent 和 MCP。
4. 卡顿持续时重启 Codex，回收 Renderer 与工具子进程。
5. 复盘索引范围，更新 [[AGENTS]] 规则。

## 关联

- [[AI-Agents-MOC]]
- [[mcp-session-lifecycle]]
- [[claude-code-hook-performance]]
