---
source: "Simon Willison"
title: "Codex CLI 0.128.0 adds -goal"
url: "https://simonwillison.net/2026/Apr/30/codex-goals/#atom-everything"
published: "2026-04-30T23:23:17+00:00"
score: 5
ingested: "2026-05-08"
status: unread
---

# Codex CLI 0.128.0 adds -goal

> Source: [Simon Willison](https://simonwillison.net/2026/Apr/30/codex-goals/#atom-everything)

<p><strong><a href="https://github.com/openai/codex/releases/tag/rust-v0.128.0">Codex CLI 0.128.0 adds /goal</a></strong></p>
The latest version of OpenAI's Codex CLI coding agent adds their own version of the <a href="https://ghuntley.com/ralph/">Ralph loop</a>: you can now set a <code>/goal</code> and Codex will keep on looping until it evaluates that the goal has been completed... or the configured token budget has been exhausted.</p>
<p>It looks like the feature is mainly implemented though 
