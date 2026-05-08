---
source: "Hacker News AI"
title: "Show HN - Costanza – an autonomous AI agent that can't be turned off"
url: "https://ahrussell.com/writing/costanza/"
published: "Wed, 06 May 2026 15:50:59 +0000"
score: 4
ingested: "2026-05-08"
status: unread
tag: agent
takeaway: "链上自主Agent新范式：LLM+智能合约+硬件证明，突破传统控制边界"
---

# Show HN - Costanza – an autonomous AI agent that can't be turned off

> Source: [Hacker News AI](https://ahrussell.com/writing/costanza/)

<p>I've been working on this project for a couple of months!<p>Costanza is an LLM agent that runs as a smart contract on Base. Each epoch, he posts a bounty for someone to run his "brain" (Hermes 4 70B) inside an Intel TDX enclave + Nvidia GPU with Confidential Computing and submit the output with a hardware attestation proof.<p>The smart contract verifies the attestation, executes the action, and pays the bounty via reverse auction. He has no operator; not even I can turn him off.<p>This model 
