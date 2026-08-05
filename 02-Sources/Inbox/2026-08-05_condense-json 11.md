---
source: Simon Willison
category: ai-agent
title: condense-json 1.1
url: https://simonwillison.net/2026/Aug/3/condense-json/#atom-everything
published: '2026-08-03T04:56:26+00:00'
score: 5
ingested: '2026-08-05'
status: unread
---

# condense-json 1.1

> Source: [Simon Willison](https://simonwillison.net/2026/Aug/3/condense-json/#atom-everything)

<p><strong>Release:</strong> <a href="https://github.com/simonw/condense-json/releases/tag/1.1">condense-json 1.1</a></p>
        <p>After shipping <a href="https://simonwillison.net/2026/Aug/2/condense-json/">condense-json 1.0</a> I started integrating it into LLM, and found there were some desirable new features already:</p>
<blockquote>
<ul>
<li>Replacements object can now include values other than strings. These will be identified and used as structural replacements by <code>condense_json()<
