---
source: "Simon Willison"
title: "LLM 0.32a0  is a major backwards-compatible refactor"
url: "https://simonwillison.net/2026/Apr/29/llm/#atom-everything"
published: "2026-04-29T19:01:47+00:00"
score: 5
ingested: "2026-05-08"
status: unread
---

# LLM 0.32a0  is a major backwards-compatible refactor

> Source: [Simon Willison](https://simonwillison.net/2026/Apr/29/llm/#atom-everything)

<p>I just released <a href="https://llm.datasette.io/en/latest/changelog.html#a0-2026-04-28">LLM 0.32a0</a>, an alpha release of my <a href="https://llm.datasette.io/">LLM</a> Python library and CLI tool for accessing LLMs, with some consequential changes that I've been working towards for quite a while.</p>
<p>Previous versions of LLM modeled the world in terms of prompts and responses. Send the model a text prompt, get back a text response.</p>
<pre><span class="pl-k">import</span> <span class
