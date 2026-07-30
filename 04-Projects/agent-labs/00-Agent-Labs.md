---
type: project
title: Agent Labs
status: active
created: 2026-07-30
updated: 2026-07-30
tags: [ai-agent, labs, portfolio]
---

# Agent Labs

Agent 学习证据区。每个 Lab 必须留下可运行结果、失败记录和验收证据。

## M1：最小 Tool Loop

关联：[[03-Notes/Concepts/Agent-Loop-与-Tool-Contract]]

### 必交付

- [ ] 框架无关的最小循环
- [ ] calculator 工具 schema
- [ ] 未知工具、参数错误、超时、重复调用测试
- [ ] `max_steps` 和明确终态
- [ ] 一条成功 trace
- [ ] 一条失败 trace
- [ ] 一页取舍说明

### 验收

- 测试可以重复运行。
- 失败不会进入无限循环。
- Trace 能定位每次模型决策和工具结果。
- README 能让未来的自己在 10 分钟内恢复上下文。

## 作品证据

```dataview
TABLE module AS "模块", maturity AS "成熟度", artifact AS "产物", eval AS "Eval"
FROM "03-Notes"
WHERE type = "learning-node" AND contains(list("demonstrated", "teachable"), maturity)
SORT module ASC
```
