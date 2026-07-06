#!/usr/bin/env python3
"""
Content Pipeline Script for AI Dev Tools Affiliate Site
Reads keywords.md and tracks which keywords have been written about.
Outputs the next batch of keywords to write about.

Priority order:
  1. Section 9 (High-Intent Long-Tail) — all EASY + HIGH, money pages
  2. Other HIGH intent + EASY difficulty
  3. Other HIGH intent + MEDIUM difficulty
  4. Everything else by intent/difficulty
"""
import re
import os
import json
from pathlib import Path
from datetime import datetime

SITE_DIR = Path.home() / "Hermes" / "ai-tools-site"
KEYWORDS_FILE = SITE_DIR / "research" / "keywords.md"
STATE_FILE = SITE_DIR / "research" / "pipeline-state.json"
CONTENT_DIR = SITE_DIR / "src" / "content"

# IDs 151-180 are the new high-intent long-tail money-page keywords
MONEY_KEYWORD_IDS = set(range(151, 181))


def load_keywords():
    """Parse keywords.md and return list of keyword dicts."""
    keywords = []
    with open(KEYWORDS_FILE) as f:
        for line in f:
            line = line.strip()
            # Match table rows: | # | keyword | intent | page type | difficulty |
            m = re.match(r'\|\s*(\d+)\s*\|\s*(.+?)\s*\|\s*(High|Medium|Low)\s*\|\s*(review|comparison|alternative|list|pricing)\s*\|\s*(Easy|Medium|Hard)\s*\|', line)
            if m:
                kid = int(m.group(1))
                keywords.append({
                    "id": kid,
                    "keyword": m.group(2).strip(),
                    "intent": m.group(3),
                    "page_type": m.group(4),
                    "difficulty": m.group(5),
                    "is_money_page": kid in MONEY_KEYWORD_IDS,
                })
    return keywords


def load_state():
    """Load pipeline state (which keywords have been written)."""
    if STATE_FILE.exists():
        with open(STATE_FILE) as f:
            return json.load(f)
    return {"written_ids": [], "last_run": None, "total_generated": 0}


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def get_content_files():
    """List all existing content files to cross-check."""
    files = []
    for subdir in ["reviews", "comparisons", "alternatives", "bestof"]:
        d = CONTENT_DIR / subdir
        if d.exists():
            for f in d.glob("*.md"):
                files.append(f.stem)
    return files


def next_batch(batch_size=5):
    """Return the next batch of keywords to write about.

    Priority:
      Tier 0: money page keywords (Section 9, IDs 151-180) — always first
      Tier 1: HIGH intent + EASY difficulty
      Tier 2: HIGH intent + MEDIUM difficulty
      Tier 3: everything else
    """
    keywords = load_keywords()
    state = load_state()
    written = set(state["written_ids"])

    # Filter to unwritten
    unwritten = [k for k in keywords if k["id"] not in written]

    def priority(k):
        intent_score = {"High": 0, "Medium": 1, "Low": 2}[k["intent"]]
        diff_score = {"Easy": 0, "Medium": 1, "Hard": 2}[k["difficulty"]]
        money_bonus = 0 if k["is_money_page"] else 1
        return (money_bonus, intent_score, diff_score)

    unwritten.sort(key=priority)
    return unwritten[:batch_size]


def mark_written(ids):
    """Mark keyword IDs as written."""
    state = load_state()
    state["written_ids"].extend(ids)
    state["last_run"] = datetime.now().isoformat()
    state["total_generated"] = len(state["written_ids"])
    save_state(state)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "next":
        batch = next_batch(5)
        if not batch:
            print("ALL DONE: All keywords have been written about.")
        else:
            print(f"NEXT BATCH ({len(batch)} keywords):")
            for k in batch:
                tag = " 💰" if k["is_money_page"] else ""
                print(f"  [{k['id']}] [{k['intent']}] [{k['difficulty']}] {k['keyword']} -> {k['page_type']}{tag}")
    elif len(sys.argv) > 1 and sys.argv[1] == "stats":
        keywords = load_keywords()
        state = load_state()
        money_total = sum(1 for k in keywords if k["is_money_page"])
        money_written = sum(1 for kid in state["written_ids"] if kid in MONEY_KEYWORD_IDS)
        print(f"Total keywords: {len(keywords)}")
        print(f"Written: {len(state['written_ids'])}")
        print(f"Remaining: {len(keywords) - len(state['written_ids'])}")
        print(f"Money pages (Section 9): {money_total} total, {money_written} written, {money_total - money_written} remaining")
        print(f"Last run: {state.get('last_run', 'never')}")
    else:
        print("Usage: python content-pipeline.py [next|stats]")
