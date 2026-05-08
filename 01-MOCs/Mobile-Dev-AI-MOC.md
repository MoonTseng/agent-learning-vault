---
type: moc
title: Mobile Dev × AI
updated: 2026-05-07
---

# Mobile Dev × AI MOC 📱

我的主战场：Android（工作，CamScanner）+ Flutter（个人项目）。
重点是把 AI agent / LLM 塞进移动端开发流程里。

## 方向

### 开发流程加速
- 生成代码 / UI / 单测
- Code review / 重构
- 崩溃分析 / 日志分析（参考 [[camscanner-support-log-analysis]]）

### 端侧 AI
- Android ML Kit / LiteRT / Gemini Nano
- Flutter 端跑 LLM（llama.cpp / mlc-llm）
- 离线 OCR / 语音 / 翻译

### 工具链
- Android 工程扫描 / 治理（参考 [[android-engineering-scan-for-governance]]）
- Gradle 插件里接 AI

## Notes

```dataview
LIST
FROM "03-Notes/Mobile-AI"
SORT file.mtime DESC
```

## 相关 Skills

```dataview
TABLE rating, status
FROM "03-Notes/Skills"
WHERE contains(platform, "android") OR contains(platform, "flutter")
SORT rating DESC
```
