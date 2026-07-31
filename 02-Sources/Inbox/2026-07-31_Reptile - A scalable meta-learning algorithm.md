---
source: OpenAI News
title: Reptile - A scalable meta-learning algorithm
url: https://openai.com/index/reptile
published: Wed, 07 Mar 2018 08:00:00 GMT
score: 5
ingested: '2026-07-31'
status: unread
---

# Reptile - A scalable meta-learning algorithm

> Source: [OpenAI News](https://openai.com/index/reptile)

We’ve developed a simple meta-learning algorithm called Reptile which works by repeatedly sampling a task, performing stochastic gradient descent on it, and updating the initial parameters towards the final parameters learned on that task. Reptile is the application of the Shortest Descent algorithm to the meta-learning setting, and is mathematically similar to first-order MAML (which is a version of the well-known MAML algorithm) that only needs black-box access to an optimizer such as SGD or A
