---
type: pipeline
title: Ideas Pipeline
updated: 2026-05-07
---

# Ideas Pipeline 🚀

一个人搞钱的 idea 流转板。每个 idea 都走：
**Seeds → Validating → Building → Shipped / Killed**

每个阶段必做动作：
- Seeds：写一句话问题 + 目标用户 + kill criteria
- Validating：查 3 个竞品 + 问 1 个潜在用户 + 估最小可验证版本工作量
- Building：定 deadline 和 MVP 范围
- Shipped：记录上线数据，30 天后复盘
- Killed：写清 kill reason，下次避坑

## 🌱 Seeds

```dataview
TABLE effort, channel, created
FROM "05-Ideas/Seeds"
WHERE type = "idea"
SORT created DESC
```

## 🔬 Validating

```dataview
TABLE effort, channel, revenue-model
FROM "05-Ideas/Validating"
WHERE type = "idea"
SORT file.mtime DESC
```

## 🔨 Building

```dataview
TABLE effort, channel, file.mtime as last-touched
FROM "05-Ideas/Building"
WHERE type = "idea"
SORT file.mtime DESC
```

## 🚀 Shipped

```dataview
TABLE channel, revenue-model, file.mtime as shipped-at
FROM "05-Ideas/Shipped"
WHERE type = "idea"
SORT file.mtime DESC
```

## ❌ Killed（复盘用）

```dataview
TABLE kill-reason, file.mtime as killed-at
FROM "05-Ideas/Killed"
WHERE type = "idea"
SORT file.mtime DESC
```
