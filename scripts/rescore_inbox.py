#!/usr/bin/env python3
"""
Batch re-score existing Inbox notes with Claude Haiku.

For each note:
- Read frontmatter + first 800 chars of body
- Ask Claude: score 1-5 + primary tag (agent/monetize/tool/research/news/noise) + 1-line takeaway
- Update frontmatter in-place

Low score (1) → move to 99-Archive/low-score
High score (4-5) → stay in Inbox, mark `status: highlight`
Noise tag → move to 99-Archive/noise
"""
import os, re, sys, json, shutil, time
from pathlib import Path
import urllib.request
import urllib.error

ROOT = Path(__file__).resolve().parent.parent
INBOX = ROOT / "02-Sources/Inbox"
ARCHIVE_LOW = ROOT / "99-Archive/low-score-2026-05"
ARCHIVE_NOISE = ROOT / "99-Archive/noise-2026-05"
ARCHIVE_LOW.mkdir(parents=True, exist_ok=True)
ARCHIVE_NOISE.mkdir(parents=True, exist_ok=True)

API_KEY = os.environ.get("ANTHROPIC_API_KEY")
MODEL = "claude-haiku-4-5"
API_URL = os.environ.get(
    "ANTHROPIC_API_URL",
    "https://api.anthropic.com/v1/messages",
)

PROMPT_TMPL = """你是一个 AI 技术/创业内容的评审员。用户 Ray 的兴趣：
- AI Agent、LLM 应用、MCP、Cursor/Claude Code 类工具
- AI 时代的个人变现（indie dev、SaaS、副业项目、内容创业）
- 前沿研究简讯（Anthropic/OpenAI/Google 官方、Karpathy、Latent Space 等）

对下面的文章，输出 JSON：
{
  "score": 1-5 的整数（1=完全无关/标题党/抄新闻，3=有点意思，5=必读精华）,
  "tag": "agent" | "monetize" | "tool" | "research" | "news" | "noise",
  "takeaway": "一句话(<=30字)概括核心价值，或为何低分"
}

仅返回 JSON，不要任何额外文字。

标题: {title}
来源: {source}
正文摘要:
{body}
"""

def call_claude(title, source, body):
    body_snippet = body[:1500]
    prompt = (PROMPT_TMPL
              .replace("{title}", title)
              .replace("{source}", source)
              .replace("{body}", body_snippet))
    req = urllib.request.Request(
        API_URL,
        method="POST",
        headers={
            "x-api-key": API_KEY,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
        data=json.dumps({
            "model": MODEL,
            "max_tokens": 200,
            "messages": [{"role": "user", "content": prompt}],
        }).encode("utf-8"),
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        print(f"  HTTP {e.code}: {e.read()[:200]}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"  Error: {e}", file=sys.stderr)
        return None
    
    text = data["content"][0]["text"].strip()
    # Strip code fences if present
    text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text, flags=re.M)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # Try to extract first JSON object
        m = re.search(r"\{.*?\}", text, re.S)
        if m:
            try:
                return json.loads(m.group(0))
            except Exception:
                pass
        print(f"  Bad JSON: {text[:150]}", file=sys.stderr)
        return None


def parse_frontmatter(content):
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", content, re.S)
    if not m:
        return None, content
    fm_text, body = m.groups()
    fm = {}
    for line in fm_text.split("\n"):
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip()
    return fm, body


def dump_frontmatter(fm):
    lines = ["---"]
    for k, v in fm.items():
        lines.append(f"{k}: {v}")
    lines.append("---")
    return "\n".join(lines)


def process(path: Path, idx: int, total: int):
    content = path.read_text(errors="ignore")
    fm, body = parse_frontmatter(content)
    if not fm:
        print(f"[{idx}/{total}] skip (no frontmatter): {path.name}")
        return None
    
    # Idempotent: skip if already scored (unless FORCE env set)
    if "score" in fm and fm["score"].isdigit() and int(fm["score"]) > 0 and "tag" in fm:
        if not os.environ.get("FORCE_RESCORE"):
            return None
    
    title = fm.get("title", path.stem).strip('"')
    source = fm.get("source", "").strip('"')
    
    result = call_claude(title, source, body)
    if not result:
        return None
    
    score = int(result.get("score", 3))
    tag = result.get("tag", "news")
    takeaway = result.get("takeaway", "").replace('"', "'")[:80]
    
    # Update frontmatter
    fm["score"] = str(score)
    fm["tag"] = tag
    fm["takeaway"] = f'"{takeaway}"'
    if score >= 4:
        fm["status"] = "highlight"

    new_content = dump_frontmatter(fm) + "\n" + body
    path.write_text(new_content)
    
    print(f"[{idx}/{total}] {score}⭐ [{tag}] {title[:50]}  → {takeaway[:40]}")
    
    # Route low-value notes to archive
    if tag == "noise":
        shutil.move(str(path), str(ARCHIVE_NOISE / path.name))
    elif score <= 2:
        shutil.move(str(path), str(ARCHIVE_LOW / path.name))
    
    return {"score": score, "tag": tag, "title": title}


def require_api_key() -> None:
    if not API_KEY:
        raise SystemExit(
            "ANTHROPIC_API_KEY is required. Export it in shell or load it from ignored local config."
        )


def main():
    require_api_key()
    files = sorted(INBOX.glob("*.md"))
    # skip daily notes
    files = [f for f in files if not re.match(r"^\d{4}-\d{2}-\d{2}\.md$", f.name)]
    total = len(files)
    print(f"Processing {total} notes...")
    
    results = []
    for i, f in enumerate(files, 1):
        r = process(f, i, total)
        if r:
            results.append(r)
        time.sleep(0.3)  # gentle rate limit
    
    # Summary
    by_tag = {}
    by_score = {}
    for r in results:
        by_tag[r["tag"]] = by_tag.get(r["tag"], 0) + 1
        by_score[r["score"]] = by_score.get(r["score"], 0) + 1
    
    print("\n=== Summary ===")
    print("By tag:", by_tag)
    print("By score:", by_score)


if __name__ == "__main__":
    main()
