---
type: guide
title: Learning Session Log
updated: 2026-07-30
tags: [ai-agent, learning-session]
---

# 学习记录与纠错

`06-Daily/` 保存学习过程：闭卷回答、不确定点、错误、纠正和下一步。每天一个文件，同一天的多次学习继续追加，不必每次创建新文档。

## Obsidian 操作

1. 执行命令 `Daily notes: Open today's daily note`。
2. Obsidian 自动创建 `06-Daily/YYYY-MM-DD.md`，并套用 `_templates/daily-note.md`。
3. 光标放到“学习记录”下，执行 `Templates: Insert template`。
4. 选择 `_templates/learning-session.md`。
5. 先闭卷回答，再校验和纠错。

## 内容边界

- `06-Daily/`：保留原始回答和纠错过程。
- `03-Notes/`：只保存验证后的当前理解。
- `04-Projects/agent-labs/`：保存代码、测试、Trace 和 Eval。

纠错时不删除原回答。在下方追加“判定、修正、依据”。只有经过一手来源或实验验证的结论才能回写 `03-Notes/`。

## 用 Codex

```text
读取 AGENTS.md 和目标 Concept。
在今天的 06-Daily 日记追加一个 learning-session 模板块。
逐题进行闭卷 Recall；我回答前不要提示。
保留我的原回答，追加判定、纠正和证据。
验证后提出 Concept 修改 diff，等我确认再回写。
未完成实验时不要升级 maturity。
```
