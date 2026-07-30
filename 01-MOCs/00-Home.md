---
type: moc
title: Home
updated: 2026-07-30
---

# Home 🏠

整个 Agent Learning Vault 的入口 + Inbox 清理面板。

## 主题地图

- [[Agent-Learning-Roadmap]] — Agent 工程学习、复习、实践证据
- [[AI-Agents-MOC]] — AI agent、skill、MCP、框架
- [[Mobile-Dev-AI-MOC]] — Android / Flutter 里用 AI 加速开发
- [[Monetization-MOC]] — 独立开发赚钱、vibe coding、公众号

## 运行区

- [[05-Ideas/00-Pipeline|Ideas Pipeline]] — idea 从萌芽到上线
- `04-Projects/` — 当前进行中的项目
- [[06-Daily/README|学习记录与纠错]] — 闭卷回答、纠错和回写 SOP

---

## 📥 Inbox 清理面板

> 目标：每次打开这里，先看"精华"和"该处理的"，其他当噪音

### 🔥 未读精华（score ≥ 4）

```dataview
TABLE WITHOUT ID
  file.link AS "标题",
  score AS "⭐",
  tag AS "类",
  takeaway AS "一句话"
FROM "02-Sources/Inbox"
WHERE score >= 4 AND status = "unread"
SORT score DESC, file.ctime DESC
LIMIT 20
```

### ⚡ 今日新增

```dataview
TABLE WITHOUT ID
  file.link AS "标题",
  score AS "⭐",
  tag AS "类"
FROM "02-Sources/Inbox"
WHERE file.ctime >= date(today)
SORT score DESC
```

### 📊 Inbox 分布（按 tag）

```dataview
TABLE WITHOUT ID
  tag AS "类别",
  length(rows) AS "数量",
  round(sum(rows.score) / length(rows), 1) AS "平均分"
FROM "02-Sources/Inbox"
WHERE tag != null
GROUP BY tag
SORT length(rows) DESC
```

### 🗑 需要归档（score ≤ 2，unread > 7 天）

```dataview
LIST
FROM "02-Sources/Inbox"
WHERE score <= 2 AND status = "unread" AND (date(today) - file.ctime).days > 7
LIMIT 30
```

---

## 🧠 最近笔记（03-Notes / 05-Ideas）

```dataview
TABLE file.mtime AS "修改时间"
FROM "03-Notes" OR "05-Ideas"
SORT file.mtime DESC
LIMIT 10
```

---

## 📈 本周统计

```dataview
TABLE WITHOUT ID
  length(rows) AS "数量"
FROM "02-Sources/Inbox"
WHERE file.ctime >= date(today) - dur(7 days)
GROUP BY true
```
