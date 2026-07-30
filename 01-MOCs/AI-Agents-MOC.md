---
type: moc
title: AI Agents
updated: 2026-07-30
---

# AI Agents MOC 🤖

我对 AI agent 生态的持续跟踪。重点：for 移动端开发，但不限于。

## 系统学习

- [[Agent-Learning-Roadmap]] — 九模块能力路线、碎片任务、复习和作品证据
- [[03-Notes/Concepts/Agent-Loop-与-Tool-Contract]] — 当前 M1 试点

## 我在用的 Agent

- [[03-Notes/Agents/hermes-agent|Hermes Agent]] — 本地主 agent，tool calling + skill 系统
- [[03-Notes/Agents/claude-code|Claude Code]] — 代码任务为主
- [[03-Notes/Agents/codex|Codex]]
- [[03-Notes/Agents/opencode|OpenCode]]

## Skills（按评分排序）

```dataview
TABLE rating, status, platform, last-verified
FROM "03-Notes/Skills"
WHERE type = "skill"
SORT rating DESC
```

## MCP Servers

```dataview
TABLE status, last-verified
FROM "03-Notes/MCPs"
WHERE type = "mcp"
SORT last-verified DESC
```

## 核心概念

- [[03-Notes/Concepts/context-engineering|Context Engineering]]
- [[03-Notes/Concepts/harness|Harness / Agent Harness 原理]]
- [[03-Notes/Concepts/tool-use|Tool Use]]
- [[03-Notes/Concepts/rag|RAG]]

## 待探索（Inbox）

```dataview
LIST
FROM "02-Sources/Inbox"
WHERE contains(tags, "ai-agent")
SORT file.ctime DESC
LIMIT 15
```
