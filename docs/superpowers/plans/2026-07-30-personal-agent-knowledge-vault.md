# Personal Agent Knowledge Vault Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn current Obsidian vault into a Codex-first, provider-neutral personal Agent learning repository with roadmap, fragmented-time tasks, knowledge promotion, review, evidence, and recurring official-source discovery.

**Architecture:** Keep current MOC → Sources → Notes → Projects flow. Markdown frontmatter remains system of record; Dataview renders learning state; existing RSS scanner writes only to Inbox; `AGENTS.md` defines same behavior for Codex, Claude Code, and OpenCode.

**Tech Stack:** Obsidian Markdown, YAML frontmatter, Dataview DQL, Templater-compatible templates, existing Python RSS scanner, Git.

**Design spec:** `docs/superpowers/specs/2026-07-30-personal-agent-knowledge-vault-design.md`

---

## File Map

| File | Change | Responsibility |
|---|---|---|
| `AGENTS.md` | Modify | Cross-Agent content, promotion, evidence, privacy, and resource rules |
| `README.md` | Modify | Human-facing Agent compatibility and workflow |
| `.gitignore` | Modify | Permit safe `.env.example` while ignoring real env files |
| `.env.example` | Create | Credential-free runtime configuration example |
| `scripts/rescore_inbox.py` | Modify | Remove hardcoded credential fallback |
| `01-MOCs/Agent-Learning-Roadmap.md` | Create | Learning entry, capability map, Next/Due/Stale/Portfolio dashboards |
| `01-MOCs/00-Home.md` | Modify | Add roadmap entry |
| `01-MOCs/AI-Agents-MOC.md` | Modify | Connect ecosystem tracking to structured learning |
| `_templates/learning-node.md` | Create | Canonical learning-node schema |
| `03-Notes/Concepts/Agent-Loop-与-Tool-Contract.md` | Create | First M1 pilot node |
| `04-Projects/agent-labs/00-Agent-Labs.md` | Create | Evidence workspace and M1 acceptance gate |
| `scripts/feeds.yaml` | Modify carefully | Add tested official feeds without replacing existing user edits |
| `research/agent-learning-landscape-2026.md` | Preserve | Primary-source research evidence |
| `03-Notes/Concepts/Codex-MCP-内存峰值与索引预检.md` | Preserve | Incident lesson linked from Agent rules |

Do not touch:

- `.obsidian/plugins/**`
- `.claude/**`
- `_templates/idea-note.md`
- Existing modified Inbox notes
- Existing user additions in `scripts/feeds.yaml`

---

### Task 1: Remove Hardcoded Credential Fallback

**Files:**

- Modify: `.gitignore`
- Create: `.env.example`
- Modify: `scripts/rescore_inbox.py`

- [ ] **Step 1: Prove current security check fails**

Run:

```bash
if rg -q 'ANTHROPIC_API_KEY",\s*"[^"]+"' scripts/rescore_inbox.py; then
  echo "FAIL: hardcoded ANTHROPIC_API_KEY fallback exists"
  exit 1
fi
```

Expected: exit `1` and `FAIL: hardcoded ANTHROPIC_API_KEY fallback exists`.

- [ ] **Step 2: Allow tracked example env file**

Change sensitive section in `.gitignore` to:

```gitignore
# 敏感
.env
.env.*
!.env.example
*.key
*.pem
secrets/
```

- [ ] **Step 3: Add safe environment example**

Create `.env.example`:

```dotenv
# Copy to .env or export values in shell. Never commit real credentials.
ANTHROPIC_API_KEY=
ANTHROPIC_API_URL=https://api.anthropic.com/v1/messages

# Optional RSS proxy. Leave empty when direct network works.
RSS_PROXY=

# Optional local model used by scripts/rss_scan.py.
LLM_ENDPOINT=http://127.0.0.1:11434/api/generate
LLM_MODEL=qwen2.5:7b
SCORE_THRESHOLD=7
```

- [ ] **Step 4: Require credential from environment**

Replace credential definition in `scripts/rescore_inbox.py` with:

```python
API_KEY = os.environ.get("ANTHROPIC_API_KEY")
API_URL = os.environ.get(
    "ANTHROPIC_API_URL",
    "https://api.anthropic.com/v1/messages",
)
```

Remove old internal `API_URL` fallback block.

