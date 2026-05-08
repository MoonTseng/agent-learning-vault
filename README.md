# Brain 🧠

yue_zeng / MoonTseng 的个人知识库。Obsidian vault + Hermes Agent 读写。

## 目录约定

```
01-MOCs/        各主题的索引页（Map of Content）
02-Sources/     原始信息
  Inbox/        自动抓取的 raw，待分拣
  Blogs/        已归档的原文摘录
03-Notes/       我自己的原子笔记（真思考产出）
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

## 工作流

- 每天 cronjob 扫订阅源，> 7 分的写入 `02-Sources/Inbox/`
- 周末人工精读 Inbox，有价值的改写成 `03-Notes/` 下原子笔记
- idea 从 `05-Ideas/Seeds/` 出发，走 pipeline，Killed 必写 kill reason
- 每月 skill 体检：扫 Skills/ 里 `last-verified` > 90 天的，让 agent 查最新版本

## 用 Hermes 查询

直接问：「brain 里有没有 xxx 的笔记？」
Hermes 会用 obsidian skill 的 search_files 搜。

## 不放进 vault 的东西

- 密钥、token、客户敏感信息
- 大体积二进制（> 10MB 的视频/数据集，用 git-lfs 或外部链接）
- 公司（INTSIG）未公开项目的源码片段
