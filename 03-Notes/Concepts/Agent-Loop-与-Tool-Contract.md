---
type: learning-node
title: Agent Loop 与 Tool Contract
module: M1
maturity: seed
timebox: 25
volatility: medium
prerequisites: []
created: 2026-07-30
updated: 2026-07-30
last-verified: 2026-07-30
review-after: 2026-08-06
source-of-truth:
  - https://www.anthropic.com/engineering/building-effective-agents
  - https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/
artifact: "[[04-Projects/agent-labs/00-Agent-Labs|Agent Labs]]"
eval:
next-action: 手写 calculator 工具 schema，并定义 4 个失败用例
recall-prompts:
  - 模型、Harness、工具执行器分别负责什么？
  - Agent Loop 必须具备哪些停止条件？
  - 为什么工具结果也属于不可信输入？
tags:
  - ai-agent
  - tool-use
  - learning
---

# Agent Loop 与 Tool Contract

## 学习目标

脱离框架解释 `observe → decide → act → observe` 循环，以及模型、Harness、工具执行器之间的责任边界。

## 10 分钟

不看资料回答三个 Recall 问题。不会的部分写成疑问，不补抄定义。

## 25 分钟

设计 calculator 工具 schema，并覆盖：

1. 未知工具名。
2. 参数类型错误。
3. 工具超时。
4. 重复调用。

## 60 分钟

实现最小循环；保存结构化 trace；增加 `max_steps`、明确终态、重复调用检测。

## 晋升门槛

- `practiced`：calculator schema 和四个失败用例完成。
- `demonstrated`：最小循环可运行，测试通过，trace 已保存。
- `teachable`：能解释循环边界、停止策略、错误策略和框架取舍。

## 当前理解

Agent 不是一段 Prompt。Agent 是模型决策、状态、工具执行、终止条件、错误处理和观测共同组成的系统。

## 学习记录

闭卷回答和纠错写入当天 `06-Daily`，并链接本笔记。下面自动展示相关记录：

```dataview
LIST
FROM "06-Daily"
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## 下一步

手写 calculator 工具 schema，并定义 4 个失败用例。
