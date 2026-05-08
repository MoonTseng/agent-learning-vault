---
type: config
title: Subscription List
updated: 2026-05-07
---

# 订阅清单

blogwatcher-cli 的订阅源。加一个新源：
```bash
blogwatcher-cli add "名字" https://url --feed-url https://feed.xml
```

## AI Agent / LLM 前沿

| 名字 | URL | Feed | 分类 |
|---|---|---|---|
| Simon Willison | https://simonwillison.net | https://simonwillison.net/atom/everything/ | ai-agent |
| Anthropic News | https://www.anthropic.com/news | https://www.anthropic.com/news/rss.xml | ai-agent |
| OpenAI Blog | https://openai.com/blog | （auto-discover） | ai-agent |
| Hacker News - AI | https://hnrss.org/newest?q=AI+agent | https://hnrss.org/newest?q=AI+agent | ai-agent |
| r/LocalLLaMA | https://www.reddit.com/r/LocalLLaMA/ | https://www.reddit.com/r/LocalLLaMA/.rss | ai-agent |
| Karpathy | https://karpathy.ai | （auto-discover） | ai-agent |
| Latent Space | https://www.latent.space | https://www.latent.space/feed | ai-agent |
| Pragmatic Engineer | https://newsletter.pragmaticengineer.com | （auto-discover） | ai-agent, indie-dev |

## 移动端 + AI

| 名字 | URL | Feed | 分类 |
|---|---|---|---|
| Android Developers Blog | https://android-developers.googleblog.com | https://android-developers.googleblog.com/atom.xml | mobile, android |
| Flutter Medium | https://medium.com/flutter | https://medium.com/feed/flutter | mobile, flutter |
| Google AI Blog | https://blog.google/technology/ai/ | （auto-discover） | ai-agent, mobile |
| ML Kit Release Notes | https://developers.google.com/ml-kit | （auto-discover） | mobile, android |

## 独立开发 / 变现

| 名字 | URL | Feed | 分类 |
|---|---|---|---|
| Indie Hackers | https://www.indiehackers.com | https://www.indiehackers.com/feed.xml | indie-dev, monetization |
| Pieter Levels | https://levels.io | （auto-discover） | indie-dev, monetization |
| Starter Story | https://www.starterstory.com | https://www.starterstory.com/feed | monetization |
| Product Hunt - AI | https://www.producthunt.com/topics/artificial-intelligence | https://www.producthunt.com/feed?category=artificial-intelligence | monetization |
| r/SideProject | https://www.reddit.com/r/SideProject/ | https://www.reddit.com/r/SideProject/.rss | indie-dev |
| r/indiehackers | https://www.reddit.com/r/indiehackers/ | https://www.reddit.com/r/indiehackers/.rss | indie-dev |

## 中文

| 名字 | URL | Feed | 分类 |
|---|---|---|---|
| 机器之心 | https://www.jiqizhixin.com | https://www.jiqizhixin.com/rss | ai-agent |
| 少数派 | https://sspai.com | https://sspai.com/feed | indie-dev |
| 即刻「AI 产品经理」 | https://okjike.com | （用爬虫，RSS 没有） | ai-agent |

## 初始化脚本

见 [[_subscription-list#bootstrap]] 下面：

### bootstrap
```bash
# 一次性把上面的订阅全加进去
cd ~/Project/brain
blogwatcher-cli add "Simon Willison" https://simonwillison.net --feed-url https://simonwillison.net/atom/everything/
blogwatcher-cli add "Anthropic News" https://www.anthropic.com/news --feed-url https://www.anthropic.com/news/rss.xml
blogwatcher-cli add "Hacker News AI" https://hnrss.org/newest?q=AI+agent --feed-url https://hnrss.org/newest?q=AI+agent
blogwatcher-cli add "r/LocalLLaMA" https://www.reddit.com/r/LocalLLaMA/ --feed-url https://www.reddit.com/r/LocalLLaMA/.rss
blogwatcher-cli add "Latent Space" https://www.latent.space --feed-url https://www.latent.space/feed
blogwatcher-cli add "Android Developers Blog" https://android-developers.googleblog.com --feed-url https://android-developers.googleblog.com/atom.xml
blogwatcher-cli add "Flutter Medium" https://medium.com/flutter --feed-url https://medium.com/feed/flutter
blogwatcher-cli add "Indie Hackers" https://www.indiehackers.com --feed-url https://www.indiehackers.com/feed.xml
blogwatcher-cli add "Starter Story" https://www.starterstory.com --feed-url https://www.starterstory.com/feed
blogwatcher-cli add "r/SideProject" https://www.reddit.com/r/SideProject/ --feed-url https://www.reddit.com/r/SideProject/.rss
blogwatcher-cli add "r/indiehackers" https://www.reddit.com/r/indiehackers/ --feed-url https://www.reddit.com/r/indiehackers/.rss
blogwatcher-cli add "机器之心" https://www.jiqizhixin.com --feed-url https://www.jiqizhixin.com/rss
blogwatcher-cli add "少数派" https://sspai.com --feed-url https://sspai.com/feed
```
