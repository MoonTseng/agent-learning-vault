---
source: Hacker News Show HN
category: ai-monetize
title: Show HN - SIMD Viterbi Decoder in Rust
url: https://github.com/brian-armstrong/fec
published: Tue, 04 Aug 2026 22:37:05 +0000
score: 5
ingested: '2026-08-05'
status: unread
---

# Show HN - SIMD Viterbi Decoder in Rust

> Source: [Hacker News Show HN](https://github.com/brian-armstrong/fec)

<p>I wrote libcorrect in C in 2016 and wanted to revisit it in Rust. Instead of doing just a direct conversion, I went down the rabbit hole of making Rust's std::simd work for me. I ended up with a templated, generic Viterbi decoder for convolutional codes that dispatches the decode at runtime depending on which instruction sets are available. For small rates and orders, the entire decode lives in registers. Larger codes work through memory but take advantage of some acceleration structures.<p>I
