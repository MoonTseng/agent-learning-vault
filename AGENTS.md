# Agent Rules

本文件约束所有维护此 vault 的 Agent，包括 Codex、Hermes、Claude Code、OpenCode。

## LEARNED

[LEARN] Performance: Obsidian/Markdown 仓库禁止直接执行全仓代码图谱索引。

Mistake: 索引包含 `.obsidian/plugins/**` 打包 JS，造成内存峰值与 Swap。

Correction: 先检查目录体积；优先 Markdown 搜索；必须索引时排除插件、生成物、vendor、archive。

[LEARN] Performance: 启动子 Agent 前检查 MCP 复制成本与系统内存。

Mistake: 后台 Agent 复制整套 MCP 服务，Codex 总占用约 2.5 GiB。

Correction: 轻量研究优先当前 Agent；确需并行时减少 MCP、限制并发、结束后确认子进程释放。

[LEARN] Security: 进程诊断输出必须过滤命令行凭证。

Mistake: `ps` 完整命令可能暴露 MCP token。

Correction: 展示进程前脱敏参数；公开仓库前执行密钥扫描并轮换已暴露凭证。

## Resource Preflight

执行索引、并行 Agent、批量抓取前：

1. 用 `du` 检查目标目录和最大文件。
2. 排除 `.obsidian/plugins/`、`.git/`、`.venv/`、`99-Archive/`、生成物和第三方依赖。
3. 检查当前 Agent 数、MCP 进程数、内存压力和 Swap。
4. 估算每个子 Agent 是否会复制 MCP 服务；收益不足时保持单 Agent。
5. 任务结束后检查临时进程是否释放。

## Safe Diagnostics

- 进程输出只展示 PID、CPU、RSS、进程名；禁止展示完整参数。
- 日志、配置、环境变量、URL 查询参数进入对话或笔记前必须脱敏。
- 发现硬编码凭证时，不复制值；记录文件位置，要求删除并轮换。
