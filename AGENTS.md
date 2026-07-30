# Agent Rules

本文件约束所有维护此 vault 的 Agent。Codex 是默认执行端；其他工具必须遵循同一内容协议。

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

[LEARN] Testing: zsh 脚本禁止把 `path` 用作循环或普通变量。

Mistake: `for path in ...` 覆盖 zsh 特殊数组 `$path`，使后续 `rg`、`git` 无法从 `$PATH` 找到。

Correction: 使用 `required_file` 等任务变量；验证脚本启用 `set -e`，失败后重跑未执行检查。

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

## Vault Content Contract

### Source boundary

- Automatic fetches write only to `02-Sources/Inbox/`.
- Inbox content is unverified source material, not canonical knowledge.
- Canonical knowledge lives under `03-Notes/` and requires primary source, verification date, and review date.

### Learning maturity

Allowed progression:

`seed → practiced → demonstrated → teachable`

- New Agent-generated learning notes start at `seed`.
- Reading or summarizing cannot advance maturity.
- `practiced` requires an experiment or retrieval exercise.
- `demonstrated` requires linked artifact and eval evidence.
- `teachable` requires boundaries, failure cases, and trade-offs.

### Human ownership

- Human-authored notes are user data.
- Never overwrite, delete, or bulk-move human notes without explicit instruction.
- When Agent output conflicts with human notes, preserve both and create a review item.

### Cross-Agent compatibility

- Markdown and YAML frontmatter are system of record.
- Provider-specific commands stay optional.
- Codex, Claude Code, and OpenCode must produce compatible fields.
- Read this file before modifying vault content.

### Privacy

- Never store credentials, company-confidential code, customer data, internal endpoints, or unredacted private traces.
- Public examples use synthetic data.
