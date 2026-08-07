---
source: Hacker News Show HN
category: ai-monetize
title: Show HN - BlazeRules – YAML rule engine for streaming data, upto 5M records-SEC
url: https://news.ycombinator.com/item?id=49204650
published: Fri, 07 Aug 2026 00:55:02 +0000
score: 5
ingested: '2026-08-07'
status: unread
---

# Show HN - BlazeRules – YAML rule engine for streaming data, upto 5M records-SEC

> Source: [Hacker News Show HN](https://news.ycombinator.com/item?id=49204650)

<p><a href="https://github.com/purijs/blazerules" rel="nofollow">https://github.com/purijs/blazerules</a><p>I initially wanted to make a sub-millisecond log parser in C++ but that blew into a embeddable decision engine, that can run YAML defined rules on incoming data.
The rules are executed in a vectorized format on incoming data by reprojecting into a columnar format first, if it's not already. Depending on the payload size and rules complexity, the performance goes from 200K records/s to more