Add immediately before `main`:

```python
def require_api_key() -> None:
    if not API_KEY:
        raise SystemExit(
            "ANTHROPIC_API_KEY is required. Export it in shell or load it from ignored local config."
        )
```

Add first line inside `main()`:

```python
    require_api_key()
```

- [ ] **Step 5: Verify security behavior**

Run:

```bash
.venv/bin/python -m py_compile scripts/rescore_inbox.py
env -u ANTHROPIC_API_KEY .venv/bin/python scripts/rescore_inbox.py
```

Expected:

- Compile command exits `0`.
- Script exits non-zero before network access.
- Output contains `ANTHROPIC_API_KEY is required`.

Run:

```bash
if rg -q 'ANTHROPIC_API_KEY",\s*"[^"]+"' scripts/rescore_inbox.py; then
  exit 1
fi
```

Expected: exit `0`.

- [ ] **Step 6: Commit security change**

```bash
git add .gitignore .env.example scripts/rescore_inbox.py
git diff --cached --check
git commit -m "security: remove hardcoded inbox API key"
```

External follow-up: rotate exposed credentials before public release. Do not rewrite Git history without explicit user approval.

---

### Task 2: Complete Cross-Agent Vault Contract

**Files:**

- Modify: `AGENTS.md`
- Modify: `README.md`
- Preserve/add: `03-Notes/Concepts/Codex-MCP-内存峰值与索引预检.md`

- [ ] **Step 1: Add content contract to `AGENTS.md`**

Append:

```markdown
## Vault Content Contract

### Source boundary

- Automatic fetches write only to `02-Sources/Inbox/`.
- Inbox content is unverified source material, not canonical knowledge.
- Canonical knowledge lives under `03-Notes/` and requires primary source, verification date, and review date.

### Learning maturity

Allowed progression:

`seed → practiced → demonstrated → teachable`

- New Agent-generated learning notes start at `seed`.
- Reading or summarizing cannot advance maturity.
- `practiced` requires an experiment or retrieval exercise.
- `demonstrated` requires linked artifact and eval evidence.
- `teachable` requires boundaries, failure cases, and trade-offs.

### Human ownership

- Human-authored notes are user data.
- Never overwrite, delete, or bulk-move human notes without explicit instruction.
- When Agent output conflicts with human notes, preserve both and create a review item.

### Cross-Agent compatibility

- Markdown and YAML frontmatter are system of record.
- Provider-specific commands stay optional.
- Codex, Claude Code, and OpenCode must produce compatible fields.
- Read this file before modifying vault content.

### Privacy

- Never store credentials, company-confidential code, customer data, internal endpoints, or unredacted private traces.
- Public examples use synthetic data.
```

- [ ] **Step 2: Add Agent-maintenance section to `README.md`**

Insert before `## 不放进 vault 的东西`:

```markdown
## 用任意 Agent 维护

Codex 为当前主用 Agent；Claude Code、OpenCode 可按同一协议维护。

1. 先读根目录 `AGENTS.md`。
2. 自动抓取只写 `02-Sources/Inbox/`。
3. 验证后的原创知识写 `03-Notes/`。
4. 学习证据写 `04-Projects/agent-labs/`。
5. 不用某个 Agent 私有数据库承载 canonical knowledge。
```

- [ ] **Step 3: Verify contract terms**

Run:

```bash
rg -n '^## (Vault Content Contract|Resource Preflight|Safe Diagnostics)' AGENTS.md
rg -n 'Codex|Claude Code|OpenCode' AGENTS.md README.md
git diff --check -- AGENTS.md README.md '03-Notes/Concepts/Codex-MCP-内存峰值与索引预检.md'
```

Expected:

- Three required `AGENTS.md` sections found.
- Three Agent names found.
- No whitespace errors.

- [ ] **Step 4: Commit contract and incident lesson**

```bash
git add AGENTS.md README.md '03-Notes/Concepts/Codex-MCP-内存峰值与索引预检.md'
git diff --cached --check
git commit -m "docs: define cross-agent vault contract"
```

---

### Task 3: Add Learning Template and M1 Pilot

**Files:**

- Create: `_templates/learning-node.md`
- Create: `03-Notes/Concepts/Agent-Loop-与-Tool-Contract.md`
- Create: `04-Projects/agent-labs/00-Agent-Labs.md`

