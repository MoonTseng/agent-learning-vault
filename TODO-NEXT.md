# Brain vault — 状态追踪

上下文快照（2026-05-08）：
- vault 本地搭好：~/Project/brain/，已推送 GitHub (MoonTseng/brain)
- git 身份：MoonTseng <MoonTseng@users.noreply.github.com>
- Python RSS scanner 替代 blogwatcher-cli（.venv + feedparser）
- 14 个订阅源配置在 scripts/feeds.yaml
- 首次扫描完成：235 篇文章入库 02-Sources/Inbox/
- Hermes cronjob 已配置：
  - brain-daily-rss-scan (每日 08:00)：no_agent 脚本模式
  - brain-weekly-digest (每周日 20:00)：LLM 总结周报

## ✅ 已完成
1. ✅ brain 仓库 local git 身份配置（MoonTseng + noreply email）
2. ✅ 历史 commit 改写为新身份 + force push
3. ✅ RSS 扫描方案落地（Python 脚本，支持代理）
4. ✅ 14 源订阅 + 首次扫描
5. ✅ 每日 RSS cronjob
6. ✅ 每周周报 cronjob

## 🔜 下一步可做
1. ollama 跑起来后，去掉 --no-llm，启用 LLM 评分（SCORE_THRESHOLD=7 过滤噪音）
2. 手动往 05-Ideas/Seeds/ 放几个 idea 笔记，让周报有内容可报
3. 探索 Obsidian 模板联动（在 Obsidian 中打开 vault、配 Dataview 查看 Inbox）
4. 加更多订阅源（个人博客、Newsletter 等）
5. 实现 "Inbox → Notes 归档" 流程（读完标记 → 移入 03-Notes/ 对应子目录）
