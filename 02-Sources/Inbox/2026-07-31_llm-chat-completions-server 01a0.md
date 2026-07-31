---
source: Simon Willison
title: llm-chat-completions-server 0.1a0
url: https://simonwillison.net/2026/Jul/30/llm-chat-completions-server/#atom-everything
published: '2026-07-30T15:43:16+00:00'
score: 5
ingested: '2026-07-31'
status: unread
---

# llm-chat-completions-server 0.1a0

> Source: [Simon Willison](https://simonwillison.net/2026/Jul/30/llm-chat-completions-server/#atom-everything)

<p><strong>Release:</strong> <a href="https://github.com/simonw/llm-chat-completions-server/releases/tag/0.1a0">llm-chat-completions-server 0.1a0</a></p>
        <p>A key goal of the new content-addressable logs <a href="https://simonwillison.net/2026/Jul/30/llm-rc1/">in LLM 0.32rc1</a> was being able to support OpenAI Chat Completion style requests where each incoming message extends the previous conversation, like this:</p>
<pre><code>curl http://localhost:8002/v1/chat/completions \
  -H 'Cont