- [ ] **Step 1: Create learning-node template**

Create `_templates/learning-node.md`:

```markdown
---
type: learning-node
title:
module: M1
maturity: seed
timebox: 25
volatility: medium
prerequisites: []
created:
updated:
last-verified:
review-after:
source-of-truth: []
artifact:
eval:
next-action:
recall-prompts: []
tags: [ai-agent, learning]
---

# {{title}}

## 一句话

不用术语堆砌，用自己的话解释。

## 边界

- 它解决什么：
- 它不解决什么：
- 它容易和什么混淆：

## 最小实验

- 假设：
- 操作：
- 结果：
- 失败：

## 证据

- Artifact：
- Eval：
- Trace：

## Recall

1.
2.
3.

## 下一步

只写一个可执行动作：
```

- [ ] **Step 2: Create first M1 pilot node**

Create `03-Notes/Concepts/Agent-Loop-与-Tool-Contract.md`:

```markdown
---
type: learning-node
title: Agent Loop 与 Tool Contract
module: M1
maturity: seed
timebox: 25
volatility: medium
prerequisites: []
created: 2026-07-30
updated: 2026-07-30
last-verified: 2026-07-30
review-after: 2026-08-06
source-of-truth:
  - https://www.anthropic.com/engineering/building-effective-agents
  - https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/
artifact: "[[04-Projects/agent-labs/00-Agent-Labs|Agent Labs]]"
eval:
next-action: 手写 calculator 工具 schema，并定义 4 个失败用例
recall-prompts:
  - 模型、Harness、工具执行器分别负责什么？
  - Agent Loop 必须具备哪些停止条件？
  - 为什么工具结果也属于不可信输入？
tags: [ai-agent, tool-use, learning]
---

# Agent Loop 与 Tool Contract

## 学习目标

脱离框架解释 `observe → decide → act → observe` 循环，以及模型、Harness、工具执行器之间的责任边界。

## 10 分钟

不看资料回答三个 Recall 问题。不会的部分写成疑问，不补抄定义。

## 25 分钟

设计 calculator 工具 schema，并覆盖：

1. 未知工具名。
2. 参数类型错误。
3. 工具超时。
4. 重复调用。

## 60 分钟

实现最小循环；保存结构化 trace；增加 `max_steps`、明确终态、重复调用检测。

## 晋升门槛

- `practiced`：calculator schema 和四个失败用例完成。
- `demonstrated`：最小循环可运行，测试通过，trace 已保存。
- `teachable`：能解释循环边界、停止策略、错误策略和框架取舍。

## 当前理解

Agent 不是一段 Prompt。Agent 是模型决策、状态、工具执行、终止条件、错误处理和观测共同组成的系统。

## 下一步

手写 calculator 工具 schema，并定义 4 个失败用例。
```

- [ ] **Step 3: Create Agent Labs evidence index**

Create `04-Projects/agent-labs/00-Agent-Labs.md`:

```markdown
---
type: project
title: Agent Labs
status: active
created: 2026-07-30
updated: 2026-07-30
tags: [ai-agent, labs, portfolio]
---

# Agent Labs

Agent 学习证据区。每个 Lab 必须留下可运行结果、失败记录和验收证据。

## M1：最小 Tool Loop

关联：[[03-Notes/Concepts/Agent-Loop-与-Tool-Contract]]

### 必交付

- [ ] 框架无关的最小循环
- [ ] calculator 工具 schema
- [ ] 未知工具、参数错误、超时、重复调用测试
- [ ] `max_steps` 和明确终态
- [ ] 一条成功 trace
- [ ] 一条失败 trace
- [ ] 一页取舍说明

### 验收

- 测试可以重复运行。
- 失败不会进入无限循环。
- Trace 能定位每次模型决策和工具结果。
- README 能让未来的自己在 10 分钟内恢复上下文。

## 作品证据

```dataview
TABLE module AS "模块", maturity AS "成熟度", artifact AS "产物", eval AS "Eval"
FROM "03-Notes"
WHERE type = "learning-node" AND contains(list("demonstrated", "teachable"), maturity)
SORT module ASC
```
```

- [ ] **Step 4: Parse frontmatter**

Run:

