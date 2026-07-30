#!/usr/bin/env python3
"""
Agent Learning Vault RSS scanner.
Fetches all subscribed feeds, scores articles with LLM, writes high-score ones to Inbox.

Usage:
    python scripts/rss_scan.py              # scan all, write new articles to Inbox
    python scripts/rss_scan.py --dry-run    # scan all, print but don't write
    python scripts/rss_scan.py --no-llm     # skip LLM scoring, write all new articles
"""

import os
import sys
import json
import hashlib
import argparse
import datetime
from pathlib import Path

import yaml
import requests
import feedparser

# === Config ===
VAULT_ROOT = Path(__file__).resolve().parent.parent
INBOX_DIR = VAULT_ROOT / "02-Sources" / "Inbox"
STATE_FILE = VAULT_ROOT / ".rss_state.json"
SUBSCRIPTION_FILE = VAULT_ROOT / "scripts" / "feeds.yaml"

# Proxy for blocked sites (Reddit, Google, Medium, etc.)
PROXY = os.environ.get("RSS_PROXY", "http://127.0.0.1:49794")
# Sites that need proxy
PROXY_DOMAINS = [
    "reddit.com", "google.com", "googleblog.com", "medium.com",
    "anthropic.com", "producthunt.com", "starterstory.com",
    "indiehackers.com"
]

# LLM scoring (optional, uses ollama local)
LLM_ENDPOINT = os.environ.get("LLM_ENDPOINT", "http://127.0.0.1:11434/api/generate")
LLM_MODEL = os.environ.get("LLM_MODEL", "qwen2.5:7b")
SCORE_THRESHOLD = int(os.environ.get("SCORE_THRESHOLD", "7"))


def needs_proxy(url: str) -> bool:
    """Check if a URL needs proxy to access."""
    for domain in PROXY_DOMAINS:
        if domain in url:
            return True
    return False


def fetch_feed(feed_url: str) -> feedparser.FeedParserDict:
    """Fetch and parse an RSS/Atom feed."""
    headers = {"User-Agent": "Mozilla/5.0 (agent-learning-vault-rss/1.0)"}
    proxies = {"http": PROXY, "https": PROXY} if needs_proxy(feed_url) else None

    try:
        resp = requests.get(feed_url, headers=headers, proxies=proxies, timeout=20)
        resp.raise_for_status()
        return feedparser.parse(resp.text)
    except Exception as e:
        print(f"  [ERROR] {feed_url}: {e}", file=sys.stderr)
        return feedparser.FeedParserDict(entries=[])


def load_state() -> dict:
    """Load seen article IDs."""
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {"seen": {}}


def save_state(state: dict):
    """Save seen article IDs."""
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2))


def article_id(entry) -> str:
    """Generate a unique ID for an article."""
    raw = entry.get("id") or entry.get("link") or entry.get("title", "")
    return hashlib.md5(raw.encode()).hexdigest()


def score_article(title: str, summary: str) -> int:
    """Score an article 1-10 using local LLM. Returns 5 on failure."""
    prompt = f"""Rate this article's relevance (1-10) for an Android developer interested in:
- AI agents, LLM tools, MCP protocol
- Mobile AI (on-device ML, AI-powered apps)
- Indie dev monetization, side projects

Title: {title}
Summary: {summary[:300]}

Reply with ONLY a number 1-10, nothing else."""

    try:
        resp = requests.post(LLM_ENDPOINT, json={
            "model": LLM_MODEL,
            "prompt": prompt,
            "stream": False
        }, timeout=30)
        result = resp.json().get("response", "5").strip()
        # Extract first number found
        for ch in result:
            if ch.isdigit():
                return int(ch)
        return 5
    except Exception:
        return 5


def write_inbox_note(entry, source_name: str, score: int = 0):
    """Write an article as a markdown note in Inbox."""
    title = entry.get("title", "Untitled").replace("/", "-").replace(":", " -")
    link = entry.get("link", "")
    summary = entry.get("summary", "")[:500]
    published = entry.get("published", "")
    date_str = datetime.date.today().isoformat()

    # Sanitize filename
    safe_title = "".join(c for c in title if c.isalnum() or c in " -_").strip()[:60]
    filename = f"{date_str}_{safe_title}.md"
    filepath = INBOX_DIR / filename

    frontmatter = yaml.safe_dump(
        {
            "source": source_name,
            "title": title,
            "url": link,
            "published": published,
            "score": score,
            "ingested": date_str,
            "status": "unread",
        },
        allow_unicode=True,
        sort_keys=False,
    ).rstrip()

    content = f"""---
{frontmatter}
---

# {title}

> Source: [{source_name}]({link})

{summary}
"""
    filepath.write_text(content)
    return filepath


def load_feeds() -> list:
    """Load feed subscriptions from feeds.yaml."""
    if not SUBSCRIPTION_FILE.exists():
        print(f"[ERROR] {SUBSCRIPTION_FILE} not found", file=sys.stderr)
        sys.exit(1)
    with open(SUBSCRIPTION_FILE) as f:
        data = yaml.safe_load(f)
    return data.get("feeds", [])


def main():
    parser = argparse.ArgumentParser(description="Agent Learning Vault RSS scanner")
    parser.add_argument("--dry-run", action="store_true", help="Print but don't write")
    parser.add_argument("--no-llm", action="store_true", help="Skip LLM scoring")
    args = parser.parse_args()

    feeds = load_feeds()
    state = load_state()
    seen = state.get("seen", {})

    total_new = 0
    total_written = 0

    print(f"Scanning {len(feeds)} feed(s)...")
    print()

    for feed_cfg in feeds:
        name = feed_cfg["name"]
        url = feed_cfg["feed_url"]
        print(f"  {name}")

        parsed = fetch_feed(url)
        entries = parsed.entries
        new_entries = []

        for entry in entries:
            aid = article_id(entry)
            if aid not in seen:
                new_entries.append(entry)
                seen[aid] = datetime.date.today().isoformat()

        if not new_entries:
            print(f"    No new articles")
            continue

        total_new += len(new_entries)
        print(f"    Found {len(new_entries)} new article(s)")

        for entry in new_entries:
            title = entry.get("title", "Untitled")
            summary = entry.get("summary", "")

            if args.no_llm:
                score = 5
            else:
                score = score_article(title, summary)

            if score >= SCORE_THRESHOLD or args.no_llm:
                if not args.dry_run:
                    path = write_inbox_note(entry, name, score)
                    print(f"    [+] ({score}/10) {title[:50]}")
                else:
                    print(f"    [DRY] ({score}/10) {title[:50]}")
                total_written += 1
            else:
                print(f"    [-] ({score}/10) {title[:50]}")

    # Save state
    state["seen"] = seen
    state["last_scan"] = datetime.datetime.now().isoformat()
    if not args.dry_run:
        save_state(state)

    print()
    print(f"Done: {total_new} new articles, {total_written} written to Inbox")


if __name__ == "__main__":
    main()
