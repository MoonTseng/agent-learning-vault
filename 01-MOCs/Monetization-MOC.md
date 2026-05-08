---
type: moc
title: Monetization
updated: 2026-05-07
---

# Monetization MOC 💰

一个人用 AI 赚钱。重点方向：vibe coding 小 app、公众号「极话」、工具型产品。

## 当前 Pipeline

→ [[05-Ideas/00-Pipeline]]

## 渠道

### 公众号「极话」
- 定位：科技 / AI 前沿 / 独立开发视角
- 现状：效果一般，需要复盘
- Shipped 文章：见 `05-Ideas/Shipped/`（走 pipeline 的选题）
- [[03-Notes/Concepts/wechat-growth-playbook|公众号增长 playbook]]（待写）

### Vibe Coding App
- Android / Flutter 快速原型 → 上架 → 变现
- 灵感来源：[[03-Notes/Concepts/vibe-coding|vibe coding 方法论]]

### 其他
- Chrome Extension
- 独立 Web 工具
- 技术咨询 / 私教

## 思考素材（Validating 区）

```dataview
TABLE revenue-model, effort, inspired-by
FROM "05-Ideas/Validating"
```

## 已 Killed 的复盘

```dataview
TABLE file.mtime as killed-at
FROM "05-Ideas/Killed"
SORT file.mtime DESC
```

## 灵感来源（Inbox 里的 monetization 类）

```dataview
LIST
FROM "02-Sources/Inbox"
WHERE contains(tags, "monetization") OR contains(tags, "indie-dev")
SORT file.ctime DESC
LIMIT 10
```