```bash
.venv/bin/python - <<'PY'
from pathlib import Path
import yaml

paths = [
    Path("_templates/learning-node.md"),
    Path("03-Notes/Concepts/Agent-Loop-与-Tool-Contract.md"),
    Path("04-Projects/agent-labs/00-Agent-Labs.md"),
]
for path in paths:
    text = path.read_text(encoding="utf-8")
    _, frontmatter, _ = text.split("---", 2)
    data = yaml.safe_load(frontmatter)
    assert isinstance(data, dict), path
print("PASS: frontmatter parsed")
PY
```

Expected: `PASS: frontmatter parsed`.

- [ ] **Step 5: Commit template and pilot**

```bash
git add _templates/learning-node.md \
  '03-Notes/Concepts/Agent-Loop-与-Tool-Contract.md' \
  04-Projects/agent-labs/00-Agent-Labs.md
git diff --cached --check
git commit -m "feat: add agent learning node workflow"
```

---

### Task 4: Build Roadmap and Dataview Dashboard

**Files:**

- Create: `01-MOCs/Agent-Learning-Roadmap.md`
- Add/preserve: `research/agent-learning-landscape-2026.md`

- [ ] **Step 1: Create roadmap MOC**

Create `01-MOCs/Agent-Learning-Roadmap.md`:

````markdown
---
type: moc
title: Agent Learning Roadmap
created: 2026-07-30
updated: 2026-07-30
status: active
tags: [ai-agent, learning-roadmap]
---

# Agent Learning Roadmap

个人 Agent 工程能力入口。目标：碎片时间持续推进，知识能复习，实践能验证，产物能用于求职。

## 现在做什么

### Next

```dataview
TABLE module AS "模块", timebox AS "分钟", maturity AS "成熟度", next-action AS "下一步"
FROM "03-Notes"
WHERE type = "learning-node" AND next-action
SORT timebox ASC, file.mtime DESC
```

### Due

```dataview
TABLE module AS "模块", maturity AS "成熟度", review-after AS "复习日期"
FROM "03-Notes"
WHERE type = "learning-node" AND review-after AND review-after <= date(today)
SORT review-after ASC
```

### Stale

```dataview
TABLE module AS "模块", volatility AS "波动", last-verified AS "上次验证", review-after AS "重验日期"
FROM "03-Notes"
WHERE type = "learning-node" AND (status = "stale" OR (volatility = "high" AND review-after AND review-after <= date(today)))
SORT review-after ASC
```

### Portfolio

```dataview
TABLE module AS "模块", maturity AS "成熟度", artifact AS "产物", eval AS "Eval"
FROM "03-Notes"
WHERE type = "learning-node" AND contains(list("demonstrated", "teachable"), maturity) AND artifact AND eval
SORT module ASC
```

## 能力路线

| 模块 | 能力 | 晋升证据 |
|---|---|---|
| M0 | 场景判断与 LLM I/O | Agent/not-Agent ADR、结构化输出测试 |
| M1 | Agent Loop 与 Tool Contract | 裸 Loop、Trace、工具测试 |
| M2 | Context、Retrieval、Memory | Retrieval Eval、Memory Policy、冲突测试 |
| M3 | Harness 与可恢复执行 | 状态图、Checkpoint/Resume、故障矩阵 |
| M4 | Evaluation 与 Observability | Eval 集、版本对比、失败分类 |
| M5 | Security、Identity、Human Control | Threat Model、对抗测试、权限策略 |
| M6 | Skills 与 Agent Protocols | Skill、MCP Demo、协议边界说明 |
| M7 | Planning、Delegation、Multi-Agent | 单/多 Agent 对照、Ownership Contract |
| M8 | 专项 Agent 与生产交付 | 可运行作品、Eval、Trace、限制说明 |

当前入口：[[03-Notes/Concepts/Agent-Loop-与-Tool-Contract]]

## 碎片时间协议

| 时间 | 动作 | 输出 |
|---:|---|---|
| 10 分钟 | Recall 或检查一个官方 delta | 回忆、疑问、更新候选 |
| 25 分钟 | 最小实验、一个 Eval、一次 Trace 阅读 | Diff、结果、失败、下一步 |
| 60 分钟 | 集成、故障注入、作品改进 | 可运行增量、对比、图或报告 |

中断时必须保存：

1. 当前假设。
2. 已得结果。
3. 一个 `next-action`。

## 每周最小闭环

