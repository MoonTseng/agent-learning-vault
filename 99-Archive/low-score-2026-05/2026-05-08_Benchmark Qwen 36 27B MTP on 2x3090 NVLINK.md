---
source: "r/LocalLLaMA"
title: "Benchmark Qwen 3.6 27B MTP on 2x3090 NVLINK"
url: "https://www.reddit.com/r/LocalLLaMA/comments/1t6susj/benchmark_qwen_36_27b_mtp_on_2x3090_nvlink/"
published: "2026-05-08T00:49:03+00:00"
score: 2
ingested: "2026-05-08"
status: unread
tag: news
takeaway: "本地LLM推理优化技巧，但缺乏普适性和实际应用价值指导"
---

# Benchmark Qwen 3.6 27B MTP on 2x3090 NVLINK

> Source: [r/LocalLLaMA](https://www.reddit.com/r/LocalLLaMA/comments/1t6susj/benchmark_qwen_36_27b_mtp_on_2x3090_nvlink/)

<!-- SC_OFF --><div class="md"><p><strong>TL;DR</strong></p> <p>On 4× RTX 3090 with NVLink bonded between GPU pairs (0↔2 and 1↔3), pinning TP=2 to a NVLinked pair gave <strong>+25% throughput</strong> at concurrency 1 and <strong>+53%</strong> at concurrency 4 vs running TP=2 over PCIe. Adding the other two GPUs to make it TP=4 made things worse, not better.</p> <h1>Setup</h1> <ul> <li><strong>Hardware:</strong> 4× RTX 3090 (24 GB), NVLink (NV4) between GPU0↔GPU2 and GPU1↔GPU3. Cross-pair traffi
