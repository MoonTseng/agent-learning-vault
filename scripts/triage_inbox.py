#!/usr/bin/env python3
"""
Inbox triage helper.

Ranks Inbox notes for concept promotion and can mark top candidates as highlights
without touching canonical notes under 03-Notes/.

Usage:
    .venv/bin/python scripts/triage_inbox.py
    .venv/bin/python scripts/triage_inbox.py --limit 5 --apply
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import yaml

ROOT = Path(__file__).resolve().parent.parent
INBOX = ROOT / "02-Sources" / "Inbox"
FEEDS_FILE = ROOT / "scripts" / "feeds.yaml"

OFFICIAL_SOURCES = {
    "OpenAI News",
    "Anthropic News",
    "OWASP GenAI Security",
    "A2A Releases",
}

MODULE_RULES = [
    (
        "M1",
        "Agent Loop / Tool Contract",
        [
            "agent loop",
            "tool contract",
            "tool use",
            "codex",
            "harness",
            "sandbox",
            "workflow",
            "loop",
            "cli",
            "executor",
        ],
        (
            "10 分钟: 摘 loop / contract。",
            "25 分钟: 对照现有 Agent Loop 笔记。",
            "60 分钟: 补 trace 或最小实验。",
        ),
    ),
    (
        "M2",
        "Context / Memory",
        [
            "memory",
            "context",
            "retrieval",
            "memory poisoning",
            "context poisoning",
            "prompt injection",
            "context engineering",
        ],
        (
            "10 分钟: 标 memory / context 风险。",
            "25 分钟: 对照现有 context 笔记。",
            "60 分钟: 做最小检索或冲突测试。",
        ),
    ),
    (
        "M3",
        "Harness / Recoverable Execution",
        [
            "checkpoint",
            "resume",
            "recover",
            "recovery",
            "retry",
            "timeout",
            "failure",
            "state",
            "trace",
        ],
        (
            "10 分钟: 提 failure mode。",
            "25 分钟: 画状态流。",
            "60 分钟: 加 checkpoint / resume 试验。",
        ),
    ),
    (
        "M4",
        "Eval / Observability",
        [
            "eval",
            "evaluation",
            "benchmark",
            "observability",
            "telemetry",
            "metric",
            "metrics",
            "compare",
            "comparison",
            "validity",
        ],
        (
            "10 分钟: 抽 eval claim。",
            "25 分钟: 对照现有评测方法。",
            "60 分钟: 写 1 个小 eval。",
        ),
    ),
    (
        "M5",
        "Security / Control",
        [
            "security",
            "threat",
            "prompt injection",
            "authorization",
            "authentication",
            "auth",
            "identity",
            "permission",
            "jailbreak",
            "policy",
        ],
        (
            "10 分钟: 摘 attack surface。",
            "25 分钟: 映射控制点。",
            "60 分钟: 写 threat model 或对抗测试。",
        ),
    ),
    (
        "M6",
        "Protocols / Skills",
        [
            "mcp",
            "protocol",
            "a2a",
            "skill",
            "skills",
            "agent protocol",
            "specification",
            "spec",
            "contract",
        ],
        (
            "10 分钟: 记协议 delta。",
            "25 分钟: 对照 spec / implementation。",
            "60 分钟: 写边界或兼容性 note。",
        ),
    ),
]


@dataclass
class Candidate:
    path: Path
    title: str
    source: str
    category: str
    score: int
    module_id: str
    module_name: str
    reason: str
    next_10: str
    next_25: str
    next_60: str


def load_feed_categories() -> dict[str, str]:
    if not FEEDS_FILE.exists():
        return {}
    data = yaml.safe_load(FEEDS_FILE.read_text(encoding="utf-8")) or {}
    categories: dict[str, str] = {}
    for feed in data.get("feeds", []):
        name = feed.get("name")
        category = feed.get("category", "")
        if name:
            categories[name] = category
    return categories


def parse_note(path: Path):
    text = path.read_text(encoding="utf-8", errors="ignore")
    if not text.startswith("---\n"):
        return None, None
    parts = text.split("---\n", 2)
    if len(parts) < 3:
        return None, None
    try:
        fm = yaml.safe_load(parts[1]) or {}
    except Exception:
        return None, None
    body = parts[2]
    return fm, body


def score_text(text: str, keywords: Iterable[str]) -> tuple[int, list[str]]:
    score = 0
    hits: list[str] = []
    for kw in keywords:
        if kw in text:
            score += 2 if " " in kw else 1
            hits.append(kw)
    return score, hits


def choose_module(blob: str) -> tuple[str, str, list[str], tuple[str, str, str]]:
    best = ("", "", -1, [], "")
    for module_id, module_name, keywords, action in MODULE_RULES:
        score, hits = score_text(blob, keywords)
        if score > best[2]:
            best = (module_id, module_name, score, hits, action)
        elif score == best[2] and score > 0 and len(hits) > len(best[3]):
            best = (module_id, module_name, score, hits, action)
    if best[2] <= 0:
        return (
            "M1",
            "Agent Loop / Tool Contract",
            [],
            (
                "10 分钟: 摘 loop / contract。",
                "25 分钟: 对照现有 Agent Loop 笔记。",
                "60 分钟: 补 trace 或最小实验。",
            ),
        )
    return best[0], best[1], best[3], best[4]


def build_candidates() -> list[Candidate]:
    feed_categories = load_feed_categories()
    candidates: list[Candidate] = []

    for path in sorted(INBOX.glob("*.md")):
        fm, body = parse_note(path)
        if not fm:
            continue

        title = str(fm.get("title", path.stem))
        source = str(fm.get("source", ""))
        category = str(fm.get("category", feed_categories.get(source, "")))
        status = str(fm.get("status", ""))
        score = int(fm.get("score", 0) or 0)
        takeaway = str(fm.get("takeaway", ""))
        blob = " ".join([title, source, category, takeaway, body[:1500]]).lower()

        relevance = 0
        reasons: list[str] = []

        if source in OFFICIAL_SOURCES:
            relevance += 3
            reasons.append("official source")
        if category in {"agent-official", "agent-security", "agent-protocol"}:
            relevance += 2
            reasons.append(category)
        if status == "highlight":
            relevance += 2
            reasons.append("already highlighted")

        module_id, module_name, hits, action = choose_module(blob)
        if hits:
            relevance += min(4, len(hits))
            reasons.append(", ".join(hits[:3]))

        if score >= 5:
            relevance += 1
            reasons.append("rss score")

        if relevance <= 0:
            continue

        next_10, next_25, next_60 = action
        candidates.append(
            Candidate(
                path=path,
                title=title,
                source=source,
                category=category,
                score=relevance,
                module_id=module_id,
                module_name=module_name,
                reason="; ".join(reasons) if reasons else "heuristic match",
                next_10=next_10,
                next_25=next_25,
                next_60=next_60,
            )
        )

    candidates.sort(key=lambda item: (-item.score, item.source, item.title.lower()))
    return candidates


def update_note(path: Path, candidate: Candidate) -> None:
    fm, body = parse_note(path)
    if not fm:
        return

    fm["status"] = "highlight"
    fm["triage-score"] = candidate.score
    fm["triage-module"] = candidate.module_id
    fm["triage-reason"] = candidate.reason
    fm["triage-next-action"] = candidate.next_25

    new_text = "---\n" + yaml.safe_dump(fm, allow_unicode=True, sort_keys=False).rstrip() + "\n---\n" + body.lstrip("\n")
    path.write_text(new_text, encoding="utf-8")


def print_candidates(candidates: list[Candidate], limit: int) -> None:
    rows = candidates[:limit]
    print(f"Top {len(rows)} Inbox candidate(s)")
    print()
    for idx, candidate in enumerate(rows, 1):
        print(f"{idx}. [{candidate.score}] {candidate.title}")
        print(f"   source: {candidate.source} | module: {candidate.module_id} {candidate.module_name}")
        print(f"   reason: {candidate.reason}")
        print(f"   10m: {candidate.next_10}")
        print(f"   25m: {candidate.next_25}")
        print(f"   60m: {candidate.next_60}")
        print(f"   file: {candidate.path}")
        print()


def main() -> None:
    parser = argparse.ArgumentParser(description="Rank Inbox notes for concept promotion")
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--apply", action="store_true", help="Mark top candidates as highlights")
    args = parser.parse_args()

    candidates = build_candidates()
    if not candidates:
        print("No Inbox candidates found.")
        return

    print_candidates(candidates, args.limit)

    if args.apply:
        for candidate in candidates[: args.limit]:
            update_note(candidate.path, candidate)
        print(f"Updated {min(args.limit, len(candidates))} note(s) with highlight metadata.")


if __name__ == "__main__":
    main()
