# Agent Learning Vault 🧭

 Agent 工程学习知识库模板。基于 Obsidian、纯 Markdown 和跨 Agent 维护协议。

## 它解决什么

普通资料库解决“保存在哪里”。Agent Learning Vault 继续解决：

1. **现在学什么**：路线图按 10/25/60 分钟展示下一任务。
2. **是否真正掌握**：知识按 `seed → practiced → demonstrated → teachable` 晋升。
3. **哪些内容过期**：用 `last-verified`、`review-after`、`volatility` 管理变化。
4. **面试能证明什么**：代码、Trace、Eval、Threat Model 汇总为作品证据。

```text
官方源 → Inbox 候选 → 验证/实验 → 正式笔记 → Lab/Eval → 复习与作品
```

自动化只负责发现，不直接覆盖正式知识。

## 开始使用

1. 用 Obsidian 打开 vault。
2. 启用 Dataview；需要模板时启用 Templater。
3. 打开 `01-MOCs/Agent-Learning-Roadmap.md`。
4. 从 `Next` 选择符合当前时间的任务。
5. 首个试点：`03-Notes/Concepts/Agent-Loop-与-Tool-Contract.md`。

路线图提供：

- `Next`：下一学习动作。
- `Due`：需要复习的知识。
- `Stale`：需要重验的高波动知识。
- `Portfolio`：已有 Artifact 和 Eval 的求职证据。

## 目录约定

```
01-MOCs/        各主题的索引页（Map of Content）
02-Sources/     原始信息
  Inbox/        自动抓取的 raw，待分拣
  Blogs/        已归档的原文摘录
03-Notes/       验证后的原子笔记（解释、边界、实验、证据）
  Skills/       AI agent skill 一页一个
  MCPs/         MCP server 一页一个
  Agents/       Hermes / Claude Code / Codex / OpenCode 等
  Mobile-AI/    Android / Flutter 里怎么用 AI
  Concepts/     Context Engineering / Harness / RAG / Tool Use …
04-Projects/    短期项目（PARA 的 P）
05-Ideas/       赚钱 idea pipeline：Seeds → Validating → Building → Shipped / Killed
06-Daily/       日志
99-Archive/     冷冻
_templates/     新建笔记用模板
_attachments/   图片等
```

## 运行节奏

- 每日：cron 扫官方源，高分候选写入 `02-Sources/Inbox/`。
- 每周：处理 breaking、安全、Eval 变化；完成一个最小实验。
- 每月：处理 `review-after`，重验高波动笔记。
- 每季度：按目标岗位和实践结果调整路线。

阅读不能直接标记掌握。正式知识必须有一手来源；`demonstrated` 必须有 Artifact 和 Eval。

## 查询知识

直接问 Agent：「vault 里有没有 xxx 的笔记？」

Agent 应先读 `AGENTS.md`，再搜索 MOC、Notes 和 Projects。

## 用任意 Agent 维护

Codex 为当前主用 Agent；Hermes、Claude Code、OpenCode 可按同一协议维护。

1. 先读根目录 `AGENTS.md`。
2. 自动抓取只写 `02-Sources/Inbox/`。
3. 验证后的原创知识写 `03-Notes/`。
4. 学习证据写 `04-Projects/agent-labs/`。
5. 不用某个 Agent 私有数据库承载 canonical knowledge。

## 设计资料

- `docs/superpowers/specs/2026-07-30-personal-agent-knowledge-vault-design.md`
- `docs/superpowers/plans/2026-07-30-personal-agent-knowledge-vault.md`
- `research/agent-learning-landscape-2026.md`

## 不放进 vault 的东西

- 密钥、token、客户敏感信息
- 大体积二进制（> 10MB 的视频/数据集，用 git-lfs 或外部链接）
- 公司或客户未公开项目的源码片段