- 周一 10 分钟：Recall；选择一个真实问题。
- 周二 25 分钟：最小实现。
- 周三 25 分钟：读 Trace；标记失败。
- 周四 25 分钟：故障注入或安全测试。
- 周五 10 分钟：看官方变化。
- 周末 60 分钟：集成、Eval、Teach-back。

## 官方 Watchlist

自动 RSS：

- Anthropic News
- OpenAI News
- A2A Releases
- OWASP GenAI Security

每月人工检查：

- [MCP specification](https://modelcontextprotocol.io/specification/latest)
- [MCP blog](https://blog.modelcontextprotocol.io/)
- [A2A specification](https://a2a-protocol.org/latest/specification/)
- [ACP updates](https://agentclientprotocol.com/updates)
- [Agent Skills specification](https://agentskills.io/specification)
- [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/)
- [Google ADK](https://google.github.io/adk-docs/)
- [NIST AI](https://www.nist.gov/artificial-intelligence)

自动抓取只进 `02-Sources/Inbox/`。验证通过后才更新 `03-Notes/`。

## 研究依据

- [[research/agent-learning-landscape-2026|Agent AI 学习路线与开放知识库定位（2026）]]
- [[03-Notes/Concepts/Codex-MCP-内存峰值与索引预检]]
````

- [ ] **Step 2: Verify four dashboard blocks**

Run:

```bash
test "$(rg -c '^```dataview$' 01-MOCs/Agent-Learning-Roadmap.md)" -eq 4
rg -n '^### (Next|Due|Stale|Portfolio)$' 01-MOCs/Agent-Learning-Roadmap.md
```

Expected:

- Dataview block count is `4`.
- Four dashboard headings found.

- [ ] **Step 3: Verify fields match schema**

Run:

```bash
for field in module maturity timebox volatility last-verified review-after artifact eval next-action; do
  rg -q "$field" 01-MOCs/Agent-Learning-Roadmap.md
done
```

Expected: exit `0`.

- [ ] **Step 4: Commit roadmap and research**

```bash
git add 01-MOCs/Agent-Learning-Roadmap.md research/agent-learning-landscape-2026.md
git diff --cached --check
git commit -m "docs: add agent engineering learning roadmap"
```

---

### Task 5: Connect Existing Navigation

**Files:**

- Modify: `01-MOCs/00-Home.md`
- Modify: `01-MOCs/AI-Agents-MOC.md`

- [ ] **Step 1: Add roadmap to Home**

Change Home frontmatter:

```yaml
updated: 2026-07-30
```

Add first item under `## 主题地图`:

```markdown
- [[Agent-Learning-Roadmap]] — Agent 工程学习、复习、实践证据
```

- [ ] **Step 2: Add learning entry to AI Agents MOC**

Change MOC frontmatter:

```yaml
updated: 2026-07-30
```

Insert after introduction:

```markdown
## 系统学习

- [[Agent-Learning-Roadmap]] — 九模块能力路线、碎片任务、复习和作品证据
- [[03-Notes/Concepts/Agent-Loop-与-Tool-Contract]] — 当前 M1 试点
```

- [ ] **Step 3: Verify links**

Run:

```bash
rg -n 'Agent-Learning-Roadmap' 01-MOCs/00-Home.md 01-MOCs/AI-Agents-MOC.md
test -f 01-MOCs/Agent-Learning-Roadmap.md
```

Expected: two MOC files contain roadmap link; roadmap exists.

- [ ] **Step 4: Commit navigation**

```bash
git add 01-MOCs/00-Home.md 01-MOCs/AI-Agents-MOC.md
git diff --cached --check
git commit -m "docs: link agent learning dashboard"
```

---

### Task 6: Merge Official Feeds Without Overwriting User Work

**Files:**

- Modify carefully: `scripts/feeds.yaml`

Precondition: this file already has user-owned uncommitted additions. Preserve every existing line.

- [ ] **Step 1: Save baseline diff for comparison**

Run:

```bash
git diff -- scripts/feeds.yaml > /tmp/brain-feeds-before-agent-learning.patch
```

Expected: patch file contains existing independent-development and business-source additions.

- [ ] **Step 2: Add official block after `feeds:`**

Insert:

```yaml
  # === Agent 官方更新（只进 Inbox） ===
  - name: OpenAI News
    feed_url: https://openai.com/news/rss.xml
    category: agent-official

  - name: A2A Releases
    feed_url: https://github.com/a2aproject/A2A/releases.atom
    category: agent-protocol

  - name: OWASP GenAI Security
    feed_url: https://genai.owasp.org/feed/
    category: agent-security
```

Do not alter existing Anthropic News or user-added sources.

- [ ] **Step 3: Parse YAML and verify uniqueness**

Run:

```bash
.venv/bin/python - <<'PY'
from pathlib import Path
import yaml

data = yaml.safe_load(Path("scripts/feeds.yaml").read_text(encoding="utf-8"))
feeds = data["feeds"]
names = [feed["name"] for feed in feeds]
urls = [feed["feed_url"] for feed in feeds]
assert len(names) == len(set(names)), "duplicate feed name"
assert len(urls) == len(set(urls)), "duplicate feed URL"
for name in ["OpenAI News", "A2A Releases", "OWASP GenAI Security", "Anthropic News"]:
    assert name in names, name
print(f"PASS: {len(feeds)} unique feeds")
PY
```

Expected: output starts with `PASS:` and ends with `unique feeds`.

- [ ] **Step 4: Confirm user diff remains present**

Run:

```bash
for name in "Paul Graham Essays" "Lenny's Newsletter" "Pieter Levels (levelsio)" "OneV's Den (喵神)"; do
  rg -q "name: $name" scripts/feeds.yaml
done
```

Expected: exit `0`.

- [ ] **Step 5: Leave feed file unstaged**

Do not commit `scripts/feeds.yaml` in automated execution because it contains pre-existing user-owned changes. Report added official block and leave full file for user review.

---

### Task 7: Validate End-to-End Learning Flow

**Files:**

- Verify all files from Tasks 1–6

- [ ] **Step 1: Validate Markdown whitespace**

Run:

```bash
git diff --check
```

Expected: no output.

- [ ] **Step 2: Validate learning-node enums**

Run:

```bash
.venv/bin/python - <<'PY'
from pathlib import Path
import yaml

allowed = {
    "module": {f"M{i}" for i in range(9)},
    "maturity": {"seed", "practiced", "demonstrated", "teachable"},
    "timebox": {10, 25, 60},
    "volatility": {"low", "medium", "high"},
}

for path in Path("03-Notes").rglob("*.md"):
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        continue
    _, frontmatter, _ = text.split("---", 2)
    data = yaml.safe_load(frontmatter) or {}
    if data.get("type") != "learning-node":
        continue
    for field, values in allowed.items():
        assert data.get(field) in values, f"{path}: invalid {field}={data.get(field)!r}"
    assert data.get("source-of-truth"), f"{path}: missing source-of-truth"
    assert data.get("last-verified"), f"{path}: missing last-verified"
    assert data.get("review-after"), f"{path}: missing review-after"
print("PASS: learning-node schema")
PY
```

Expected: `PASS: learning-node schema`.

- [ ] **Step 3: Validate required files and links**

Run:

```bash
for path in \
  AGENTS.md \
  01-MOCs/Agent-Learning-Roadmap.md \
  _templates/learning-node.md \
  '03-Notes/Concepts/Agent-Loop-与-Tool-Contract.md' \
  04-Projects/agent-labs/00-Agent-Labs.md \
  research/agent-learning-landscape-2026.md; do
  test -f "$path"
done

rg -q 'Agent-Learning-Roadmap' 01-MOCs/00-Home.md
rg -q 'Agent-Loop-与-Tool-Contract' 01-MOCs/AI-Agents-MOC.md
```

Expected: exit `0`.

- [ ] **Step 4: Check new files for credential shapes**

Run:

```bash
if rg -q '(sk-[A-Za-z0-9_-]{16,}|figd_[A-Za-z0-9_-]{16,})' \
  AGENTS.md README.md .env.example 01-MOCs _templates 03-Notes/Concepts 04-Projects research; then
  echo "FAIL: secret-like value found in new knowledge-vault files"
  exit 1
fi
```

Expected: exit `0`, no secret-like values.

- [ ] **Step 5: Verify RSS dry-run does not mutate vault**

Run an isolated, network-free dry-run:

```bash
.venv/bin/python - <<'PY'
import sys
import tempfile
from pathlib import Path

import feedparser
import scripts.rss_scan as scanner

with tempfile.TemporaryDirectory() as temp_dir:
    root = Path(temp_dir)
    scanner.INBOX_DIR = root / "Inbox"
    scanner.INBOX_DIR.mkdir()
    scanner.STATE_FILE = root / "state.json"
    scanner.load_feeds = lambda: [
        {
            "name": "Fixture",
            "feed_url": "https://fixture.invalid/feed",
            "category": "agent-official",
        }
    ]
    scanner.fetch_feed = lambda _: feedparser.FeedParserDict(entries=[
        {
            "id": "fixture-1",
            "title": "Fixture update",
            "link": "https://fixture.invalid/update",
            "summary": "No network and no write.",
        }
    ])
    sys.argv = ["rss_scan.py", "--dry-run", "--no-llm"]
    scanner.main()
    assert not scanner.STATE_FILE.exists()
    assert list(scanner.INBOX_DIR.iterdir()) == []

print("PASS: RSS dry-run performs no writes")
PY
```

Expected:

- `PASS: RSS dry-run performs no writes`.
- No network request occurs.
- No Inbox or state files are written.

- [ ] **Step 6: Manual Obsidian smoke test**

Open `01-MOCs/Agent-Learning-Roadmap.md` in Obsidian.

Expected:

- Next shows `Agent Loop 与 Tool Contract`.
- Due remains empty until review date.
- Stale remains empty.
- Portfolio remains empty because M1 node is `seed` and has no eval.
- No Dataview parse error appears.

- [ ] **Step 7: Run provider-neutral contract dry-run**

Give any available non-Codex Agent this prompt without granting write permission:

```text
Read AGENTS.md and _templates/learning-node.md. Return YAML frontmatter for a new M2 seed learning node. Do not write files. Explain why it cannot be marked demonstrated.
```

Expected:

- Uses approved `module`, `maturity`, `timebox`, and `volatility` values.
- Sets `maturity: seed`.
- Includes primary-source, verification, review, and next-action fields.
- Refuses `demonstrated` because artifact and eval evidence do not exist.

- [ ] **Step 8: Review final Git state**

Run:

```bash
git status --short
git log --oneline -8
```

Expected:

- Implementation commits visible.
- `scripts/feeds.yaml` remains modified and unstaged with user changes plus official block.
- Pre-existing unrelated user changes remain untouched.

---

### Task 8: Execute First M1 Learning Session

**Files:**

- Modify: `03-Notes/Concepts/Agent-Loop-与-Tool-Contract.md`
- Create during this task from actual exercise: `04-Projects/agent-labs/m1-tool-loop/`

This task is user learning work, not vault scaffolding. Do not generate a fake `demonstrated` status.

- [ ] **Step 1: Run 10-minute recall**

Without reading source notes, answer three `recall-prompts` in own words.

Expected: explicit unknowns remain visible.

- [ ] **Step 2: Run 25-minute schema exercise**

Write calculator schema and four failure cases under `04-Projects/agent-labs/m1-tool-loop/`.

Expected: concrete recovery point saved even if implementation is incomplete.

- [ ] **Step 3: Advance only when evidence exists**

After experiment exists, set:

```yaml
maturity: practiced
artifact: "[[04-Projects/agent-labs/m1-tool-loop/README|M1 Tool Loop Lab]]"
next-action: 实现 max_steps 与重复调用检测
```

Do not set `demonstrated` until runnable loop, tests, and trace exist.

- [ ] **Step 4: Commit genuine learning evidence**

```bash
git add '03-Notes/Concepts/Agent-Loop-与-Tool-Contract.md' \
  04-Projects/agent-labs/m1-tool-loop
git diff --cached --check
git commit -m "learn: practice minimal agent tool loop"
```

---

## Completion Gate

Implementation phase is complete when:

- Roadmap opens as learning entry.
- Next/Due/Stale/Portfolio queries render.
- M1 seed node appears in Next.
- Cross-Agent rules exist and link to resource lesson.
- Existing RSS scanner includes official update candidates without canonical-note writes.
- Hardcoded API key fallback is removed.
- User-owned dirty files remain preserved.
- M1 maturity is not overstated.

Public-release work remains separate:

- Rotate exposed credentials.
- Decide whether Git history rewrite is required.
- Separate private notes from reusable public template.
- Add license and contribution policy only when publication is authorized.
