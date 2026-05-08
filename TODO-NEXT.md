# Brain vault — 下次继续做的事

上下文快照（2026-05-07）：
- vault 本地已搭好：~/Project/brain/，git init + 首次 commit 完成（main 分支）
- remote 已加：https://github.com/MoonTseng/brain.git（用户在 GitHub 手建私库）
- Hermes obsidian skill 已能读写 vault（OBSIDIAN_VAULT_PATH 已写入 ~/.hermes/.env）

还没做：

1. gh auth login
   ```
   gh auth login -h github.com -p https -w
   ```
   - GitHub.com → HTTPS → Authenticate Git → Yes
   - 切到 MoonTseng 账号授权
   - 目的：把 credential.helper 配成 osxkeychain，gitlab.intsig.net 的凭据不会被碰

2. brain 仓库单独配 local git 身份（避免公司邮箱出现在个人开源历史）
   - 用户需先去 https://github.com/settings/emails 看自己的 noreply 邮箱（格式：{id}+MoonTseng@users.noreply.github.com）
   - 或同意直接用公司邮箱
   ```
   cd ~/Project/brain
   git config user.name  "MoonTseng"
   git config user.email "<noreply 邮箱>"
   # 如果第一次 commit 用的是公司邮箱，想改掉需要 git commit --amend --reset-author
   ```

3. 首次推送
   ```
   cd ~/Project/brain
   git push -u origin main
   ```

4. 安装 blogwatcher-cli + bootstrap 订阅
   - 安装：`go install github.com/JulienTant/blogwatcher-cli/cmd/blogwatcher-cli@latest` 或 brew 下载 binary
   - 订阅清单见 02-Sources/_subscription-list.md 的 bootstrap 代码块

5. 两个 cronjob
   - 每日 08:00：blogwatcher-cli scan → 用 LLM 给新文章评分+分类 → > 7 分的写入 02-Sources/Inbox/
   - 每周日 20:00：周报，扫 Inbox 最近 7 天 + Ideas pipeline 流转情况，生成到 06-Daily/

## 骨架结构参考

```
01-MOCs/        Home, AI-Agents, Mobile-Dev-AI, Monetization
02-Sources/     Inbox (待分拣), Blogs (已归档), _subscription-list.md
03-Notes/       Skills, MCPs, Agents, Mobile-AI, Concepts
04-Projects/    短期项目
05-Ideas/       Seeds → Validating → Building → Shipped/Killed + 00-Pipeline.md
06-Daily/       日志
_templates/     skill-note, mcp-note, idea-note, daily-note
```
