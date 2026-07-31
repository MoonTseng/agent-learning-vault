---
type: moc
title: Agent Learning Roadmap
created: 2026-07-30
updated: 2026-07-30
status: active
tags: [ai-agent, learning-roadmap]
---

# Agent Learning Roadmap

Agent Learning Vault 学习入口。目标：碎片时间持续推进，知识能复习，实践能验证，产物能用于求职。

## 现在做什么

### Next

```dataview
TABLE module AS "模块", timebox AS "分钟", maturity AS "成熟度", next-action AS "下一步"
FROM "03-Notes"
WHERE type = "learning-node" AND next-action
SORT timebox ASC, file.mtime DESC
```

### Due

```dataview
TABLE module AS "模块", maturity AS "成熟度", review-after AS "复习日期"
FROM "03-Notes"
WHERE type = "learning-node" AND review-after AND review-after <= date(today)
SORT review-after ASC
```

### Stale

```dataview
TABLE module AS "模块", volatility AS "波动", last-verified AS "上次验证", review-after AS "重验日期"
FROM "03-Notes"
WHERE type = "learning-node" AND (status = "stale" OR (volatility = "high" AND review-after AND review-after <= date(today)))
SORT review-after ASC
```

### Portfolio

```dataview
TABLE module AS "模块", maturity AS "成熟度", artifact AS "产物", eval AS "Eval"
FROM "03-Notes"
WHERE type = "learning-node" AND contains(list("demonstrated", "teachable"), maturity) AND artifact AND eval
SORT module ASC
```

### Inbox Shortlist

```dataview
TABLE triage-score AS "分数", triage-module AS "模块", triage-next-action AS "下一步", takeaway AS "一句话"
FROM "02-Sources/Inbox"
WHERE status = "highlight" AND triage-score
SORT triage-score DESC, file.mtime DESC
LIMIT 10
```

## 能力路线

| 模块 | 能力 | 晋升证据 |
|---|---|---|
| M0 | 场景判断与 LLM I/O | Agent/not-Agent ADR、结构化输出测试 |
| M1 | Agent Loop 与 Tool Contract | 裸 Loop、Trace、工具测试 |
| M2 | Context、Retrieval、Memory | Retrieval Eval、Memory Policy、冲突测试 |
| M3 | Harness 与可恢复执行 | 状态图、Checkpoint/Resume、故障矩阵 |
| M4 | Evaluation 与 Observability | Eval 集、版本对比、失败分类 |
| M5 | Security、Identity、Human Control | Threat Model、对抗测试、权限策略 |
| M6 | Skills 与 Agent Protocols | Skill、MCP Demo、协议边界说明 |
| M7 | Planning、Delegation、Multi-Agent | 单/多 Agent 对照、Ownership Contract |
| M8 | 专项 Agent 与生产交付 | 可运行作品、Eval、Trace、限制说明 |

当前入口：[[03-Notes/Concepts/Agent-Loop-与-Tool-Contract]]

## 碎片时间协议

| 时间 | 动作 | 输出 |
|---:|---|---|
| 10 分钟 | Recall 或检查一个官方 delta | 回忆、疑问、更新候选 |
| 25 分钟 | 最小实验、一个 Eval、一次 Trace 阅读 | Diff、结果、失败、下一步 |
| 60 分钟 | 集成、故障注入、作品改进 | 可运行增量、对比、图或报告 |

中断时必须保存：

1. 当前假设。
2. 已得结果。
3. 一个 `next-action`。

## 每周最小闭环

- 周一 10 分钟：Recall；选择一个真实问题。
- 周二 25 分钟：最小实现。
- 周三 25 分钟：读 Trace；标记失败。
- 周四 25 分钟：故障注入或安全测试。
- 周五 10 分钟：看官方变化。
- 周末 60 分钟：集成、Eval、Teach-back。

## 官方 Watchlist

自动 RSS：

- Anthropic News
- OpenAI News
- A2A Releases
- OWASP GenAI Security

每月人工检查：

- [MCP specification](https://modelcontextprotocol.io/specification/latest)
- [MCP blog](https://blog.modelcontextprotocol.io/)
- [A2A specification](https://a2a-protocol.org/latest/specification/)
- [ACP updates](https://agentclientprotocol.com/updates)
- [Agent Skills specification](https://agentskills.io/specification)
- [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/)
- [Google ADK](https://google.github.io/adk-docs/)
- [NIST AI](https://www.nist.gov/artificial-intelligence)

自动抓取只进 `02-Sources/Inbox/`。验证通过后才更新 `03-Notes/`。

## 研究依据

- [[research/agent-learning-landscape-2026|Agent AI 学习路线与开放知识库定位（2026）]]
- [[03-Notes/Concepts/Codex-MCP-内存峰值与索引预检]]
